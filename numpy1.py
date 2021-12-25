import numpy as np

# seed for reproducibility
np.random.seed(0)

x1 = np.random.randint(10, size=6)  # One-dimensional array
x2 = np.random.randint(10, size=(3, 4))  # Two-dimensional array
x3 = np.random.randint(10, size=(3, 4, 5))  # Three-dimensional array

# print(x3.ndim, x3.shape, x3.size, x3.itemsize, x3.nbytes)

print(x1)

newX1 = x1
newX2 = x1.copy()
newX1[0] = 6

print(x1)
print(newX1)
print(newX2)