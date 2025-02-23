# How to clone this repo

Go in your terminal to the folder where you want to clone the repo and run

```shell
git clone https://github.com/hbeukers/simulation-tutorial.git
```

# How to start

To use this repo you need `uv` [installed](https://docs.astral.sh/uv/getting-started/installation/).

Go to the repo folder and run:

```shell
uv sync
```

This should be enough to set everything up, including python version.

For running specific commands in the virtual environment use:

```shell
uv run <command>
```

The tutorial notebooks are located in the notebooks folder.

For VS Code: Using the jupyter extensions allows you to run the notebooks within VS code using this virtual enviroment.

# How this repo was set up

The repo was set up using the following commands:

Go to the folder were you have your repositories

```shell
uv init simulation-tutorial 
```

To install the wanted packages 
```shell
uv add xarray[io, parallel, viz]
uv add multiprocess
uv add tqdm
uv add jupyter
uv add qutip
uv add lmfit
```

Change python version
```shell
uv python pin 3.13
uv sync
```

Add the following lines to `pyproject.toml` such that the project becomes an editable install and we can import modules from our own repository.
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/simulation_tutorial"]
```

Add the following lines to `pyproject.toml` to also format jupyter notebooks, directly fix linting issues and also sort the imports
```toml
[tool.ruff]
extend-include = ["*.ipynb"]
fix = true

[tool.ruff.lint]
select = ["I"]
```