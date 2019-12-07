# pullnrun

A simple python app for running a set of commands from remote sources and pushing result files to remote targets.

## Installing

Ensure that you are using Python >= 3.6 with `python --version`. To install, run:

```bash
pip install pullnrun
```

## Usage

### Examples

See [examples](./examples) for usage examples.

## Testing

For unittests and linting, run:

```bash
# Unittests
python3 -m unittest discover tst/

# Unittests with coverage
coverage run --source ./ --omit setup.py,tst/* -m unittest discover tst/
coverage report -m

# Linting error check
pylint -E */

# Full linting output
pylint */
```
