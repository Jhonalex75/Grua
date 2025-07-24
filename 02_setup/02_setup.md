# Chapter 2: Setting Up Your Environment

Before we can start building our application, we need to ensure that you have Python and the Tkinter library correctly installed.

---

### 1. Installing Python

If you don't have Python installed, download the latest version from the official website:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

**Important:** During installation, make sure to check the box that says **"Add Python to PATH"**. This will allow you to run Python from your computer's terminal easily.

### 2. Verifying the Tkinter Installation

Tkinter is part of Python's standard library, so it is usually included with your Python installation. You can easily verify this.

1.  Open your system's terminal (Command Prompt on Windows, Terminal on macOS/Linux).
2.  Type the following command and press Enter:

    ```bash
    python -m tkinter
    ```

If a small window appears with the title "tk" and some buttons, congratulations! Tkinter is installed and working correctly.

### 3. Running the Verification Script

This tutorial folder includes a simple script to double-check that everything is ready. To run it, navigate to this directory (`02_setup`) in your terminal and execute:

```bash
python verify_setup.py
```

This will open a window confirming that Tkinter is ready for our project.

*(Note: If you encounter an error in step 2 or 3, you may need to install Tkinter manually. This is rare, but the command is typically `sudo apt-get install python3-tk` on Debian/Ubuntu Linux or reinstalling Python on Windows/macOS, ensuring the "tcl/tk and IDLE" option is selected.)*
