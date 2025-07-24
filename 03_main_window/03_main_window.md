# Chapter 3: Creating the Main Window

Every desktop application needs a main window. This window acts as the primary container for all the other elements of your user interface, such as buttons, text boxes, and plots.

In this chapter, we will write a simple script to create and display the main window for our application using Tkinter.

---

### Key Steps

The process of creating a basic window in Tkinter involves these core steps:

1.  **Import the Library:** We must first import the `tkinter` library to get access to its tools.
2.  **Create the Main Instance:** We create an object from the `tk.Tk` class. This object represents the main window itself.
3.  **Configure the Window:** We can set properties like the window's title and its initial size.
4.  **Start the Event Loop:** We call the `.mainloop()` method. This is a crucial step that actually displays the window and makes it listen for user actions (like closing the window).

### Running the Script

You can execute the `main_window_app.py` script in this folder to see the result: a simple, empty window.

```bash
python main_window_app.py
```
