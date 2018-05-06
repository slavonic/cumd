# cumd

Church Slavonic Markdown Dialect

## Usage
```
pip install cumd

cumd -h

cumd input.md output.html
```

## Developing and testing

```
virtualenv .venv -p python3

. .venv/bin/activate

pip install -r requirements.txt pytest pylint

pytest .
pylint .
```
