# pullnrun

A simple python app for running a set of commands from remote sources and pushing result files to remote targets.

## Testing

For unittests and linting, run:

```bash
# Unittests
python3 -m unittest discover tst/

# Unittests with coverage
coverage run --source ./ --omit setup.py -m unittest discover tst/
coverage report -m

# Linting error check
pylint -E */

# Full linting output
pylint */
```
