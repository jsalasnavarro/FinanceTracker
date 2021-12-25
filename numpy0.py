import numpy as np

# making a simple array
simpleArr = np.array([0, 1, 2, 3])

# 3x3 array as a nested list with a range of var i to i+3
arr = np.array([range(i, i+3) for i in [2, 4, 6]])

# alternative use of range
# start = 2
# end = 6
# step = 1
newArr = np.arange(2, 5, 1).reshape(1,3)

# 1x10 array of zeros
zer = np.zeros(10, dtype=int)
# print(zer)

# 3x5 array of ones
ones = np.ones((3, 5), dtype=float)
# print(ones)

# an 3x5 array w/ specified number other than 1 or 0
myArr = np.full((3,5), 3.14)
# print(myArr)

# array of 5 values evenly spaced between 0 and 5
arr1 = np.linspace(0, 5, 5, dtype=float)
# print(arr1)

# array of uniformly distributed random values between 0 and 1
rand = np.random.random((3,3))
# print(rand)

# array of uniformly distributed random values between 0 and 1 with a std of 1
rand1 = np.random.normal(0, 1, (3, 3))
print(rand1)

# 3x3 array of random integers between 0 and 10
randInt = np.random.randint(0, 10, (3,3))
print(randInt)

# 3x3 identity matrix
idMat = np.eye(3)
print(idMat)

# uninitialized array of 3 ints, values are what exist at location in memory
un = np.empty(3)
print(un)