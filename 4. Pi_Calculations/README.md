# Pi Approximation Methods

This repository contains Python code in both a Python script and Jupyter notebook for approximating the mathematical constant Pi using different methods:

1. Monte Carlo method
2. Taylor series expansion of arctan(x)
3. Machin-like formula
4. Ramanujan series

## Code Files

The Python code is provided in two formats:

1. `4. Pi_Calculations.py`: A Python script that can be run from the command line.
2. `Pi_Calculations.ipynb`: A Jupyter notebook that contains the same code as the Python script along with additional explanations and visualizations.

## Approximation Methods

### Monte Carlo Method

The Monte Carlo method is a probabilistic algorithm used to estimate the value of Pi. It works by generating random points within a square and determining whether they lie within a quarter of a unit circle centered at the origin. The ratio of the number of points within the circle to the total number of points generated is then used to estimate the value of Pi. This method has a relatively low accuracy and requires a large number of iterations to produce a good approximation.

### Taylor Series Expansion of Arctan(x)

The Taylor series expansion of the arctan(x) function can be used to estimate the value of Pi. This method involves summing an infinite series of terms where each term depends on the previous one. As more terms are added to the sum, the approximation becomes more accurate. However, the method converges relatively slowly and requires a large number of terms to produce a good approximation.

### Machin-like Formula

The Machin-like formula is another way to approximate Pi. It involves using the arctan function to compute Pi as a linear combination of two angles: arctan(1/5) and arctan(1/239). This method has a faster convergence rate than the Taylor series expansion of arctan(x) but requires the use of two separate arctan series.

### Ramanujan Series

The Ramanujan series is a formula for computing Pi that was discovered by the Indian mathematician Srinivasa Ramanujan. It involves summing an infinite series of terms and has a very fast convergence rate. However, the formula requires the use of large factorials and is computationally expensive.

## Usage

To use the Python script, simply run the `4. Pi_Calculations.py` file from the command line. You can modify the `num_terms` variable to change the number of terms used in the approximation methods. The output will show the estimated value of Pi for each method, as well as the actual value of Pi obtained from the `math` library.

To use the Jupyter notebook, open the `Pi_Calculations.ipynb` file in a Jupyter notebook environment. The notebook contains the same code as the Python script along with additional explanations and visualizations.

Note that the Monte Carlo method may produce slightly different results each time it is run due to the random nature of the algorithm.

## Requirements

The code requires Python 3.x and the `decimal`, 'random' and `math` libraries.