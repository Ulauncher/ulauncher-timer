# Timer Extension


<img aligh="center" src="http://i.imgur.com/bc2bzZ8.png">

## Basic usage

### Time formats

The timer extension accepts times in two formats:

- Time duration in hours, minutes, and/or seconds
- Time of day (absolute time in the next 24 hours)

#### Examples

##### Time duration
- `3m` = 3 minutes
- `5h` = 5 hours
- `2m30s` = 2 minutes and 30 seconds

##### Time of day
- `1:30pm` = 1:30 PM
- `720a` = 7:20 AM

### Persistent timer mode

Choose _Alert periodically until closed_ in settings to make timers harder to
ignore. Close the timer notification to stop persistent timer notifications.

## Running tests

Setup

```sh
git clone https://github.com/Ulauncher/Ulauncher
ULAUNCHER_PTH=$(python -c 'import site; print(site.getsitepackages()[0])')/ulauncher.pth
realpath Ulauncher > $ULAUNCHER_PTH

pip install websocket-client python-Levenshtein
pip install pytest pytest-pep8 freezegun
```

Run tests

```sh
pytest
```
