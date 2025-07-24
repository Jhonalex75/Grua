# Chapter 5: Implementing the Bisection Method

Now we arrive at the core of our tutorial: implementing a numerical method. We will start with one of the most intuitive and reliable root-finding algorithms: the **Bisection Method**.

---

### What is the Bisection Method?

The bisection method is a numerical technique used to find the root of a non-linear equation, which is a point `x` where a function `f(x)` equals zero.

The method is based on the **Intermediate Value Theorem**, which states that if a continuous function `f(x)` has values of opposite sign at the endpoints of an interval `[a, b]`, then it must have at least one root within that interval.

### The Algorithm Steps

The process is straightforward and iterative:

1.  **Choose an Interval:** Start with an interval `[a, b]` where the function changes sign, meaning `f(a) * f(b) < 0`.
2.  **Find the Midpoint:** Calculate the middle point of the interval, `c = (a + b) / 2`.
3.  **Evaluate the Function:**
    *   If `f(c)` is very close to zero, then `c` is our approximate root. We're done!
    *   If `f(c)` is not the root, we check the sign. If `f(a)` and `f(c)` have opposite signs, the root must be in the new, smaller interval `[a, c]`. Otherwise, it must be in `[c, b]`.
4.  **Repeat:** We repeat the process with the new, halved interval until the interval is small enough for our desired precision.

### Why is this useful in Engineering?

Many engineering problems (e.g., finding equilibrium points, solving for material stress, analyzing heat transfer) can be described by equations that are too complex to solve directly. The bisection method provides a reliable way to find approximate solutions to these equations.

The script in this folder, `bisection_method_logic.py`, contains a clear implementation of this algorithm.
