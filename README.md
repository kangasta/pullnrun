# pullnrun

[![Build Status](https://travis-ci.org/kangasta/pullnrun.svg?branch=master)](https://travis-ci.org/kangasta/pullnrun)
[![Maintainability](https://api.codeclimate.com/v1/badges/7198c6ec9229ca477164/maintainability)](https://codeclimate.com/github/kangasta/pullnrun/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7198c6ec9229ca477164/test_coverage)](https://codeclimate.com/github/kangasta/pullnrun/test_coverage)

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
