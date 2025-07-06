# Python Project

This is a standard Python project following best practices:
- Uses a virtual environment
- Dependencies listed in `requirements.txt`
- Source code in `src/`
- Tests in `tests/`

## Setup

1. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - Windows (PowerShell):
     ```sh
     .venv\Scripts\Activate.ps1
     ```
   - Windows (cmd):
     ```sh
     .venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Project

```sh
python src/main.py
```

## Running Tests

```sh
pytest
```
