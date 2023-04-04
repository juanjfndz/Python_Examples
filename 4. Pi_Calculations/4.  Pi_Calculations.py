import random
import math
from decimal import Decimal, getcontext

#-----------------------------------------------------------------------------#
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

def ramanujan_series_term(k):
    numerator = Decimal(factorial(4 * k)) * (1103 + 26390 * k)
    denominator = Decimal(factorial(k)) ** 4 * 396 ** (4 * k)
    return Decimal(numerator / denominator)


def ramanujan_pi(precision=100):
    getcontext().prec = precision + 10
    series_sum = Decimal(0)
    k = 0

    while True:
        term = ramanujan_series_term(k)
        if term < 10 ** (-precision):
            break
        series_sum += term
        k += 1

    constant = Decimal(2 * math.sqrt(2) / 9801)
    pi_estimate = Decimal(1 / (constant * series_sum))
    return round(pi_estimate, precision)
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
def arctan_term(x, n):
    """Calculate the arctan term in the Machin-like formula."""
    return (-1) ** n * (x ** (2 * n + 1)) / (2 * n + 1)


def arctan_series(x, num_terms):
    """Calculate the arctan series for a given x and number of terms."""
    return sum(arctan_term(x, n) for n in range(num_terms))


def machin_pi(num_terms=1000):
    """Compute an approximation of pi using Machin-like formula.
    
    Parameters:
    num_terms (int): Number of terms to use in the series approximation.
    
    Returns:
    float: Approximation of pi.
    """
    pi_over_4 = 4 * arctan_series(1/5, num_terms) - arctan_series(1/239, num_terms)
    return 4 * pi_over_4
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
def monte_carlo_pi(iterations):
    """Estimate the value of Pi using the Monte Carlo method.
    
    :param iterations: The number of random points to generate in the simulation.
    :type iterations: int
    :return: The estimated value of Pi.
    :rtype: float
    """

    if iterations < 1:
        raise ValueError("Iterations must be greater than 0.")

    points_inside_circle = 0

    for _ in range(iterations):
        x = random.random()
        y = random.random()

        distance_to_origin = math.sqrt(x**2 + y**2)

        if distance_to_origin <= 1:
            points_inside_circle += 1

    return (4 * points_inside_circle) / iterations
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
def taylor_pi(num_terms: int) -> float:
    """
    Estimate the value of pi using the Taylor series expansion of arctan(x) with x = 1.

    :param num_terms: The number of terms to include in the series.
    :return: The estimated value of pi.
    """
    taylor_sum = 0
    for i in range(num_terms):
        term = (-1) ** i / (2 * i + 1)
        taylor_sum += term

    pi_estimate = 4 * taylor_sum
    return pi_estimate
#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    num_terms = 100000
    # Example usage:
    print(f"Estimated value of pi using {num_terms} terms: ")
    print(f"   Monte Carlo method: {monte_carlo_pi(num_terms):.10f}")
    print(f"   Taylor method: {taylor_pi(num_terms):.10f}\n")
    print(f"Machin method: {machin_pi():.16f}")
    print(f"Ramanujan method (presicion 50): {ramanujan_pi(precision=50)}")
    print(f"Math library pi constant: {math.pi:.50f}")