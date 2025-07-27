# ----------------------------------------------------------------------------
# Chapter 9: Interactive Mass-Spring-Damper Simulation GUI
#
# Purpose:
# This is the final application of the tutorial. It combines all learned
# concepts to create a professional-grade interactive simulation tool.
# It demonstrates:
#   - Importing and using separate logic modules (solver and model).
#   - Building a clean, class-based GUI with modern widgets.
#   - Embedding a Matplotlib plot directly into the Tkinter window for
#     dynamic and professional data visualization.
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import numpy as np

# --- Matplotlib imports for embedding plots in Tkinter ---
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Step 1: Import our custom modules ---
# We import the generic solver and the specific system model we created.
from runge_kutta_solver import solve_rk4
from mass_spring_damper_model import mass_spring_damper_system

class MassSpringDamperApp:
    """
    Encapsulates the entire GUI application for the simulation.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Mass-Spring-Damper Simulation")
        self.root.geometry("800x600")

        # --- Configure the main layout --- 
        # The window is split into a control panel on the left and a plot on the right.
        self.root.columnconfigure(1, weight=3) # Give more weight to the plot column
        self.root.rowconfigure(0, weight=1)

        # --- Control Panel Frame ---
        control_frame = ttk.LabelFrame(self.root, text="System Parameters", padding=15)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Create input fields for physical parameters
        self.m_entry = self._create_labeled_entry(control_frame, "Mass (m):\n[kg]", "250.0")
        self.c_entry = self._create_labeled_entry(control_frame, "Damping (c):\n[N*s/m]", "100.0")
        self.k_entry = self._create_labeled_entry(control_frame, "Spring K (k):\n[N/m]", "15000.0")
        
        # Simulation button
        simulate_button = ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        simulate_button.pack(pady=20)

        # --- Plotting Frame ---
        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Create the Matplotlib figure and axes
        self.fig, self.ax1 = plt.subplots(figsize=(7, 5))
        self.ax2 = self.ax1.twinx() # Create a second y-axis

        # Create the Tkinter canvas to hold the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize with a welcome plot
        self.show_initial_plot()

    def _create_labeled_entry(self, parent, label_text, default_value=""):
        """Helper method to create a label and an entry field."""
        frame = ttk.Frame(parent)
        frame.pack(pady=10, fill=tk.X)
        label = ttk.Label(frame, text=label_text)
        label.pack()
        entry = ttk.Entry(frame, width=20, justify='center')
        entry.pack()
        entry.insert(0, default_value)
        return entry

    def show_initial_plot(self):
        """Displays a welcome message on the plot area before the first simulation."""
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.text(0.5, 0.5, 'Click "Run Simulation" to see the results.',
                      ha='center', va='center', fontsize=12, style='italic')
        self.ax1.set_xlabel('')
        self.ax1.set_ylabel('')
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.canvas.draw()

    def run_simulation(self):
        """Gathers input, runs the simulation, and updates the plot."""
        try:
            # 1. Get parameters from the GUI
            m = float(self.m_entry.get())
            c = float(self.c_entry.get())
            k = float(self.k_entry.get())

            # Basic validation
            if m <= 0 or c < 0 or k <= 0:
                raise ValueError("Physical parameters must be positive (c can be zero).")

            # 2. Define simulation settings
            initial_conditions = [0.0, 0.0]  # [x(0), v(0)]
            time_span = (0.0, 5.0)
            time_step = 0.01

            def external_force(t):
                return 1000.0 if t < 0.1 else 0.0

            # 3. Prepare the system for the solver
            system_to_solve = lambda t, y: mass_spring_damper_system(t, y, m, c, k, external_force)

            # 4. Call the generic RK4 solver
            t_values, y_values = solve_rk4(system_to_solve, initial_conditions, time_span, time_step)
            displacement = y_values[:, 0]
            velocity = y_values[:, 1]

            # 5. Update the plot with the new results
            self.ax1.clear()
            self.ax2.clear()

            self.ax1.plot(t_values, displacement, color='tab:blue', label='Displacement')
            self.ax1.set_xlabel('Time (s)')
            self.ax1.set_ylabel('Displacement (m)', color='tab:blue')
            self.ax1.tick_params(axis='y', labelcolor='tab:blue')
            self.ax1.grid(True, which='both')

            self.ax2.plot(t_values, velocity, color='tab:red', linestyle='--', label='Velocity')
            self.ax2.set_ylabel('Velocity (m/s)', color='tab:red')
            self.ax2.tick_params(axis='y', labelcolor='tab:red')

            self.fig.suptitle('System Response', fontsize=14)
            self.fig.tight_layout(rect=[0, 0, 1, 0.96])
            self.canvas.draw()

        except ValueError as e:
            tk.messagebox.showerror("Input Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("An Unexpected Error Occurred", str(e))

def main():
    root = tk.Tk()
    app = MassSpringDamperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
