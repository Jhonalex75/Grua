# Chapter 6: Integrating the Algorithm with the GUI

This is the most exciting chapter. We will now connect our numerical method logic (the "backend") with our graphical user interface (the "frontend"). This is a fundamental concept in software development: **separation of concerns**.

Our algorithm is in one file, and our GUI is in another. This makes our code:

*   **Reusable:** We can use our `bisection_method` in other applications.
*   **Maintainable:** We can update the GUI without breaking the algorithm, and vice-versa.
*   **Testable:** It's easier to test the logic separately from the user interface.

---

### What You Will Learn

1.  **Importing Your Own Code:** How to import the `bisection_method` function from our previous script.
2.  **Structuring the App:** How to build a clean layout for input fields (`Entry`), labels (`Label`), and a results area.
3.  **Handling User Input:** How to get values from multiple `Entry` widgets, convert them to numbers, and handle potential errors (e.g., the user types text instead of a number).
4.  **Displaying Results:** How to call the bisection method with the user's data and display the calculated root or any error messages directly in the GUI.

### Running the Script

Execute the `bisection_gui_app.py` script in this folder to launch the interactive application.

```bash
python bisection_gui_app.py
```
