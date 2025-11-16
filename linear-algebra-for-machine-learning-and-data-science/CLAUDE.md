# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is course material for DeepLearning.AI's "Linear Algebra for Machine Learning and Data Science" course, organized into weekly modules covering fundamental linear algebra concepts.

**Course Structure:**
- Week 1: Systems of linear equations
- Week 2: Solving systems of linear equations
- Week 3: Vectors and Linear Transformations
- Week 4: Determinants and Eigenvectors

## Environment Setup

This project uses `uv` for dependency management and requires Python 3.13+.

### Initial Setup

```bash
uv sync
```

This creates a virtual environment at `.venv/` and installs dependencies from `pyproject.toml`.

### Running Python Scripts

```bash
uv run <script_path>
```

Example:
```bash
uv run week-1/system-of-equations/script.py
```

## Dependencies

The project uses NumPy for all linear algebra computations:
- `numpy>=2.3.4`: Matrix operations, linear algebra functions (det, solve, inv, rank)

## Code Organization

### Jupytext Format

Scripts in this repository use Jupytext format (`.py` files with special cell markers):
- `# %% [markdown]` - Markdown cells for explanations, questions, and documentation
- `# %%` - Code cells for executable Python code
- Compatible with both regular Python execution and Jupyter notebook conversion

**Benefits:**
- Can run as regular Python scripts via `uv run`
- Can be opened in VSCode's interactive Python window
- Can be converted to `.ipynb` format using Jupytext

### Week-by-Week Structure

Each week directory contains:
- `README.md`: Links to course slides and materials
- Subdirectories for specific topics with Python scripts demonstrating concepts
- Scripts follow educational format: question → solution → visualization

## Common Linear Algebra Patterns

When working with linear algebra exercises in this codebase:

1. **System of Equations**: Use matrix form `Ax = b` with `np.linalg.solve(A, b)`
2. **Determinants**: Use `np.linalg.det(matrix)` to check singularity
3. **Matrix Rank**: Use `np.linalg.matrix_rank(matrix)` to check linear independence
4. **Matrix Inverse**: Use `np.linalg.inv(matrix)` for non-singular matrices
5. **Singularity Check**: Matrix is singular if `abs(det) < 1e-10` (floating-point tolerance)

### Script Structure Template

```python
# %% [markdown]
# ## Question Title
# Problem statement with mathematical notation

# %%
# Solution with clear variable definitions
# Use meaningful variable names (A, b, x for matrices/vectors)
# Print intermediate steps and final results
```

## Writing Mathematical Formulas

### LaTeX in Markdown Cells (Jupytext `.py` files)

Use LaTeX syntax for mathematical formulas in markdown cells:

**Inline math** (within text): `$...$`
```python
# %% [markdown]
# The determinant is calculated as $\det(A) = ad - bc$ for a 2×2 matrix.
```

**Display math** (separate line): `$$...$$`
```python
# %% [markdown]
# ## Matrix Form
#
# $$
# A\vec{x} = \vec{b}
# $$
#
# where:
# $$
# A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad
# \vec{x} = \begin{bmatrix} x \\ y \end{bmatrix}, \quad
# \vec{b} = \begin{bmatrix} b_1 \\ b_2 \end{bmatrix}
# $$
```

**Common LaTeX patterns for linear algebra:**
- Matrices: `\begin{bmatrix} ... \end{bmatrix}` or `\begin{pmatrix} ... \end{pmatrix}`
- Determinant: `\begin{vmatrix} ... \end{vmatrix}` or `\det(A)`
- Vectors: `\vec{v}` or `\mathbf{v}`
- System of equations: `\begin{aligned} ... \end{aligned}` or `\begin{cases} ... \end{cases}`
- Subscripts: `a_{11}`, Superscripts: `A^{-1}`, `A^T`

### LaTeX in HTML Files

For interactive visualizations and demonstrations, use MathJax 3 in HTML files:

**1. Add MathJax to `<head>`:**
```html
<!-- MathJax for LaTeX rendering -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
    MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']]
        },
        svg: {
            fontCache: 'global'
        }
    };
</script>
```

**2. Use LaTeX in HTML:**
```html
<!-- Inline math -->
<p>The determinant is $\det(A) = ad - bc$</p>

<!-- Display math -->
<div>
    $$
    \det\begin{pmatrix}
    a & b \\
    c & d
    \end{pmatrix} = ad - bc
    $$
</div>
```

**3. Dynamic content with MathJax:**
```javascript
// After updating innerHTML with LaTeX
if (typeof MathJax !== 'undefined') {
    MathJax.typesetPromise([element]).catch((err) => console.log('MathJax error:', err));
}
```

**Examples:**
- [determinant-illustration.html](week-1/system-of-equations/determinant-illustration.html) - Interactive matrix determinant visualization with calculation steps and geometric interpretation using LaTeX formulas
- [matrix-illustration.html](week-1/system-of-equations/matrix-illustration.html) - Matrix transformation visualization in 2D/3D with animated transitions, showing how matrices transform space
