import os
import sys
import threading


def capture_all_output(func, *args, **kwargs):
   """
   Runs a function while capturing all its output (including from C libraries)
   
   This is like recording everything a worker says, even whispers.
   Some AI libraries print messages directly to the screen, bypassing Python's
   normal print system. This function catches ALL output, even those sneaky messages.
   
   Returns: (function_result, captured_output_string)
   """
   # Create a pipe (like a telephone line) to capture output
   r, w = os.pipe()

   def reader(pipe):
      """Background thread that reads from the pipe"""
      with os.fdopen(pipe) as f:
         while True:
               data = f.read(1024)  # Read in chunks of 1024 characters
               if not data:
                  break
               captured.append(data)

   captured = []  # List to store all captured output
   t = threading.Thread(target=reader, args=(r,))  # Start background reader
   t.start()

   # Save the original output destinations
   stdout_fd = sys.stdout.fileno()
   stderr_fd = sys.stderr.fileno()
   saved_stdout_fd = os.dup(stdout_fd)
   saved_stderr_fd = os.dup(stderr_fd)

   # Redirect all output to our pipe
   os.dup2(w, stdout_fd)
   os.dup2(w, stderr_fd)
   os.close(w)

   try:
      # Run the actual function
      result = func(*args, **kwargs)
   finally:
      # Restore original output destinations (very important!)
      os.dup2(saved_stdout_fd, stdout_fd)
      os.dup2(saved_stderr_fd, stderr_fd)
      os.close(saved_stdout_fd)
      os.close(saved_stderr_fd)

   t.join()  # Wait for background reader to finish
   output = "".join(captured)  # Combine all captured text
   return result, output
