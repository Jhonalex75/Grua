# ----------------------------------------------------------------------------
# Chapter 9: Generic 4th-Order Runge-Kutta Solver
#
# Purpose:
# This script provides a general-purpose function to solve a system of
# first-order ordinary differential equations (ODEs) using the classical
# 4th-order Runge-Kutta (RK4) method. This solver is designed to be
# completely independent of any specific problem, making it a reusable
# and powerful tool for numerical analysis.
# ----------------------------------------------------------------------------

import numpy as np

def solve_rk4(system_of_odes, y0, t_span, dt):
    """
    Solves a system of first-order ODEs using the RK4 method.

    The RK4 method is a numerical technique for approximating the solution of
    ODEs. It provides a good balance of accuracy and computational cost.

    Args:
        system_of_odes (function): The function defining the system of ODEs.
                                   It must take `t` (time) and `y` (a numpy array of state variables)
                                   as arguments and return a numpy array of the derivatives (dy/dt).
        y0 (list or np.ndarray): A list or array of the initial conditions for the state variables
                                 [y1(0), y2(0), ...].
        t_span (tuple): A tuple containing the start and end time for the simulation, e.g., (0, 10).
        dt (float): The time step (h) for the integration. A smaller dt increases
                    accuracy but also computation time.

    Returns:
        tuple: A tuple containing two numpy arrays:
               - t_values: The array of time points from t_start to t_end.
               - y_values: A 2D numpy array where each row corresponds to a time point and each
                           column corresponds to a state variable in the system.
    """
    # --- 1. Setup the time array ---
    t_start, t_end = t_span
    # Ensure the number of steps is an integer
    num_steps = int((t_end - t_start) / dt)
    t_values = np.linspace(t_start, t_end, num_steps + 1)

    # --- 2. Initialize the solution array ---
    # Convert initial conditions to a numpy array for vector operations
    y0 = np.array(y0, dtype=float)
    num_variables = len(y0)
    y_values = np.zeros((num_steps + 1, num_variables))
    y_values[0, :] = y0

    # --- 3. The RK4 Integration Loop ---
    # This loop iterates through each time step to solve the system.
    for i in range(num_steps):
        t = t_values[i]
        y = y_values[i, :]

        # The core of the RK4 method is to calculate four "slopes" (k1, k2, k3, k4)
        # across the interval. Each 'k' is an array of derivatives for all variables.
        k1 = np.array(system_of_odes(t, y), dtype=float)
        k2 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k1), dtype=float)
        k3 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k2), dtype=float)
        k4 = np.array(system_of_odes(t + dt, y + dt * k3), dtype=float)

        # The next value of y is calculated using a weighted average of the four slopes.
        # The middle slopes (k2, k3) are given more weight, which is key to the method's accuracy.
        y_next = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        y_values[i + 1, :] = y_next

    return t_values, y_values
