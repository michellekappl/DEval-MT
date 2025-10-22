import os
from multiprocessing import Process, Queue
from typing import List
import pandas as pd
from simalign import SentenceAligner

from Dataset import DEvalDataset  # Note: Make sure simalign is installed
from alignment.live_dashboard import LiveDashboard
from alignment.output_capture import capture_all_output
from alignment.word_alignment import WordAlignment

class AlignmentProcessor:
    """Handles word alignment between source and target sentences."""
    def __init__(self, model: str, token_type: str, matching_method: str, *, use_multiprocessing: bool = True, max_workers: int | None = None):
        self.model = model
        self.token_type = token_type
        self.matching_method = matching_method
        self.use_multiprocessing = use_multiprocessing
        self.max_workers = max_workers

    def __align_single__(self, original: str, translation: str, aligner: SentenceAligner) -> WordAlignment:
        """Align a single pair of sentences (find which words match)"""
        # Split sentences into individual words
        src_split = original.split()
        trg_split = translation.split()
        
        # Use the AI model to find alignments
        alignments = aligner.get_word_aligns(src_split, trg_split)
        
        # Return the alignments using our chosen method as a WordAlignment object
        alignment_tuples = alignments[self.matching_method]
        return WordAlignment(original, translation, alignment_tuples)

    @classmethod
    def read_from_file(cls, filepath: str) -> List[WordAlignment]:
        """Read alignments from a file and return a list of WordAlignment objects."""
        alignments = []
        raw_alignments: pd.DataFrame = pd.read_csv(filepath)
        for _, row in raw_alignments.iterrows():
            source = row['source']
            target = row['target']
            alignment_str = row['alignment']
            alignment_tuples = []
            for pair in alignment_str.split():
                src_idx, trg_idx = map(int, pair.split('-'))
                alignment_tuples.append((src_idx, trg_idx))
            alignments.append(WordAlignment(source, target, alignment_tuples))
        return alignments


    def process_multiple(self, ds: DEvalDataset, original_column: str, translation_columns: List[str] | None = None) -> dict[str, List[WordAlignment]]:
        """Process translation columns in a dataset and produce word alignments.

        Args:
            ds: DEvalDataset instance with a source column and translation columns registered.
            translation_columns: Optional explicit list of dataset column names containing translations.
                If None, all registered translation columns (ds.translation_columns.values()) are used.

        Returns:
            Dict[str, List[WordAlignment]] mapping each translation column name to a list of WordAlignment objects.
        """
        # Choose source column
        if original_column in ds.df.columns:
            source_series = ds.df[original_column]
        else:
            raise ValueError(f"Dataset requires a source sentence column that matches the provided column name ('{original_column}').")

        # Determine translation columns
        if translation_columns is None:
            translation_columns = list(ds.translation_columns.values())
            if not translation_columns:
                raise ValueError("No translation columns registered. Use ds.add_translations or ds.translate first.")
        else:
            missing = [c for c in translation_columns if c not in ds.df.columns]
            if missing:
                raise ValueError(f"Missing translation columns: {missing}")

        base_source = source_series.tolist()
        targets = [ds.df[col].tolist() for col in translation_columns]
        labels = translation_columns
        supertasks = list(zip([base_source]*len(targets), targets))

        all_results: dict[str, List[WordAlignment]] = {}

        with LiveDashboard(len(supertasks), labels=labels) as live_dashboard:
            for supertask_idx, (original, translation) in enumerate(supertasks):
                current_label = labels[supertask_idx]

                # Determine parallelism parameters,
                # i.e. number of batches to split into depending on CPU core count and max_workers parameter
                cpu_count = os.cpu_count() or 1
                configured_workers = self.max_workers if (self.max_workers is not None and self.max_workers > 0) else cpu_count
                num_batches = min(len(original), configured_workers)
                batch_size = max(1, len(original) // num_batches)
                batches = [
                    (original[i:i+batch_size], translation[i:i+batch_size])
                    for i in range(0, len(original), batch_size)
                ]

                live_dashboard.setup_supertask(supertask_idx, batches)
                batch_results = {}

                if self.use_multiprocessing and num_batches > 1 and __name__ == '__main__':
                    print("Using multiprocessing with {} batches".format(num_batches))
                    # Multiprocessing path
                    queue = Queue()
                    processes = [
                        Process(
                            target=alignment_worker,
                            args=(self.model, self.token_type, self.matching_method, b[0], b[1], queue, i)
                        ) for i, b in enumerate(batches)
                    ]
                    for p in processes:
                        p.start()

                    completed = set()
                    while len(completed) < len(processes):
                        try:
                            msg = queue.get(timeout=0.1)
                            kind = msg[0]
                            if kind == "progress":
                                _, task_id, step = msg
                                live_dashboard.update_progress(task_id, step)
                            elif kind == "log":
                                _, task_id, content = msg
                                live_dashboard.add_log(task_id, content)
                            elif kind == "results":
                                _, task_id, results = msg
                                batch_results[task_id] = results
                            elif kind == "done":
                                completed.add(msg[1])
                        except:
                            pass

                    for p in processes:
                        p.join()
                else:
                    print("Using single-process mode with {} batches".format(num_batches))
                    if __name__ != '__main__':
                        print("⚠️ Warning: Multiprocessing disabled because __name__ != '__main__'. This is expected in notebooks or scripts without a __main__ guard and can be fixed by adding a __main__ guard around the main script.")
                    # Single-process fallback (spawn-safe; good for notebooks or scripts without __main__ guard)
                    for i, (orig_batch, trg_batch) in enumerate(batches):
                        def do_alignment_inline():
                            aligner = SentenceAligner(model=self.model, token_type=self.token_type, matching_methods="i")
                            results = []
                            for step, (src, trg) in enumerate(zip(orig_batch, trg_batch), start=1):
                                src_split = src.split()
                                trg_split = trg.split()
                                aligns = aligner.get_word_aligns(src_split, trg_split)
                                tuples = aligns[self.matching_method]
                                results.append(WordAlignment(src, trg, tuples))
                                live_dashboard.update_progress(i, step)
                            return results
                        results, captured = capture_all_output(do_alignment_inline)
                        if captured.strip():
                            for line in captured.strip().splitlines():
                                live_dashboard.add_log(i, line)
                        batch_results[i] = results

                supertask_results: List[WordAlignment] = []
                for i in range(len(batches)):
                    if i in batch_results:
                        supertask_results.extend(batch_results[i])
                all_results[current_label] = supertask_results
                live_dashboard.finalize_supertask()

        return all_results


def alignment_worker(model: str, token_type: str, matching_method: str, originals: List[str], translations: List[str], queue: Queue, task_id: int):
    """
    This is what each worker process runs:
    1. Create the minimal AI model needed for alignment
    2. Process each sentence pair 
    3. Report progress back to main process
    4. Send results back when done
    """
    def do_alignment():
        # Create the AI model (each process needs its own copy); only compute itermax ('i') for efficiency
        aligner = SentenceAligner(model=model, token_type=token_type, matching_methods="i")
        results = []
        
        # Process each sentence pair
        for i, (src, trg) in enumerate(zip(originals, translations)):
            # Split sentences into individual words
            src_split = src.split()
            trg_split = trg.split()
            
            # Use the AI model to find alignments
            alignments = aligner.get_word_aligns(src_split, trg_split)
            
            # Get the alignments using the specified method and create WordAlignment object
            alignment_tuples = alignments[matching_method]
            word_alignment = WordAlignment(src, trg, alignment_tuples)
            results.append(word_alignment)

            # Report progress: "I finished sentence number i+1"
            queue.put(("progress", task_id, i + 1))

        return results

    # Run the alignment work and capture any output it produces
    results, captured = capture_all_output(do_alignment)

    # Send the results back to the main process
    queue.put(("results", task_id, results))

    # # If the worker produced any output, send it back to main process
    if captured.strip():
        # Split output into lines and send each line separately
        for line in captured.strip().splitlines():
            queue.put(("log", task_id, line))

    # Tell the main process: "I'm completely finished"
    queue.put(("done", task_id))