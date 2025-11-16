# %% [markdown]
# # Linear Algebra Pre-Assessment
#
# We want your learning experience to be as efficient as possible. If you already know some linear algebra you might be able to skip some of the lectures in this course. Have a look at the questions below. If you already know how to answer them feel free to skip the videos listed in parentheses.

# %% [markdown]
# ## Question 1: System of Linear Equations
#
# **Translate the following description into a system of linear equations.**
#
# *(Videos: System of sentences, System of equations as lines and planes)*
#
# Bob has a mixture of apples and oranges of the same size, which he split into two bags. The first bag contains 4 apples and 3 oranges and weighs 700g. The second bag contains 2 apples and 6 oranges and weighs 1000g.

# %%
# Solution to Question 1
# Let:
#   x = weight of one apple (in grams)
#   y = weight of one orange (in grams)
#
# System of equations:
#   4x + 3y = 700  (first bag)
#   2x + 6y = 1000 (second bag)

import numpy as np

# Coefficient matrix A
A_q1 = np.array([
    [4, 3],
    [2, 6]
])

# Constants vector b
b_q1 = np.array([700, 1000])

print("Question 1: System of Linear Equations")
print("Coefficient matrix A:")
print(A_q1)
print("\nConstants vector b:")
print(b_q1)
print("\nSystem of equations:")
print("4x + 3y = 700")
print("2x + 6y = 1000")

# Solve the system
solution_q1 = np.linalg.solve(A_q1, b_q1)
print(f"\nSolution: x = {solution_q1[0]}g (apple), y = {solution_q1[1]}g (orange)")

# %% [markdown]
# ## Question 2: Matrix Form
#
# **Translate the following system of linear equations into the matrix form:**
#
# *(Videos: System of Equations)*
#
# $$
# \begin{cases}
# 5x + 3y + 5z = 6 \\
# 7x + 2y + 8z = 17 \\
# 4x + 3z = 8
# \end{cases}
# $$

# %%
# Solution to Question 2
# Matrix form: Ax = b

# Coefficient matrix A
A_q2 = np.array([
    [5, 3, 5],
    [7, 2, 8],
    [4, 0, 3]
])

# Constants vector b
b_q2 = np.array([6, 17, 8])

print("Question 2: Matrix Form")
print("Coefficient matrix A:")
print(A_q2)
print("\nConstants vector b:")
print(b_q2)
print("\nMatrix form: Ax = b")

# Solve the system
solution_q2 = np.linalg.solve(A_q2, b_q2)
print(f"\nSolution: x = {solution_q2[0]}, y = {solution_q2[1]}, z = {solution_q2[2]}")

# %% [markdown]
# ## Question 3: Determinant
#
# **Compute the determinant of the following matrix:**
#
# *(Video: The determinant)*
#
# $$
# \begin{bmatrix}
# 1 & 2 & 1 \\
# 0 & 3 & 5 \\
# 4 & 3 & 8
# \end{bmatrix}
# $$

# %%
# Solution to Question 3
M_q3 = np.array([
    [1, 2, 1],
    [0, 3, 5],
    [4, 3, 8]
])

det_q3 = np.linalg.det(M_q3)

print("Question 3: Determinant")
print("Matrix M:")
print(M_q3)
print(f"\nDeterminant of M: {det_q3}")
print(f"Determinant (rounded): {round(det_q3, 2)}")

# %% [markdown]
# ## Question 4: Linear Dependence
#
# **Does the matrix above have any linear dependent row?**
#
# *(Video: Linear Dependence and Independence)*
#
# A row is linearly dependent if it can be expressed as a linear combination of other rows.

# %%
# Solution to Question 4
print("Question 4: Linear Dependence")
print("Matrix M:")
print(M_q3)

# Calculate the rank of the matrix
rank_q3 = np.linalg.matrix_rank(M_q3)

print(f"\nRank of matrix: {rank_q3}")
print(f"Number of rows: {M_q3.shape[0]}")

if rank_q3 < M_q3.shape[0]:
    print("\n The matrix HAS linearly dependent rows")
    print("  (Rank < Number of rows)")
else:
    print("\n The matrix does NOT have linearly dependent rows")
    print("  (Rank = Number of rows, all rows are linearly independent)")

# %% [markdown]
# ## Question 5: Singular vs Non-singular
#
# **Is the matrix singular or non-singular?**
#
# *(Videos: A geometric notion of singularity, Singular vs Nonsingular matrices)*
#
# - A matrix is **singular** if its determinant = 0
# - A matrix is **non-singular** if its determinant != 0

# %%
# Solution to Question 5
print("Question 5: Singular vs Non-singular")
print("Matrix M:")
print(M_q3)
print(f"\nDeterminant: {det_q3}")

if abs(det_q3) < 1e-10:  # Close to zero (accounting for floating point precision)
    print("\n The matrix is SINGULAR")
    print("  (Determinant = 0)")
    print("  - The matrix is NOT invertible")
    print("  - Rows/columns are linearly dependent")
else:
    print("\n The matrix is NON-SINGULAR")
    print("  (Determinant != 0)")
    print("  - The matrix is invertible")
    print("  - Rows/columns are linearly independent")

    # Calculate and display the inverse
    M_inv = np.linalg.inv(M_q3)
    print("\nInverse matrix M^(-1):")
    print(M_inv)

# %% [markdown]
# ## Summary
#
# This notebook covers fundamental linear algebra concepts:
#
# 1. **System of Linear Equations**: Translating word problems into mathematical equations
# 2. **Matrix Form**: Representing systems as Ax = b
# 3. **Determinant**: Computing the determinant to understand matrix properties
# 4. **Linear Dependence**: Checking if rows/columns are linearly independent
# 5. **Singularity**: Determining if a matrix is invertible
#
# These concepts are foundational for machine learning and data science applications.
