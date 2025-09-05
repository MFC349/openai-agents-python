# Visual Studio Development Setup

This document provides instructions for developing the OpenAI Agents Python SDK using Microsoft Visual Studio.

## Prerequisites

1. **Visual Studio 2019 or later** with Python development workload installed
2. **Python 3.9 or later** (Python 3.12 recommended)
3. **uv** package manager (will be installed automatically or manually)
4. **Git** for version control

## Getting Started

### 1. Open the Project

1. Open Visual Studio
2. Choose "Open a project or solution"
3. Navigate to the repository folder and select `openai-agents-python.sln`

### 2. Set Up Python Environment

The project uses `uv` as the package manager. If you don't have it installed:

```bash
pip install uv
```

Then sync the project dependencies:

```bash
uv sync --all-extras --all-packages --group dev
```

### 3. Configure Python Interpreter

1. In Visual Studio, go to **Tools** > **Options** > **Python** > **Environments**
2. Select the virtual environment created by uv (typically in `.venv` folder)
3. Or add a new environment pointing to your Python 3.12 installation

## Development Workflow

### Code Formatting and Linting

The project uses `ruff` for formatting and linting. You can run these commands in the Terminal within Visual Studio:

```bash
# Format code
uv run ruff format

# Check for linting issues
uv run ruff check

# Fix auto-fixable linting issues
uv run ruff check --fix
```

### Type Checking

```bash
uv run mypy . --exclude site
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest -s -k test_name
```

### Building Documentation

```bash
uv run mkdocs build
```

## Git Integration

Visual Studio has built-in Git support. You can:

1. **View changes**: Use the **Git Changes** window (View > Git Changes)
2. **Commit changes**: Stage files and write commit messages in the Git Changes window
3. **Push/Pull**: Use the Git menu or the Git Changes window toolbar
4. **Branch management**: Use the branch selector in the status bar

### Recommended Git Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests and linting: `uv run pytest && uv run ruff check && uv run mypy .`
4. Commit your changes using Visual Studio's Git integration
5. Push your branch and create a pull request

## Project Structure

- `src/agents/` - Main source code
- `tests/` - Test files
- `examples/` - Example usage code
- `docs/` - Documentation source files
- `.vscode/` - VS Code configuration (if you switch between editors)
- `.editorconfig` - Cross-editor formatting configuration

## Troubleshooting

### uv not found

If Visual Studio can't find `uv`, ensure it's in your PATH or install it via pip:

```bash
pip install uv
```

### Python Environment Issues

1. Check that Python 3.9+ is installed
2. Verify that the virtual environment is activated
3. Re-run `uv sync` to ensure all dependencies are installed

### Git Authentication

If you have issues with Git authentication:

1. Configure your Git credentials: `git config --global user.name "Your Name"`
2. Set up SSH keys or use a personal access token for HTTPS
3. Use Visual Studio's credential manager for seamless authentication

## Additional Resources

- [Main development guide](AGENTS.md)
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Visual Studio Python Development](https://docs.microsoft.com/en-us/visualstudio/python/)