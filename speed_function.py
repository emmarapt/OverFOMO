from numpy import meshgrid
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

""" Functions """


def objective(x, y, weight_cl, weight_cr):
    return weight_cl * (x ** 2) - weight_cr * (y ** 2)


def weight_cr_fun(x, y):
    return - x ** 2 + x + y


# define range for input
r_min, r_max = 0, 1.0
# sample input range uniformly at 0.1 increments
xaxis = np.arange(r_min, r_max, 0.1).tolist()
yaxis = np.arange(r_min, r_max, 0.1).tolist()

# Defining the range for the input values on the horizontal axis
cl = np.arange(0, 1, 0.1).tolist()
cr = np.arange(0, 1, 0.1).tolist()

""" Plot for Weight_CL """

plt.style.use('seaborn-darkgrid')
fig1, ax = plt.subplots()

# Computing the values of the quadratic equation for different values in x_values
y_cl = [(x + 0.2) ** 2 + x - 1 for x in cl]
# y_inv = [-(x + 0.2) ** 2 - x + 1 for x in cl]

# y_cr = [-x**2 - x for x in cr]
ax.plot(cl, y_cl, linewidth=2)
# ax.plot(cr, y_cr, linewidth=2)
plt.xlabel('Confidence level')
plt.ylabel('Weight for CL')
plt.title('Plot for Weight_CL')
plt.legend(["weight_cl", "weight_cr"])
plt.grid()

# create a mesh from the axis
cl, cr = meshgrid(xaxis, yaxis)
"""for speed"""
objective_fun_speed = objective(cl, cr, weight_cl=0.8, weight_cr=0.2)
""" for weight CR"""
objective_fun_cr = weight_cr_fun(cl, cr)

""" Plot for Weight_CR"""

fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(cl, cr, objective_fun_cr, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
ax.set_xlabel('Confidence level')
ax.set_ylabel('Coverage ratio')
ax.set_zlabel('Weight for CR')
ax.set_title('Plot for Weight_CR')
ax.view_init(azim=-20, elev=15)
plt.grid()

""" Plot for Speed """

fig3 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(cl, cr, objective_fun_speed, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
ax.set_xlabel('Confidence level')
ax.set_ylabel('Coverage ratio')
ax.set_zlabel('Change speed')
ax.set_title('Plot for Speed')
ax.view_init(azim=-100, elev=15)
plt.grid()

plt.show()
