import os
from multiprocessing import Process, Queue, freeze_support
from typing import List, Tuple

from simalign import SentenceAligner  # Make sure simalign is installed

# Import our custom classes - handle both relative and absolute imports
try:
    # Try relative imports first (when used as a package)
    from .live_dashboard import LiveDashboard
    from .output_capture import capture_all_output
except ImportError:
    # Fall back to absolute imports (when run directly)
    from live_dashboard import LiveDashboard
    from output_capture import capture_all_output

class AlignmentProcessor:
    """
    Main class that handles word alignment between source and target sentences
    """
    def __init__(self, model: str, token_type: str, matching_method: str):
        # For more information about these parameters, see the simalign documentation (https://github.com/cisnlp/simalign)
        self.model = model              # AI model to use (e.g., "bert")
        self.token_type = token_type    # How to split words (e.g., "bpe")
        self.matching_method = matching_method  # Algorithm for matching (e.g., "itermax")

    def __align_single__(self, original: str, translation: str, aligner: SentenceAligner) -> List[Tuple[int, int]]:
        """Align a single pair of sentences (find which words match)"""
        # Split sentences into individual words
        src_split = original.split()
        trg_split = translation.split()
        
        # Use the AI model to find alignments
        alignments = aligner.get_word_aligns(src_split, trg_split)
        
        # Return the alignments using our chosen method
        return alignments[self.matching_method]

    def __align_multiple__(self, originals: List[str], translations: List[str], queue: Queue, task_id: int = -1) -> List[List[Tuple[int, int]]]:
        """Align multiple sentence pairs (this runs on each CPU core)"""
        # Create the AI model (each process needs its own copy)
        aligner = SentenceAligner(model=self.model, token_type=self.token_type, matching_methods="mai")
        results = []
        
        # Process each sentence pair
        for i, (src, trg) in enumerate(zip(originals, translations)):
            aligned = self.__align_single__(src, trg, aligner)
            results.append(aligned)

            # Tell the main process: "I finished sentence number i+1"
            queue.put(("progress", task_id, i + 1))

        return results

    def process_multiple(self, sources: List[List[str]], targets: List[List[str]]) -> None:
        """
        Main method that processes multiple translation sets using parallel processing
    
        - Each set of original & translated sentences is a "supertask"
        - For each supertask, we divide the pages among multiple workers (CPU cores)
        - Each worker processes their pages and reports progress
        - We show everything in a live dashboard
        """
        # Combine sources and targets into supertasks
        # Example: [(german_sentences, english_sentences), (german_sentences, spanish_sentences)]
        supertasks = list(zip(sources, targets))

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
                        target=process_batch_worker,  # The function each worker will run
                        args=(self.model, self.token_type, self.matching_method,
                            batch[0], batch[1], queue, i)  # Arguments for the worker
                    )
                    for i, batch in enumerate(batches)
                ]

                # Start all worker processes (like telling all translators to start working)
                for p in processes:
                    p.start()

                # Keep track of which workers have finished
                completed = set()

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
                            
                        elif msg[0] == "done":
                            # Worker says: "I'm completely finished"
                            completed.add(msg[1])
                            
                    except:
                        # No message received in 0.1 seconds, continue checking
                        pass

                # Wait for all worker processes to completely finish
                for p in processes:
                    p.join()

                # Update dashboard to show this translation set is complete
                live_dashboard.finalize_supertask()


def align_sentences_batch(model, token_type, matching_method, originals, translations, queue, task_id):
    """
    Helper function that creates an AlignmentProcessor and processes a batch of sentences
    
    This is what each worker process actually runs. It's separate from the main class
    because of how Python multiprocessing works - each process needs its own copy of everything.
    """
    processor = AlignmentProcessor(model, token_type, matching_method)
    return processor.__align_multiple__(originals, translations, queue, task_id)


def process_batch_worker(model, token_type, matching_method, originals, translations, queue: Queue, task_id: int):
    """
    The main function that each worker process runs
    
    This is like the job description for each worker:
    1. Process your batch of sentences
    2. Capture any output/messages you produce
    3. Send those messages back to the main process
    4. Report when you're done
    """
    def do_align():
        """Wrapper function to do the actual alignment work"""
        return align_sentences_batch(model, token_type, matching_method, originals, translations, queue, task_id)

    # Run the alignment work and capture any output it produces
    _, captured = capture_all_output(do_align)

    # If the worker produced any output, send it back to main process
    if captured.strip():
        # Split output into lines and send each line separately
        # (This prevents overwhelming the log display with huge messages)
        for line in captured.strip().splitlines():
            queue.put(("log", task_id, line))

    # Tell the main process: "I'm completely finished"
    queue.put(("done", task_id))


if __name__ == "__main__":
    # This prevents issues with multiprocessing on Windows
    freeze_support()

    # Example usage with dummy data
    # In real usage, you would replace this with your actual sentence data
    
    # Each list represents one "translation set" (like one experiment or language pair)
    fake_sources = [
        # German sentences (100 copies of the same sentence for demonstration)
        ["Der Geschäftsführer mochte die Friseurin, weil ihm die angebotenen Frisuren gefielen."] * 1000,
        ["Der Geschäftsführer küsste seine Freundin."] * 2000,
        ["Kim ist Manager."] * 1200
    ]
    fake_targets = [
        # Corresponding translations
        ["The manager liked the hairdresser because he liked the offered hairstyles."] * 1000,  # English
        ["El gerente besó a su novia."] * 2000,  # Spanish
        ["Kim est le manager."] * 1200  # French
    ]

    # Create the processor with specific settings
    # - "bert": Use BERT model for word alignment
    # - "bpe": Use Byte-Pair Encoding for tokenization
    # - "itermax": Use iterative maximum matching algorithm
    processor = AlignmentProcessor("bert", "bpe", "itermax")
    
    # Start processing! This will:
    # 1. Show a live dashboard
    # 2. Process each translation set using multiple CPU cores
    # 3. Display progress and logs in real-time
    processor.process_multiple(fake_sources, fake_targets)
