# How to get started

### Clone repository

Go in your terminal to the folder where you want to clone the repo and run

```shell
git clone https://github.com/hbeukers/simulation-tutorial.git
```

### Install and sync `uv`

To use this repo you need `uv` [installed](https://docs.astral.sh/uv/getting-started/installation/).

Go to the repo folder and run:

```shell
uv sync
```

This should be enough to set everything up, including python version.

### Run Jupyter notebooks

Use one of the following methods to run the notebooks in the notebooks folder:

##### VS Code
Install the Jupyter extension. Open the notebook in VS Code and select as kernel `.venv`. Now you can run the notebooks in VS Code.

##### Jupyter server
You can also start a jupyter server in the more traditional way by working in the browser. Run the following command in the folder of the repository.

# How this repo was set up

The repo was set up using the following commands:

Go to the folder were you have your repositories

```shell
uv init simulation-tutorial --lib
```

To install the wanted packages 
```shell
uv add xarray[io, parallel, viz]
uv add multiprocess
uv add tqdm
uv add jupyter
uv add qutip
uv add lmfit
uv add ruff --dev
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

Add the following lines to `pyproject.toml` to  make sure `ruff` also formats jupyter notebooks, directly fixes linting issues and also sorts the imports
```toml
[tool.ruff]
extend-include = ["*.ipynb"]
fix = true

[tool.ruff.lint]
select = ["I"]
```

You can format the code with
```shell
uv run ruff format
```
and lint using
```shell
uv run ruff check
```