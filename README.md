# Timer Extension


<img aligh="center" src="http://i.imgur.com/bc2bzZ8.png">


## Running tests

Setup

```sh
git clone https://github.com/Ulauncher/Ulauncher
ULAUNCHER_PTH=$(python -c 'import site; print(site.getsitepackages()[0])')/ulauncher.pth
realpath Ulauncher > $ULAUNCHER_PTH

pip install websocket-client python-Levenshtein
pip install pytest pytest-pep8
```

Run tests

```sh
pytest
```
