# Project Archimedes

[Project Archimedes Hackathon](https://hackathon.truewealth.ch/) by [Truwealth AG](https://www.truewealth.ch/).

Creating a framework that analyzes historical patterns to predict future economic trends. Leverage coding skills and analytical thinking to transform historical data into actionable insights, ultimately building a tool that can help navigate complex economic currents. This event isn't just about competition — it's about collaborating to build something meaningful that bridges the gap between historical analysis and future forecasting.

We draw inspiration from Ray Dalios's [Principles for Dealing with the Changing World Order](https://www.economicprinciples.org/the-changing-world-order/), aiming to create a tool that can help understand and predict big economic cycles.

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