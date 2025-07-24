# ----------------------------------------------------------------------------
# Chapter 3: Main Window Application
#
# Purpose:
# This script demonstrates the fundamental steps to create the main window
# of a desktop application using the Tkinter library.
# ----------------------------------------------------------------------------

# 1. Import the Tkinter library
#    We import the library and give it a shorter, conventional alias 'tk'
#    to make our code cleaner and easier to type.
import tkinter as tk

def main():
    """
    This function contains the main logic for creating and running our
    simple windowed application.
    """
    # 2. Create the main application window instance.
    #    The `tk.Tk()` class creates the top-level window. You should only have
    #    one of these in your application. We assign it to a variable,
    #    conventionally named 'root', 'window', or 'app'.
    window = tk.Tk()

    # 3. Configure the window's properties.
    #    - .title(): Sets the text that appears in the window's title bar.
    #    - .geometry(): Sets the initial size of the window in pixels ("widthxheight").
    window.title("My First GUI Application")
    window.geometry("500x350") # Width=500px, Height=350px

    # 4. Start the Tkinter event loop.
    #    This is the most important step. The .mainloop() method tells Python
    #    to display the window and listen for events (like mouse clicks or
    #    key presses). The program will stay in this loop until the window
    #    is closed. Without this line, the window would appear and disappear
    #    instantly.
    window.mainloop()

# This is a standard Python convention.
# The code inside this 'if' block will only run when the script is executed
# directly (e.g., `python main_window_app.py`). It won't run if the script
# is imported as a module into another file.
if __name__ == "__main__":
    main()
