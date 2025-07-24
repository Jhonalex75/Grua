# ----------------------------------------------------------------------------
# Chapter 4: Basic Widgets Application
#
# Purpose:
# This script introduces the concept of building a GUI application using a
# Python class. This is a more organized and scalable approach compared to
# using global variables for widgets.
# ----------------------------------------------------------------------------

import tkinter as tk

# --- Professional GUI Structure: Using a Class ---
# As applications grow, managing all widgets (buttons, labels, etc.) as
# separate variables becomes messy. A class acts as a blueprint or container
# for our application, keeping all related widgets and functions neatly organized.

class BasicApp:
    """
    This class encapsulates our entire GUI application.
    """
    def __init__(self, root):
        """
        The constructor for our application class.
        'root' is the main window that this application will be built inside of.
        """
        # Store the root window and configure it.
        self.root = root
        self.root.title("Basic Widgets App")
        self.root.geometry("400x250")

        # --- Create the widgets --- 
        # We create the widgets and attach them to 'self' so they can be
        # accessed from other methods within this class.

        # 1. A Label for instructions.
        self.instruction_label = tk.Label(self.root, text="Please enter your name:", font=("Helvetica", 12))
        self.instruction_label.pack(pady=10)

        # 2. An Entry widget for user input.
        self.name_entry = tk.Entry(self.root, width=30, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        # 3. A Button to trigger an action.
        #    The 'command' is set to a method of this class: self.show_greeting
        self.greet_button = tk.Button(self.root, text="Show Greeting", command=self.show_greeting)
        self.greet_button.pack(pady=15)

        # 4. A Label to display the result.
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"))
        self.result_label.pack(pady=10)

    def show_greeting(self):
        """
        This method is called when the 'greet_button' is clicked.
        """
        # Get the text from the Entry widget.
        user_name = self.name_entry.get()

        # Check if the user entered something.
        if user_name:
            greeting = f"Hello, {user_name}!"
        else:
            greeting = "Please enter a name first."

        # Update the text of the result label.
        self.result_label.config(text=greeting)

def main():
    """
    The main function to set up and run the application.
    """
    # Create the main window instance.
    root = tk.Tk()
    # Create an instance of our application class, passing the root window to it.
    app = BasicApp(root)
    # Start the event loop.
    root.mainloop()

if __name__ == "__main__":
    main()
