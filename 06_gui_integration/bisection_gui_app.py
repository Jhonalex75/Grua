# ----------------------------------------------------------------------------
# Chapter 6: Bisection Method GUI Application
#
# Purpose:
# This script builds a complete GUI application that allows a user to find
# the root of a function using the bisection method. It demonstrates the
# crucial concept of separating logic from presentation by importing the
# `bisection_method` function from another file.
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk # Themed Tkinter widgets for a more modern look

# --- Step 1: Import the backend logic ---
# We import the necessary functions from our logic file. This is the key to
# code reuse and separation of concerns.
from bisection_method_logic import bisection_method, example_function

class BisectionApp:
    """
    This class encapsulates the entire GUI for the bisection method solver.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Bisection Method Solver")
        self.root.geometry("450x400")

        # Use a modern theme
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

        # --- Create and layout the widgets using frames ---
        # Frames are containers that help organize other widgets.
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a dedicated frame for input fields
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="15")
        input_frame.pack(fill=tk.X, pady=10)

        # Create widgets for user input
        self.a_entry = self._create_labeled_entry(input_frame, "Interval Start (a):")
        self.b_entry = self._create_labeled_entry(input_frame, "Interval End (b):")
        self.tol_entry = self._create_labeled_entry(input_frame, "Tolerance:", "1e-7")

        # --- Calculation Button ---
        calculate_button = ttk.Button(main_frame, text="Calculate Root", command=self.calculate_root)
        calculate_button.pack(pady=15)

        # --- Results Area ---
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_label = ttk.Label(result_frame, text="Please enter parameters and click calculate.", font=("Helvetica", 12, "italic"))
        self.result_label.pack(pady=10)

    def _create_labeled_entry(self, parent, label_text, default_value=""):
        """Helper method to create a label and an entry field neatly."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        label = ttk.Label(frame, text=label_text, width=18)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.insert(0, default_value)
        return entry

    def calculate_root(self):
        """
        This method is called when the button is clicked. It gathers input,
        calls the bisection method, and displays the result.
        """
        try:
            # 1. Get and validate user input
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tolerance = float(self.tol_entry.get())

            # 2. Call the imported bisection method function
            root = bisection_method(example_function, a, b, tolerance)

            # 3. Display the result
            if root is not None:
                result_text = f"Approximate Root: {root:.7f}"
                self.result_label.config(text=result_text, foreground="green", font=("Helvetica", 12, "bold"))
            else:
                result_text = "Failed to converge. Try increasing iterations or changing the interval."
                self.result_label.config(text=result_text, foreground="orange", font=("Helvetica", 12, "italic"))

        except ValueError as e:
            # Handle errors from invalid input (e.g., text) or from the bisection method itself
            self.result_label.config(text=f"Error: {e}", foreground="red", font=("Helvetica", 12, "italic"))
        except Exception as e:
            # Catch any other unexpected errors
            self.result_label.config(text=f"An unexpected error occurred: {e}", foreground="red", font=("Helvetica", 12, "italic"))

def main():
    root = tk.Tk()
    app = BisectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
