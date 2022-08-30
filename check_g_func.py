import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


# -- Non-linear weights -- #
def weight_conf(x):
	# g = 4*(x-0.5)**2
	g = 1.6 * x ** 2 - 1.6 * x + 1
	return g


def weight_cov(x):
	# f = -4*(x-0.5)**2 + 1
	f = -1.6 * x ** 2 + 1.6 * x
	return f


# # -- Linear weights -- #
# def weight_conf(x):
#     y = 2*x - 1
#     y[x<0.5] = -2*x[x<0.5] + 1
#     return y
#
# def weight_cov(x):
#     f = np.zeros(x.shape)
#     f[x <= 0.5] = 2*x[x <= 0.5]
#     f[x > 0.5] = -2 * x[x> 0.5] + 2
#     return f


# -- Functions to convert confidence level/coverage ratio to speed adjustment -- #
def conf_to_adj(x):
	# g = 4*(x-0.5)**2
	g = 2 * x - 1
	return g


def cr_to_adj(x):
	# f = -2*x + 1
	if isinstance(x, float):
		if x <= 0.2:
			f = -5 * x + 1
		else:
			f = -1.25 * x + 0.25
	else:
		f = -5 * x + 1
		f[x > 0.2] = -1.25 * x[x > 0.2] + 0.25
	return f


# -- G(x,y) -- #
def G(conf, cov_ratio):
	# g = weight_conf(conf)*conf + weight_cov(conf)*(cov_ratio)
	# g = weight_conf(conf) + weight_cov(cov_ratio)
	# print(weight_conf(conf))
	# print(weight_cov(conf))
	g = weight_conf(conf) * conf_to_adj(conf) + weight_cov(conf) * cr_to_adj(cov_ratio)
	return g


# -- Test cases -- #
def select_case(case_id):
	if case_id == 1:
		# -- Case #1 -- #
		conf = 0.8
		cov_ratio = 0.05
		print('Expected action: Faster ++')
	elif case_id == 2:
		# -- Case #2 -- #
		conf = 0.8
		cov_ratio = 0.6
		print('Expected action: Faster +')
	elif case_id == 3:
		# -- Case #3 -- #
		conf = 0.4
		cov_ratio = 0.05
		print('Expected action: Slower -')
	elif case_id == 4:
		# -- Case #4 -- #
		conf = 0.4
		cov_ratio = 0.6
		print('Expected action: Slower --')
	elif case_id == 5:
		# -- Case #3 -- #
		conf = 0.6
		cov_ratio = 0.4
		print('Expected action: Slower -')
	elif case_id == 6:
		# -- Case #4 -- #
		conf = 0.6
		cov_ratio = 0.8
		print('Expected action: Slower --')
	else:
		print('Non-defined Case')
	return conf, cov_ratio


# -- Print case-specific results -- #
for id in [1, 2, 3, 4, 5, 6]:
	print('Case #{}#'.format(id))
	conf, cov_ratio = select_case(id)
	print('Conf: {:.2f}, Cov_Ratio:{:.2f}'.format(conf, cov_ratio))
	print('G(x,y) = {:.4f}\n'.format(G(conf, cov_ratio)))

# -- Make data -- #
conf = np.arange(0.0, 1, 0.005)
cov_ratio = np.arange(0.0, 1, 0.005)
X, Y = np.meshgrid(conf, cov_ratio)
Z = G(X, Y)

plt.figure()
plt.plot(conf, weight_conf(conf), 'orange', label='weight_conf')
plt.plot(conf, weight_cov(conf), label='weight_cr')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.grid()

plt.figure()
plt.plot(conf, conf_to_adj(conf), 'orange', label='f_conf')
plt.plot(conf, cr_to_adj(conf), label='g_cr')
plt.xlim(0, 1)
plt.ylim(-1, 1)
plt.legend()
plt.grid()

# Plot the surface.
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
					   linewidth=0, antialiased=False)
# ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.02f}')

fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel('Confidence')
ax.set_ylabel('Coverage Ratio')
plt.show()
