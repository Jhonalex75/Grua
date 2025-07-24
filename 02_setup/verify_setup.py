# -----------------------------------------------------------------------------
# Chapter 2: Setup Verification Script
#
# Purpose:
# This script performs a simple check to confirm that the Tkinter library
# is correctly installed and available in your Python environment.
#
# How it works:
# 1. It attempts to import the `tkinter` library.
# 2. If the import is successful, it creates a small, simple window.
# 3. If a window appears on your screen, your setup is correct!
# -----------------------------------------------------------------------------

try:
    # We use a 'try...except' block as a safe way to handle potential errors.
    # If Tkinter is not installed, Python would raise an 'ImportError'.
    import tkinter as tk
    
    # --- If the import was successful, the code below will run ---

    print("Tkinter was successfully imported. Creating a test window...")

    # 1. Create the main application window (often called 'root' or 'window').
    #    This is the main container for all other interface elements (widgets).
    root = tk.Tk()

    # 2. Set the title of the window.
    root.title("Tkinter Verification")

    # 3. Create a widget. A 'Label' is a simple widget used to display text.
    #    We tell the Label what window it belongs to ('root') and what text to show.
    message_label = tk.Label(
        root,
        text="Congratulations! Tkinter is installed and working correctly.",
        font=("Helvetica", 12), # We can customize the font and size.
        padx=20, # 'padx' adds some horizontal space (padding) inside the label.
        pady=20  # 'pady' adds some vertical space.
    )

    # 4. Place the widget into the window.
    #    The '.pack()' method is one of the simplest ways to place widgets.
    #    It automatically manages the layout.
    message_label.pack()

    # 5. Start the Tkinter event loop.
    #    This crucial line tells the window to appear on the screen and wait for
    #    user actions (like clicking the close button). The program will stay
    #    running on this line until the window is closed.
    root.mainloop()

    print("Test window closed. Setup is verified!")

except ImportError:
    # This block will only run if the 'import tkinter' line failed.
    print("--- ERROR ---")
    print("Tkinter library not found.")
    print("This is uncommon, as Tkinter is part of the standard Python library.")
    print("Please try reinstalling Python, ensuring the 'tcl/tk and IDLE' option is selected during installation.")
