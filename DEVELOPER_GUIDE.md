# Developer Guide

This guide provides command line instructions for working with projects in this DeepLearning.AI Courses repository.

## Prerequisites

- **Python 3.13+** installed
- **uv** package manager installed ([installation guide](https://github.com/astral-sh/uv))

## Project Structure

This repository contains multiple course directories, each with its own dependencies:

```
DeepLearning-AI-Courses/
├── agentic-ai/
├── acp-agent-communication-protocol/
├── claude-code-a-highly-agentic-coding-assistant/
└── jupyter-ai-coding-in-notebooks/
```

Each project directory contains:
- `pyproject.toml` - Project dependencies and configuration
- `uv.lock` - Locked dependency versions
- `.venv/` - Virtual environment (auto-created, not in git)

## Getting Started

### 1. Initial Setup

Navigate to the specific course directory you want to work with:

```bash
cd jupyter-ai-coding-in-notebooks
```

Install dependencies and create virtual environment:

```bash
uv sync
```

This command:
- Creates a `.venv/` directory in the project folder
- Installs all dependencies from `pyproject.toml`
- Locks dependency versions in `uv.lock`

### 2. Verify Installation

Check Python version:

```bash
uv run python --version
```

List installed packages:

```bash
uv pip list
```

## Running Projects

### Python Scripts

Run any Python script using:

```bash
uv run python script_name.py
```

Or run Python code directly:

```bash
uv run python -c "print('Hello, World!')"
```

### Jupyter Notebooks

#### Execute Notebooks Programmatically

Run a notebook and save results back to the file:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace "notebook_name.ipynb"
```

With extended timeout and error handling:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace "notebook_name.ipynb" --ExecutePreprocessor.timeout=120 --allow-errors
```

#### Start Jupyter Lab

Launch interactive Jupyter Lab server:

```bash
uv run jupyter lab
```

This opens Jupyter Lab in your browser at `http://localhost:8888`

#### Start Jupyter Notebook (Classic)

```bash
uv run jupyter notebook
```

### Convert Notebooks

Convert notebook to Python script:

```bash
uv run jupyter nbconvert --to python "notebook_name.ipynb"
```

Convert to HTML:

```bash
uv run jupyter nbconvert --to html "notebook_name.ipynb"
```

## Managing Dependencies

### Add a New Dependency

```bash
uv add package_name
```

Example:

```bash
uv add requests
```

Add with version constraint:

```bash
uv add "requests>=2.31.0"
```

### Remove a Dependency

```bash
uv remove package_name
```

### Update Dependencies

Update all dependencies to latest compatible versions:

```bash
uv sync --upgrade
```

Update specific package:

```bash
uv add "package_name@latest"
```

### View Dependency Tree

```bash
uv pip tree
```

## Project-Specific Instructions

### jupyter-ai-coding-in-notebooks

This course teaches AI-assisted coding in Jupyter notebooks using OpenAI's API.

#### Setup Environment Variables

Create a `.env` file in the exercise directory:

```bash
cd exercise-1
touch .env
```

Add your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

#### Run Exercise Notebooks

```bash
# Navigate to project root
cd jupyter-ai-coding-in-notebooks

# Execute Exercise 1
uv run jupyter nbconvert --to notebook --execute --inplace "exercise-1/L1 - Coding with Jupyter AI Lab.ipynb" --ExecutePreprocessor.timeout=120 --allow-errors

# Execute Exercise 2
uv run jupyter nbconvert --to notebook --execute --inplace "exercise-2/L2 - Book Research Assistant.ipynb" --ExecutePreprocessor.timeout=120 --allow-errors
```

#### Dependencies

- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `ipykernel>=6.0.0` - Jupyter kernel
- `pandas>=2.0.0` - Data analysis
- `nbformat>=5.0.0` - Notebook format
- `nbconvert>=7.0.0` - Notebook conversion
- `requests>=2.31.0` - HTTP library

### agentic-ai

Organized into modules with Python examples demonstrating agentic AI patterns.

```bash
cd agentic-ai
uv sync
uv run python module_name/example.py
```

### acp-agent-communication-protocol

Labs demonstrating agent communication using the ACP protocol.

```bash
cd acp-agent-communication-protocol
uv sync

# Run server example
uv run python server.py

# Run client example (in another terminal)
uv run python client.py
```

## Common Commands Reference

### uv Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install dependencies and create virtual environment |
| `uv add <package>` | Add a new dependency |
| `uv remove <package>` | Remove a dependency |
| `uv run <command>` | Run command in virtual environment |
| `uv pip list` | List installed packages |
| `uv pip tree` | Show dependency tree |
| `uv sync --upgrade` | Update all dependencies |

### Jupyter Commands

| Command | Description |
|---------|-------------|
| `uv run jupyter lab` | Start Jupyter Lab server |
| `uv run jupyter notebook` | Start Jupyter Notebook (classic) |
| `uv run jupyter nbconvert --to notebook --execute --inplace <file>` | Execute notebook |
| `uv run jupyter nbconvert --to python <file>` | Convert to Python script |
| `uv run jupyter nbconvert --to html <file>` | Convert to HTML |

## Troubleshooting

### Module Not Found Error

If you get `ModuleNotFoundError`, ensure dependencies are installed:

```bash
uv sync
```

### Wrong Python Version

Check Python version:

```bash
uv run python --version
```

If incorrect, ensure you have Python 3.13+ installed and uv is configured correctly.

### Virtual Environment Issues

Remove and recreate virtual environment:

```bash
rm -rf .venv
uv sync
```

### Jupyter Kernel Not Found

Install/reinstall ipykernel:

```bash
uv add ipykernel
uv run python -m ipykernel install --user --name=jupyter-ai-coding
```

### Notebook Execution Timeout

Increase timeout value:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace "notebook.ipynb" --ExecutePreprocessor.timeout=300
```

## Best Practices

1. **Always use `uv run`** - Ensures commands run in the correct virtual environment
2. **Sync after pulling** - Run `uv sync` after pulling updates to ensure dependencies are current
3. **Don't commit `.venv/`** - Virtual environment is already in `.gitignore`
4. **Use relative paths** - Keep notebooks and scripts portable
5. **Document dependencies** - Update `pyproject.toml` when adding new requirements

## Additional Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [Python 3.13 Documentation](https://docs.python.org/3.13/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
