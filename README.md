# Singing Sands

> Live-code modular synthesis in Python using Pure Data.

Written by David Sim ([@davids48] (https://github.com/DavidS48))

Builds on pyata, authored by Jerônimo Barbosa ([@jeraman](https://github.com/jeraman)) and recovered by Jan Van Bruggen ([@JanCVanB](https://github.com/JanCVanB))
from https://code.google.com/archive/p/pyata

## Description

Singing Sands is a Python library for controlling the [Pure Data](http://puredata.info/) modular synthesis environment. It aims to provide a streamlined interface that's usable for live-coding and performance.

## Installation

### Prerequisites

* Python 3.6 or greater.
* PureData - I'm testing with 0.48.1 - other version may well work but I don't know.

### Linux

* Clone or download the repository to a directory, `pyata`.

```
cd pyata
python3.6 -m venv venv
source venv/bin/activate
cd pyata
pip install -e .
```

* Edit `pyata/properties.config` to set the location of your pd binary.
* `python ./scripts/make_a_noise.py`

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details.
