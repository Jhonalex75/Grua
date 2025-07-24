# ----------------------------------------------------------------------------
# Chapter 5: Bisection Method Logic
#
# Purpose:
# This script provides a clear, well-commented implementation of the
# bisection method algorithm for finding the root of a function.
# This file contains only the core logic, making it reusable.
# ----------------------------------------------------------------------------

def example_function(x):
    """
    This is an example function for which we want to find the root.
    The equation is: f(x) = x^3 - x - 2
    This function has a root between x=1 and x=2.
    """
    return x**3 - x - 2

def bisection_method(func, a, b, tolerance=1e-7, max_iterations=100):
    """
    Implements the bisection method to find a root of a function.

    Args:
        func (function): The function for which to find a root. It must take one float argument.
        a (float): The start of the interval.
        b (float): The end of the interval.
        tolerance (float, optional): The desired precision of the root.
                                     The algorithm stops when the interval size |b-a| is smaller than this.
                                     Defaults to 1e-7.
        max_iterations (int, optional): The maximum number of iterations to prevent infinite loops.
                                        Defaults to 100.

    Raises:
        ValueError: If the initial interval [a, b] does not bracket a root
                    (i.e., f(a) and f(b) have the same sign).

    Returns:
        float: The approximate value of the root.
        None: If the method fails to converge within max_iterations.
    """
    # --- Step 1: Validate the initial interval ---
    # The bisection method requires the function to have opposite signs at the
    # endpoints of the interval. This guarantees a root exists between them.
    fa = func(a)
    fb = func(b)
    if fa * fb >= 0:
        raise ValueError("The function must have opposite signs at the interval endpoints a and b.")

    # --- Step 2: Iteratively narrow down the interval ---
    for i in range(max_iterations):
        # Calculate the midpoint of the current interval.
        c = (a + b) / 2.0
        fc = func(c)

        # --- Step 3: Check for convergence ---
        # We check if the interval is now smaller than our desired tolerance.
        # If it is, 'c' is a good enough approximation of the root.
        if (b - a) / 2.0 < tolerance:
            print(f"Converged after {i+1} iterations.")
            return c

        # --- Step 4: Select the new, smaller interval ---
        # We check which half of the interval contains the root and discard the other half.
        if fa * fc < 0:
            # The root is in the left half: [a, c]
            b = c
            fb = fc # Update fb for the next iteration
        else:
            # The root is in the right half: [c, b]
            a = c
            fa = fc # Update fa for the next iteration

    # If the loop finishes without converging, we return None.
    print(f"Failed to converge within {max_iterations} iterations.")
    return None

# --- Example of how to use the bisection_method function ---
# This block of code will only run if the script is executed directly.
# It will not run if this file is imported as a module into another script.
if __name__ == "__main__":
    print("--- Running Bisection Method Example ---")

    # Define the interval [a, b]
    interval_a = 1.0
    interval_b = 2.0

    print(f"Function: f(x) = x^3 - x - 2")
    print(f"Searching for a root in the interval [{interval_a}, {interval_b}]...")

    try:
        # Call our bisection method function
        root = bisection_method(example_function, interval_a, interval_b)

        # Display the result
        if root is not None:
            print(f"\nApproximate root found: {root:.7f}")
            print(f"Value of the function at the root: f({root:.7f}) = {example_function(root):.7f}")
        else:
            print("\nCould not find a root within the maximum number of iterations.")

    except ValueError as e:
        # This will catch the error if the initial interval is invalid.
        print(f"\nError: {e}")
