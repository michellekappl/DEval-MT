import os
from multiprocessing import Process, Queue, freeze_support
from typing import List, Tuple

from simalign import SentenceAligner  # Make sure simalign is installed

# Import our custom classes - handle both relative and absolute imports
try:
    # Try relative imports first (when used as a package)
    from .live_dashboard import LiveDashboard
    from .output_capture import capture_all_output
    from .word_alignment import WordAlignment
except ImportError:
    # Fall back to absolute imports (when run directly)
    from live_dashboard import LiveDashboard
    from output_capture import capture_all_output
    from word_alignment import WordAlignment

class AlignmentProcessor:
    """
    Main class that handles word alignment between source and target sentences
    """
    def __init__(self, model: str, token_type: str, matching_method: str):
        # For more information about these parameters, see the simalign documentation (https://github.com/cisnlp/simalign)
        self.model = model              # AI model to use (e.g., "bert")
        self.token_type = token_type    # How to split words (e.g., "bpe")
        self.matching_method = matching_method  # Algorithm for matching (e.g., "itermax")

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

    def process_multiple(self, sources: List[List[str]], targets: List[List[str]]) -> List[List[WordAlignment]]:
        """
        Main method that processes multiple translation sets using parallel processing
    
        - Each set of original & translated sentences is a "supertask"
        - For each supertask, we divide the pages among multiple workers (CPU cores)
        - Each worker processes their pages and reports progress
        - We show everything in a live dashboard
        
        Returns:
            List of results for each supertask, where each supertask contains
            WordAlignment objects for all sentence pairs in that set
        """
        # Combine sources and targets into supertasks
        # Example: [(german_sentences, english_sentences), (german_sentences, spanish_sentences)]
        supertasks = list(zip(sources, targets))
        
        # Store results for all supertasks
        all_results = []

        # Start the live dashboard
        with LiveDashboard(len(supertasks)) as live_dashboard:
            
            # Process each translation set
            for supertask_idx, (original, translation) in enumerate(supertasks):
                
                # 1. Decide how many workers (CPU cores) to use
                #    Don't use more workers than sentences, and don't exceed available CPU cores
                num_batches = min(len(original), os.cpu_count() or 1)
                
                # 2. Calculate how many sentences each worker gets
                batch_size = max(1, len(original) // num_batches)
                
                # 3. Split sentences into batches (like giving each worker a stack of pages)
                batches = [
                    (original[i:i + batch_size], translation[i:i + batch_size])
                    for i in range(0, len(original), batch_size)
                ]

                # Setup the dashboard to show progress for this translation set
                live_dashboard.setup_supertask(supertask_idx, batches)

                # Create a communication channel between workers and main process
                queue = Queue()  # Like a mailbox where workers can send messages
                
                # Create worker processes (like hiring multiple translators)
                processes = [
                    Process(
                        target=alignment_worker,  # The function each worker will run
                        args=(self.model, self.token_type, self.matching_method,
                            batch[0], batch[1], queue, i)  # Arguments for the worker
                    )
                    for i, batch in enumerate(batches)
                ]

                # Start all worker processes (like telling all translators to start working)
                for p in processes:
                    p.start()

                # Keep track of which workers have finished and their results
                completed = set()
                batch_results = {}  # Store results from each batch by task_id

                # Main loop: listen for messages from workers until all are done
                while len(completed) < len(processes):
                    try:
                        # Check if any worker sent a message (with 0.1 second timeout)
                        msg = queue.get(timeout=0.1)
                        
                        if msg[0] == "progress":
                            # Worker says: "I finished sentence X"
                            _, task_id, step = msg
                            live_dashboard.update_progress(task_id, step)
                            
                        elif msg[0] == "log":
                            # Worker says: "Here's what I'm doing..."
                            _, task_id, content = msg
                            live_dashboard.add_log(task_id, content)
                            
                        elif msg[0] == "results":
                            # Worker says: "Here are my alignment results"
                            _, task_id, results = msg
                            batch_results[task_id] = results
                            
                        elif msg[0] == "done":
                            # Worker says: "I'm completely finished"
                            completed.add(msg[1])
                            
                    except:
                        # No message received in 0.1 seconds, continue checking
                        pass

                # Wait for all worker processes to completely finish
                for p in processes:
                    p.join()

                # Combine results from all batches in order
                supertask_results = []
                for i in range(len(batches)):
                    if i in batch_results:
                        supertask_results.extend(batch_results[i])
                
                # Add this supertask's results to the overall results
                all_results.append(supertask_results)

                # Update dashboard to show this translation set is complete
                live_dashboard.finalize_supertask()
        
        # Return the results of the alignment
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
        # Create the AI model (each process needs its own copy)
        aligner = SentenceAligner(model=model, token_type=token_type, matching_methods="mai")
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

    # If the worker produced any output, send it back to main process
    if captured.strip():
        # Split output into lines and send each line separately
        for line in captured.strip().splitlines():
            queue.put(("log", task_id, line))

    # Tell the main process: "I'm completely finished"
    queue.put(("done", task_id))