# Pyllow
This subdirectory contains the source code for implementing PoLP enforcement in Python-based frameworks. The approach consists of two parts:
- *callgraph*: PyCG, a tool generates the call graphs of Python scripts.
- *hook*: Audithook, a Python API that monitors the application’s behavior at the function-call level.

## Usage

This will generate a callgraph for the test directory in output file.
```bash
pip install flask
python __main__.py --package flask ./test.py -o output
```