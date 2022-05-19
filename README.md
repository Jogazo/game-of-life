# GAME OF LIFE

This repository contains a game of life implementation in Python. It is intended to run on Posix compliant systems which have the required system packages.

## Required system packages:
- `python 3.8 or higher`, f-strings are being used, so lower python versions will not work.
- `pip3`

## Install guide
Note: following steps are written for Ubuntu, but feel free to edit for your distro of choice.
- `pip3 install virtualenvwrapper` and append the following to your .bashrc file 
`export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'`
`export PATH=$PATH:~/.local/bin` 
`source virtualenvwrapper.sh`
- git clone the repository
- Inside the git project: `mkvirtualenv game-of-life --python=/usr/bin/python3`
- `add2virtualenv .` (this makes the current path the root of your virtualenv)
- `pip3 install -r requirements.txt`

## Coding guide lines
All python code should follow the [PEP-8](https://www.python.org/dev/peps/pep-0008/) standard. Therefore please make a symbolic link from `pre-commit.sh` to `.git/hooks/pre-commit` or make sure that this functionallity is in your pre-commit hook.
