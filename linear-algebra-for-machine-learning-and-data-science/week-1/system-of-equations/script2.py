# %% [markdown]
# ## Calculate Determinant of a Matrix
#
# Calculate the determinant of matrix:
# $$
# A = \begin{bmatrix} 2 & 3 \\ 2 & 4 \end{bmatrix}
# $$
#
# For a 2×2 matrix, the determinant is calculated as:
# $$
# \det(A) = \det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
# $$

# %%
import numpy as np

# Define the matrix
A = np.array([[2, 3],
              [2, 4]])

print("Matrix A:")
print(A)
print()

# Calculate determinant using numpy
det_A = np.linalg.det(A)

print(f"Determinant of A: {det_A}")
print()

# Verify manually: det(A) = (2)(4) - (3)(2) = 8 - 6 = 2
manual_det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
print(f"Manual calculation: ({A[0,0]})({A[1,1]}) - ({A[0,1]})({A[1,0]}) = {manual_det}")
print()

# Check if matrix is singular (determinant ≈ 0)
if abs(det_A) < 1e-10:
    print("Matrix is SINGULAR (no unique solution)")
else:
    print("Matrix is NON-SINGULAR (has unique solution)")

# %% [markdown]
# ## Calculate Determinant of a 3×3 Matrix
#
# Calculate the determinant of matrix:
# $$
# B = \begin{bmatrix}
# 1 & 2 & 1 \\
# 2 & 1 & 1 \\
# -1 & 2 & 1
# \end{bmatrix}
# $$
#
# For a 3×3 matrix, the determinant can be calculated using cofactor expansion:
# $$
# \det(B) = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31})
# $$

# %%
# Define the 3x3 matrix
B = np.array([[1, 2, 1],
              [2, 1, 1],
              [-1, 2, 1]])

print("Matrix B:")
print(B)
print()

# Calculate determinant using numpy
det_B = np.linalg.det(B)

print(f"Determinant of B: {det_B}")
print()

# Verify manually using cofactor expansion along first row
# det(B) = 1*(1*1 - 1*2) - 2*(2*1 - 1*(-1)) + 1*(2*2 - 1*(-1))
term1 = B[0, 0] * (B[1, 1] * B[2, 2] - B[1, 2] * B[2, 1])
term2 = B[0, 1] * (B[1, 0] * B[2, 2] - B[1, 2] * B[2, 0])
term3 = B[0, 2] * (B[1, 0] * B[2, 1] - B[1, 1] * B[2, 0])
manual_det_B = term1 - term2 + term3

print("Manual calculation using cofactor expansion:")
print(f"  1*({B[1,1]}*{B[2,2]} - {B[1,2]}*{B[2,1]}) = 1*({B[1,1]*B[2,2]} - {B[1,2]*B[2,1]}) = {term1}")
print(f"- 2*({B[1,0]}*{B[2,2]} - {B[1,2]}*{B[2,0]}) = 2*({B[1,0]*B[2,2]} - {B[1,2]*B[2,0]}) = {term2}")
print(f"+ 1*({B[1,0]}*{B[2,1]} - {B[1,1]}*{B[2,0]}) = 1*({B[1,0]*B[2,1]} - {B[1,1]*B[2,0]}) = {term3}")
print(f"det(B) = {term1} - {term2} + {term3} = {manual_det_B}")
print()

# Check if matrix is singular
if abs(det_B) < 1e-10:
    print("Matrix is SINGULAR (no unique solution)")
else:
    print("Matrix is NON-SINGULAR (has unique solution)")

# %% [markdown]
# ## Question 4: Linear Dependence/Independence of Matrix Rows
#
# Determine if the following matrix has linearly dependent or independent rows:
# $$
# C = \begin{bmatrix}
# 1 & 2 & 3 \\
# 3 & 2 & 1 \\
# 2 & 2 & 1
# \end{bmatrix}
# $$
#
# **Key Concepts:**
# - Rows are **linearly independent** if the matrix has full rank (rank = number of rows)
# - Rows are **linearly dependent** if rank < number of rows
# - For a square matrix, rows are linearly independent if and only if $\det(C) \neq 0$

# %%
# Define the matrix
C = np.array([[1, 2, 3],
              [3, 2, 1],
              [2, 2, 1]])

print("Matrix C:")
print(C)
print()

# Method 1: Check determinant
det_C = np.linalg.det(C)
print(f"Determinant of C: {det_C}")
print()

# Method 2: Check matrix rank
rank_C = np.linalg.matrix_rank(C)
num_rows = C.shape[0]

print(f"Matrix rank: {rank_C}")
print(f"Number of rows: {num_rows}")
print()

# Determine linear dependence/independence
print("=" * 50)
if rank_C == num_rows:
    print("RESULT: Rows are LINEARLY INDEPENDENT")
    print(f"Reason: Rank ({rank_C}) = Number of rows ({num_rows})")
    if abs(det_C) > 1e-10:
        print(f"Confirmed: det(C) = {det_C:.4f} ≠ 0")
else:
    print("RESULT: Rows are LINEARLY DEPENDENT")
    print(f"Reason: Rank ({rank_C}) < Number of rows ({num_rows})")
    print(f"Confirmed: det(C) = {det_C:.10f} ≈ 0")
    print("\nThis means one row can be expressed as a linear")
    print("combination of the other rows.")
print("=" * 50)

# %% [markdown]
# ## Question 5: Calculate Determinant
#
# Calculate the determinant of the following matrix:
# $$
# A = \begin{bmatrix}
# 1 & 2 & 3 \\
# 0 & 2 & 2 \\
# 1 & 4 & 5
# \end{bmatrix}
# $$
#
# Determine if the matrix is singular or non-singular.

# %%
# Define the matrix
A_q5 = np.array([[1, 2, 3],
                 [0, 2, 2],
                 [1, 4, 5]])

print("Matrix A:")
print(A_q5)
print()

# Calculate determinant using numpy
det_A_q5 = np.linalg.det(A_q5)

print(f"Determinant of A: {det_A_q5}")
print()

# Verify manually using cofactor expansion along first column (easier due to 0)
# det(A) = 1*|2 2; 4 5| - 0*|2 3; 4 5| + 1*|2 3; 2 2|
minor_11 = A_q5[1, 1] * A_q5[2, 2] - A_q5[1, 2] * A_q5[2, 1]
minor_21 = A_q5[0, 1] * A_q5[2, 2] - A_q5[0, 2] * A_q5[2, 1]
minor_31 = A_q5[0, 1] * A_q5[1, 2] - A_q5[0, 2] * A_q5[1, 1]

manual_det_A_q5 = A_q5[0, 0] * minor_11 - A_q5[1, 0] * minor_21 + A_q5[2, 0] * minor_31

print("Manual calculation using cofactor expansion along first column:")
print(f"  1 * |2 2; 4 5| = 1 * (2*5 - 2*4) = 1 * {minor_11} = {A_q5[0,0] * minor_11}")
print("- 0 * |2 3; 4 5| = 0 * ... = 0")
print(f"+ 1 * |2 3; 2 2| = 1 * (2*2 - 3*2) = 1 * {minor_31} = {A_q5[2,0] * minor_31}")
print(f"det(A) = {A_q5[0,0] * minor_11} - 0 + {A_q5[2,0] * minor_31} = {manual_det_A_q5}")
print()

# Determine if singular or non-singular
print("=" * 50)
if abs(det_A_q5) < 1e-10:
    print("ANSWER: det(A) = 0. The matrix is SINGULAR.")
    print("(The matrix has no inverse and systems may have no or infinite solutions)")
else:
    print(f"ANSWER: det(A) = {det_A_q5:.0f}. The matrix is NON-SINGULAR.")
    print("(The matrix has an inverse and systems have unique solutions)")
print("=" * 50)

# %% [markdown]
# ## Question 6: Find Values for Linearly Dependent Rows
#
# Consider the matrix:
# $$
# M = \begin{bmatrix}
# 2 & 1 & 5 \\
# 1 & 2 & 1 \\
# x & y & z
# \end{bmatrix}
# $$
#
# For which values $x, y, z$ does the matrix have linearly dependent rows?
#
# **Approach:**
# - Rows are linearly dependent when det(M) = 0
# - Test each option by calculating the determinant

# %%
# Test option 1: x=1, y=3, z=3
print("Testing Option 1: x=1, y=3, z=3")
M1 = np.array([[2, 1, 5],
               [1, 2, 1],
               [1, 3, 3]])

det_M1 = np.linalg.det(M1)
rank_M1 = np.linalg.matrix_rank(M1)

print("Matrix M1:")
print(M1)
print(f"Determinant: {det_M1}")
print(f"Rank: {rank_M1}")

if abs(det_M1) < 1e-10:
    print("✓ Rows are LINEARLY DEPENDENT (det = 0)")
else:
    print("✗ Rows are linearly independent (det ≠ 0)")
print()

# Test option 2: x=3, y=3, z=6
print("Testing Option 2: x=3, y=3, z=6")
M2 = np.array([[2, 1, 5],
               [1, 2, 1],
               [3, 3, 6]])

det_M2 = np.linalg.det(M2)
rank_M2 = np.linalg.matrix_rank(M2)

print("Matrix M2:")
print(M2)
print(f"Determinant: {det_M2}")
print(f"Rank: {rank_M2}")

if abs(det_M2) < 1e-10:
    print("✓ Rows are LINEARLY DEPENDENT (det = 0)")
    # Check if row 3 is a linear combination of rows 1 and 2
    print("\nVerification: Check if row3 = a*row1 + b*row2")
    # If row3 = a*row1 + b*row2, then:
    # 3 = 2a + 1b
    # 3 = 1a + 2b
    # 6 = 5a + 1b
    # Solve for a and b
    A_sys = np.array([[2, 1], [1, 2]])
    b_sys = np.array([3, 3])
    coeffs = np.linalg.solve(A_sys, b_sys)
    print("Solving: row3 = a*row1 + b*row2")
    print(f"a = {coeffs[0]:.2f}, b = {coeffs[1]:.2f}")
    # Verify
    row3_calc = coeffs[0] * M2[0] + coeffs[1] * M2[1]
    print(f"Calculated row3: {row3_calc}")
    print(f"Actual row3: {M2[2]}")
else:
    print("✗ Rows are linearly independent (det ≠ 0)")
print()

# Test option 3: x=1, y=2, z=3
print("Testing Option 3: x=1, y=2, z=3")
M3 = np.array([[2, 1, 5],
               [1, 2, 1],
               [1, 2, 3]])

det_M3 = np.linalg.det(M3)
rank_M3 = np.linalg.matrix_rank(M3)

print("Matrix M3:")
print(M3)
print(f"Determinant: {det_M3}")
print(f"Rank: {rank_M3}")

if abs(det_M3) < 1e-10:
    print("✓ Rows are LINEARLY DEPENDENT (det = 0)")
else:
    print("✗ Rows are linearly independent (det ≠ 0)")
print()

# Summary
print("=" * 50)
print("SUMMARY:")
print(f"Option 1 (x=1, y=3, z=3): det = {det_M1:.4f} → {'DEPENDENT' if abs(det_M1) < 1e-10 else 'independent'}")
print(f"Option 2 (x=3, y=3, z=6): det = {det_M2:.4f} → {'DEPENDENT' if abs(det_M2) < 1e-10 else 'independent'}")
print(f"Option 3 (x=1, y=2, z=3): det = {det_M3:.4f} → {'DEPENDENT' if abs(det_M3) < 1e-10 else 'independent'}")
print("=" * 50)