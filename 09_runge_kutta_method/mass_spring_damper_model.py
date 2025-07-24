# ----------------------------------------------------------------------------
# Chapter 9: Mass-Spring-Damper System Model
#
# Purpose:
# This script defines the physics of a classic mass-spring-damper system
# and demonstrates how to use our generic `solve_rk4` solver to simulate
# its behavior. This showcases the power of separating the algorithm (the solver)
# from the specific problem (the model).
# ----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# --- Step 1: Import the generic solver ---
# We import the function we created in the other file.
from runge_kutta_solver import solve_rk4

# --- Step 2: Define the physical model ---
# This function represents the specific system we want to solve.

def mass_spring_damper_system(t, y, m, c, k, F_ext):
    """
    Defines the system of ODEs for a mass-spring-damper.

    The 2nd-order ODE `m*x'' + c*x' + k*x = F(t)` is converted into a
    system of two 1st-order ODEs:
    1. y[0]' = y[1]          (where y[0] is displacement x, y[1] is velocity v)
    2. y[1]' = (F(t) - c*y[1] - k*y[0]) / m

    Args:
        t (float): The current time.
        y (np.ndarray): A numpy array [displacement, velocity].
        m (float): Mass (kg).
        c (float): Damping coefficient (N*s/m).
        k (float): Spring constant (N/m).
        F_ext (function): A function that returns the external force at time t.

    Returns:
        np.ndarray: An array of the derivatives [dx/dt, dv/dt].
    """
    displacement, velocity = y
    
    # The derivatives
    d_displacement_dt = velocity
    d_velocity_dt = (F_ext(t) - c * velocity - k * displacement) / m
    
    return np.array([d_displacement_dt, d_velocity_dt])

# --- Step 3: Define a main block to run a standalone example ---
# This allows us to test this model script by itself.
if __name__ == "__main__":
    print("--- Running Mass-Spring-Damper Standalone Example ---")

    # --- Define model parameters ---
    m = 250.0  # mass (kg)
    c = 100.0  # damping (N*s/m)
    k = 15000.0 # spring constant (N/m)

    # Define an external force function (e.g., a sharp bump at the beginning)
    def external_force(t):
        return 1000.0 if t < 0.1 else 0.0

    # --- Define simulation settings ---
    initial_conditions = [0.0, 0.0]  # [initial displacement, initial velocity]
    time_span = (0.0, 5.0)           # (start_time, end_time) in seconds
    time_step = 0.01                 # dt for the solver

    # --- Create a lambda function to pass to the solver ---
    # The solver expects a function that takes only (t, y). We use a lambda
    # to "wrap" our system function, pre-filling the m, c, k, and F_ext parameters.
    system_to_solve = lambda t, y: mass_spring_damper_system(t, y, m, c, k, external_force)

    # --- Call the solver ---
    t_values, y_values = solve_rk4(system_to_solve, initial_conditions, time_span, time_step)

    # The results are in y_values, with displacement in the first column and velocity in the second.
    displacement_results = y_values[:, 0]
    velocity_results = y_values[:, 1]

    # --- Plot the results ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Displacement (m)', color='tab:blue')
    ax1.plot(t_values, displacement_results, color='tab:blue', label='Displacement')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)

    # Create a second y-axis for velocity
    ax2 = ax1.twinx()
    ax2.set_ylabel('Velocity (m/s)', color='tab:red')
    ax2.plot(t_values, velocity_results, color='tab:red', linestyle='--', label='Velocity')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.suptitle('Mass-Spring-Damper System Response (RK4)', fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
