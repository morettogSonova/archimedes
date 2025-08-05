# archimedes
archimedes project

## Project Structure

```text
.
├── data
│   ├── in                 Input data directory
│   └── out                Output data directory (normalized to our format)
├── exploratory.ipynb      Jupyter notebook for exploratory data analysis
├── poetry.lock
├── pyproject.toml         Project configuration file
├── README.md              This file
└── scripts                Transformations and data loading scripts
```

## Setup

Install Poetry if you haven't already:

```bash
pipx install poetry
```

Then, install the project dependencies:

```bash
poetry install
```

And activate the virtual environment:

```bash
eval $(poetry env activate)
```