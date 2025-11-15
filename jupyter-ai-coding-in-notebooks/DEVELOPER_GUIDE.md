# Developer Guide - Jupyter AI Coding in Notebooks

This guide provides detailed instructions for working with the Jupyter AI Coding course materials.

## Overview

This course teaches AI-assisted coding in Jupyter notebooks using OpenAI's API. You'll learn to:
- Use AI to generate and explain code in notebooks
- Work with external APIs (Open Library)
- Build AI-powered tools and assistants
- Integrate LLMs into data analysis workflows

## Prerequisites

- **Python 3.13+** installed
- **uv** package manager installed ([installation guide](https://github.com/astral-sh/uv))
- **OpenAI API key** (get one at [platform.openai.com](https://platform.openai.com))

## Quick Start

### 1. Install Dependencies

From the `jupyter-ai-coding-in-notebooks` directory:

```bash
uv sync
```

This creates a virtual environment at `.venv/` and installs all dependencies:
- openai>=1.0.0
- python-dotenv>=1.0.0
- ipykernel>=6.0.0
- pandas>=2.0.0
- nbformat>=5.0.0
- nbconvert>=7.0.0
- requests>=2.31.0

### 2. Configure OpenAI API Key

Create a `.env` file in the exercise directory:

```bash
# For Exercise 1
cd exercise-1
echo "OPENAI_API_KEY=your_api_key_here" > .env
cd ..

# For Exercise 2 (if needed)
cd exercise-2
echo "OPENAI_API_KEY=your_api_key_here" > .env
cd ..
```

**Important:** Never commit `.env` files to git. They're already in `.gitignore`.

### 3. Start Jupyter Lab

```bash
uv run jupyter lab
```

This opens Jupyter Lab in your browser at `http://localhost:8888`

## Project Structure

```
jupyter-ai-coding-in-notebooks/
├── exercise-1/
│   ├── L1 - Coding with Jupyter AI Lab.ipynb
│   ├── data/
│   │   └── customer_reviews.csv
│   └── .env (create this)
├── exercise-2/
│   ├── L2 - Book Research Assistant.ipynb
│   ├── openlibrary_api_docs.md
│   └── .env (create this if needed)
├── pyproject.toml
├── uv.lock
└── .venv/ (auto-created)
```

## Working with Exercises

### Exercise 1: Coding with Jupyter AI Lab

This exercise covers basic AI-assisted coding with data analysis.

**Start interactive session:**
```bash
uv run jupyter lab
```
Then navigate to `exercise-1/L1 - Coding with Jupyter AI Lab.ipynb`

**Execute entire notebook:**
```bash
uv run jupyter nbconvert --to notebook --execute --inplace "exercise-1/L1 - Coding with Jupyter AI Lab.ipynb" --ExecutePreprocessor.timeout=120 --allow-errors
```

**Key concepts:**
- Loading environment variables with `python-dotenv`
- Using OpenAI client with `gpt-4o-mini`
- Analyzing CSV data with pandas
- Generating summaries and insights with LLMs

### Exercise 2: Book Research Assistant

This exercise builds an AI book research assistant using Open Library API.

**Start interactive session:**
```bash
uv run jupyter lab
```
Then navigate to `exercise-2/L2 - Book Research Assistant.ipynb`

**Execute entire notebook:**
```bash
uv run jupyter nbconvert --to notebook --execute --inplace "exercise-2/L2 - Book Research Assistant.ipynb" --ExecutePreprocessor.timeout=120 --allow-errors
```

**Key concepts:**
- Making HTTP requests with `requests` library
- Working with external APIs (Open Library)
- Creating tool functions for AI agents
- Building chat handlers with automatic function calling

**API Documentation:**
See `exercise-2/openlibrary_api_docs.md` for complete Open Library API reference.

## Common Commands

### Running Notebooks

**Interactive mode (recommended for learning):**
```bash
uv run jupyter lab
```

**Execute and save results:**
```bash
uv run jupyter nbconvert --to notebook --execute --inplace "path/to/notebook.ipynb"
```

**Execute with timeout and error handling:**
```bash
uv run jupyter nbconvert --to notebook --execute --inplace "path/to/notebook.ipynb" --ExecutePreprocessor.timeout=300 --allow-errors
```

### Running Specific Cells

There are several ways to run specific cells in Jupyter notebooks:

#### Method 1: Interactive Mode (Recommended)

The easiest way is to use Jupyter Lab interactively:

```bash
uv run jupyter lab
```

Then in Jupyter Lab:
- **Run single cell:** Click cell, press `Shift+Enter` (runs and moves to next)
- **Run cell in place:** Click cell, press `Ctrl+Enter` (runs, stays on same cell)
- **Run all cells above:** Cell menu → Run All Above
- **Run all cells below:** Cell menu → Run All Below
- **Run selected cells:** Select multiple cells (Shift+Click), then `Shift+Enter`

**Keyboard shortcuts:**
- `Shift+Enter` - Run cell and select next
- `Ctrl+Enter` - Run cell in place
- `Alt+Enter` - Run cell and insert below
- `A` - Insert cell above (in command mode)
- `B` - Insert cell below (in command mode)
- `DD` - Delete cell (in command mode)
- `M` - Change to markdown cell
- `Y` - Change to code cell

#### Method 2: Execute Specific Cell Ranges with nbconvert

You can't directly specify cell numbers with nbconvert, but you can use tags:

**Step 1:** Tag cells in Jupyter Lab
1. Select cell
2. Click property inspector (gear icon) or View → Show Right Sidebar
3. Add tag (e.g., "run-this", "test", "analysis")

**Step 2:** Execute tagged cells
```bash
# This requires custom script - see Method 3 below
```

#### Method 3: Programmatic Cell Execution

Create a Python script to execute specific cells:

**execute_cells.py:**
```python
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

def execute_specific_cells(notebook_path, cell_indices):
    """
    Execute specific cells in a notebook by their index.

    Args:
        notebook_path: Path to the .ipynb file
        cell_indices: List of cell indices to execute (0-based)
    """
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Create a new notebook with only selected cells
    selected_cells = [nb.cells[i] for i in cell_indices if i < len(nb.cells)]

    # Create temporary notebook
    temp_nb = nbformat.v4.new_notebook()
    temp_nb.cells = selected_cells
    temp_nb.metadata = nb.metadata

    # Execute
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(temp_nb, {'metadata': {'path': './'}})

    # Update original notebook with results
    for i, cell_idx in enumerate(cell_indices):
        if cell_idx < len(nb.cells):
            nb.cells[cell_idx] = temp_nb.cells[i]

    # Save
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Executed cells {cell_indices} in {notebook_path}")

if __name__ == "__main__":
    # Example: python execute_cells.py notebook.ipynb 0 2 5
    notebook = sys.argv[1]
    cells = [int(x) for x in sys.argv[2:]]
    execute_specific_cells(notebook, cells)
```

**Usage:**
```bash
# Execute cells 0, 2, and 5
uv run python execute_cells.py "exercise-1/L1 - Coding with Jupyter AI Lab.ipynb" 0 2 5

# Execute just cell 1
uv run python execute_cells.py "exercise-2/L2 - Book Research Assistant.ipynb" 1
```

#### Method 4: Extract and Run Cell Code

Extract specific cell code and run it directly:

**Extract cell code:**
```python
import nbformat

# Read notebook
with open('notebook.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# Get cell 2 code (0-indexed)
cell_code = nb.cells[2]['source']
print(cell_code)

# Save to Python file
with open('cell_2.py', 'w') as f:
    f.write(cell_code)
```

**Run extracted code:**
```bash
uv run python cell_2.py
```

#### Method 5: Use Cell IDs (Jupyter Lab 3.0+)

Newer notebooks have cell IDs. You can target them programmatically:

```python
import nbformat

def execute_cell_by_id(notebook_path, cell_id):
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Find cell by ID
    for cell in nb.cells:
        if cell.get('id') == cell_id:
            # Extract and execute this cell
            print(f"Found cell: {cell_id}")
            print(cell['source'])
            return cell

    print(f"Cell {cell_id} not found")
    return None

# Usage
execute_cell_by_id('notebook.ipynb', 'cell-4')
```

#### Method 6: Run Cells in IPython

For quick testing without full notebook execution:

```bash
# Start IPython with notebook context
uv run ipython

# In IPython:
%load_ext autoreload
%autoreload 2

# Load and run cell code
%load notebook.ipynb  # Shows cell contents
# Copy/paste specific cell code and run
```

### Best Practices for Cell Execution

✅ **Do:**
- Run cells in order (top to bottom) for clean state
- Restart kernel before running all cells to verify independence
- Use cell tags to organize and identify important cells
- Comment cell purposes for clarity

❌ **Don't:**
- Run cells out of order and create hidden dependencies
- Rely on cell execution order that differs from top-to-bottom
- Mix notebook execution with external script modifications

### Typical Workflows

**Debugging a specific cell:**
```bash
# 1. Start Jupyter Lab
uv run jupyter lab

# 2. Navigate to notebook
# 3. Click the problematic cell
# 4. Press Shift+Enter to run
# 5. Fix issues
# 6. Restart Kernel & Run All Cells (to verify)
```

**Testing new code:**
```bash
# 1. Open notebook in Jupyter Lab
# 2. Insert new cell (press B in command mode)
# 3. Write code
# 4. Run with Shift+Enter
# 5. Iterate until working
# 6. Execute full notebook to verify
```

**Running specific analysis:**
```bash
# 1. Tag cells with "analysis" tag
# 2. Use interactive mode to run tagged cells
# 3. Or extract cells to separate script
# 4. Run script independently
```

### Running Python Scripts

If you create standalone Python scripts:

```bash
uv run python script_name.py
```

Run code directly:
```bash
uv run python -c "import pandas as pd; print(pd.__version__)"
```

### Converting Notebooks

**To Python script:**
```bash
uv run jupyter nbconvert --to python "notebook.ipynb"
```

**To HTML:**
```bash
uv run jupyter nbconvert --to html "notebook.ipynb"
```

**To PDF (requires LaTeX):**
```bash
uv run jupyter nbconvert --to pdf "notebook.ipynb"
```

## Dependency Management

### View Current Dependencies

```bash
uv pip list
```

### Add New Package

```bash
uv add package_name
```

Example:
```bash
uv add matplotlib
```

With version constraint:
```bash
uv add "matplotlib>=3.7.0"
```

### Remove Package

```bash
uv remove package_name
```

### Update All Dependencies

```bash
uv sync --upgrade
```

### View Dependency Tree

```bash
uv pip tree
```

## Development Workflow

### Typical Workflow

1. **Start fresh session:**
   ```bash
   uv sync
   uv run jupyter lab
   ```

2. **Work in notebooks** - Make changes, run cells interactively

3. **Test changes:**
   ```bash
   uv run jupyter nbconvert --to notebook --execute --inplace "exercise-1/L1 - Coding with Jupyter AI Lab.ipynb" --allow-errors
   ```

4. **Review outputs** - Check executed notebook for results

### Code Iteration Pattern

```bash
# Edit code in Jupyter Lab
# Save notebook (Cmd+S / Ctrl+S)

# Test execution
uv run jupyter nbconvert --to notebook --execute --inplace "notebook.ipynb"

# Review outputs
# Repeat as needed
```

## Data Files

### Exercise 1 Data

**customer_reviews.csv** - Sample dataset with customer reviews

Load in Python:
```python
import pandas as pd
df = pd.read_csv('data/customer_reviews.csv')
```

Fields typically include:
- Review text
- Ratings
- Product information
- Customer data

## API Usage

### OpenAI API

**Basic pattern:**
```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)

print(response.choices[0].message.content)
```

**Models available:**
- `gpt-4o-mini` - Fast, cost-effective
- `gpt-4o` - Most capable
- `gpt-4-turbo` - Balanced performance

### Open Library API

**Basic search:**
```python
import requests

response = requests.get(
    'https://openlibrary.org/search.json',
    params={
        'q': 'python programming',
        'limit': 5
    }
)
data = response.json()
```

**No API key required** - Open Library is free and public.

See `exercise-2/openlibrary_api_docs.md` for complete API documentation.

## Troubleshooting

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
uv sync
```

If specific package missing:
```bash
uv add package_name
```

### OpenAI API Key Issues

**Error:** `openai.AuthenticationError`

**Solutions:**
1. Check `.env` file exists in exercise directory
2. Verify API key is correct: `cat exercise-1/.env`
3. Ensure no extra spaces: `OPENAI_API_KEY=sk-...`
4. Restart Jupyter kernel after updating `.env`

### Jupyter Kernel Not Found

**Error:** Kernel not available

**Solution:**
```bash
uv add ipykernel
uv run python -m ipykernel install --user --name=jupyter-ai
```

### Notebook Execution Timeout

**Error:** `TimeoutError` during nbconvert

**Solution:** Increase timeout:
```bash
uv run jupyter nbconvert --to notebook --execute --inplace "notebook.ipynb" --ExecutePreprocessor.timeout=300
```

### Permission Denied on .env

**Error:** Cannot read `.env` file

**Solution:**
```bash
chmod 600 exercise-1/.env
```

### Requests Library Issues

**Error:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
uv add requests
uv sync
```

### Pandas DataFrame Errors

**Error:** Issues loading CSV

**Solutions:**
```python
# Check file exists
import os
print(os.path.exists('data/customer_reviews.csv'))

# Try with full path
df = pd.read_csv('exercise-1/data/customer_reviews.csv')

# Check encoding
df = pd.read_csv('data/customer_reviews.csv', encoding='utf-8')
```

## Best Practices

### Environment Variables

✅ **Do:**
- Use `.env` files for secrets
- Load with `python-dotenv`
- Keep `.env` in `.gitignore`

❌ **Don't:**
- Hard-code API keys in notebooks
- Commit `.env` files to git
- Share API keys in screenshots

### Notebook Organization

✅ **Do:**
- Use markdown cells for documentation
- Clear outputs before committing (optional)
- Use descriptive variable names
- Add comments for complex logic

❌ **Don't:**
- Run cells out of order
- Rely on global state
- Leave debug print statements

### Code Quality

✅ **Do:**
- Handle errors gracefully
- Validate API responses
- Use type hints where helpful
- Test with different inputs

❌ **Don't:**
- Ignore error messages
- Assume API always succeeds
- Skip edge cases

### Version Control

✅ **Do:**
- Commit working notebooks
- Use meaningful commit messages
- Keep `.gitignore` updated

❌ **Don't:**
- Commit `.env` files
- Commit `.venv/` directory
- Commit large data files (use `.gitignore`)

## Advanced Usage

### Running Specific Cells

Convert notebook to Python, then run specific functions:

```bash
uv run jupyter nbconvert --to python "notebook.ipynb"
uv run python -c "from notebook import my_function; my_function()"
```

### Batch Processing

Execute multiple notebooks:

```bash
for notebook in exercise-*/*.ipynb; do
    echo "Processing $notebook"
    uv run jupyter nbconvert --to notebook --execute --inplace "$notebook" --allow-errors
done
```

### Custom Jupyter Configuration

Create `jupyter_notebook_config.py`:

```python
c.NotebookApp.port = 8889
c.NotebookApp.open_browser = False
```

### Using Different OpenAI Models

Edit code in notebook:

```python
# Faster, cheaper
model = "gpt-4o-mini"

# More capable
model = "gpt-4o"

# Balanced
model = "gpt-4-turbo"

response = client.chat.completions.create(
    model=model,
    messages=[...]
)
```

## Additional Resources

### Documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [requests Documentation](https://requests.readthedocs.io/)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

### Course Materials
- [AISuite GitHub](https://github.com/andrewyng/aisuite)
- [Open Library API](https://openlibrary.org/developers/api)

### Tools
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Jupyter Lab](https://jupyterlab.readthedocs.io/)

## Getting Help

1. **Check this guide** for common issues
2. **Review course materials** in notebooks
3. **Check API documentation** for OpenAI and Open Library
4. **Verify environment setup** with `uv sync`
5. **Restart kernel** in Jupyter Lab (Kernel → Restart Kernel)

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `uv sync` |
| Start Jupyter Lab | `uv run jupyter lab` |
| Execute notebook | `uv run jupyter nbconvert --to notebook --execute --inplace "notebook.ipynb"` |
| Add package | `uv add package_name` |
| Remove package | `uv remove package_name` |
| List packages | `uv pip list` |
| Update all | `uv sync --upgrade` |
| Run Python script | `uv run python script.py` |
| Convert to Python | `uv run jupyter nbconvert --to python "notebook.ipynb"` |
| Convert to HTML | `uv run jupyter nbconvert --to html "notebook.ipynb"` |

---

**Happy coding with AI! 🚀**
