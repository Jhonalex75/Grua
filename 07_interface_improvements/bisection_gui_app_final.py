# ----------------------------------------------------------------------------
# Chapter 7: Final Bisection Method GUI Application
#
# Purpose:
# This script represents the final, polished version of our application.
# It builds upon the previous chapter by adding frontend validation to provide
# instant, clear feedback to the user, preventing invalid data from ever
# reaching the core algorithm.
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk

# --- Import the backend logic ---
# We continue to reuse our well-defined logic module.
from bisection_method_logic import bisection_method, example_function

class BisectionAppFinal:
    """
    This class encapsulates the final, improved GUI for the bisection method solver.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Bisection Method Solver (Final Version)")
        self.root.geometry("450x400")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="15")
        input_frame.pack(fill=tk.X, pady=10)

        self.a_entry = self._create_labeled_entry(input_frame, "Interval Start (a):")
        self.b_entry = self._create_labeled_entry(input_frame, "Interval End (b):")
        self.tol_entry = self._create_labeled_entry(input_frame, "Tolerance:", "1e-7")

        calculate_button = ttk.Button(main_frame, text="Calculate Root", command=self.calculate_root)
        calculate_button.pack(pady=15)

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
        Gathers input, performs frontend validation, calls the bisection method,
        and displays the result or error messages.
        """
        try:
            # --- Step 1: Get and convert user input ---
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tolerance = float(self.tol_entry.get())

            # --- Step 2: Perform Frontend Validation ---
            # These checks happen before we even call our core logic.
            if a >= b:
                self.result_label.config(text="Error: Interval start 'a' must be less than 'b'.", foreground="red")
                return # Stop execution here
            
            if tolerance <= 0:
                self.result_label.config(text="Error: Tolerance must be a positive number.", foreground="red")
                return # Stop execution here

            # --- Step 3: Call the backend logic ---
            # If frontend validation passes, we can safely call our algorithm.
            root = bisection_method(example_function, a, b, tolerance)

            # --- Step 4: Display the result ---
            if root is not None:
                result_text = f"Approximate Root: {root:.7f}"
                self.result_label.config(text=result_text, foreground="green", font=("Helvetica", 12, "bold"))
            else:
                result_text = "Failed to converge. Try increasing iterations or changing the interval."
                self.result_label.config(text=result_text, foreground="orange", font=("Helvetica", 12, "italic"))

        except ValueError as e:
            # This handles two types of errors:
            # 1. float() conversion fails if input is not a number.
            # 2. The ValueError raised by bisection_method if f(a)*f(b) >= 0.
            self.result_label.config(text=f"Error: {e}", foreground="red", font=("Helvetica", 12, "italic"))
        except Exception as e:
            # Catch any other unexpected errors.
            self.result_label.config(text=f"An unexpected error occurred: {e}", foreground="red", font=("Helvetica", 12, "italic"))

def main():
    root = tk.Tk()
    app = BisectionAppFinal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
