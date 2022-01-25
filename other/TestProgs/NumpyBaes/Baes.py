import numpy
import pymc

# Generate data with noise
number_points = 20
true_coefficients = [10.4, 5.5]
x = numpy.linspace(0, 10, number_points)
noise = numpy.random.normal(size=number_points)
data = true_coefficients[0] * x + true_coefficients[1] + noise

# PRIORs:
# as sigma is unknown then we define it as a parameter:
sigma = pymc.Uniform('sigma', 0., 100.)
# fitting the line y = a*x+b, hence the coefficient are parameters:
a = pymc.Uniform('a', 0., 20.)
b = pymc.Uniform('b', 0., 20.)


# define the model: if a, b and x are given the return value is determined, hence the model is deterministic:
@pymc.deterministic(plot=False)
def linear_fit(a=a, b=b, x=x):
    return a * x + b


# LIKELIHOOD
# normal likelihood with observed data (with noise), model value and sigma
y = pymc.Normal('y', mu=linear_fit, tau=1.0 / sigma ** 2, value=data, observed=True)
print(y)
