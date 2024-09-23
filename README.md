# How to start

To make this repo you need uv [installed](https://docs.astral.sh/uv/getting-started/installation/).
This was tested with uv version 0.4.12.

To make the repo run install uv and clone the repo.
Go to the repo folder and run:

```shell
uv sync
```

This should be enough to set everything up, including python version.

For running specific commands in the virtual environment use:

```shell
uv run <command>
```

The tutorial notebook is located in the notebooks folder.

It works very well to run this repo in VS Code.
Using the jupyter extensions allows you to run the notebooks within VS code.

# How this repo was set up

The repo was set up using the following commands:

Go to the folder were you have your repositories

```shell
uv init simulation_tutorial
```

To install the wanted packages 
```shell
uv add jupyter
uv add numpy
uv add xarray
uv add matplotlib
uv add multiprocess
uv add tqdm
```

Change python version
```shell
uv pin 3.12
uv sync
```

Add the following line to pyproject.toml such that the project becomes an editable install and we can import modules from our own repository.
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/simulation_tutorial"]
```

Add the following lines to pyproject.toml to also format jupyter notebooks, directly fix linting issues and also sort the imports
```toml
[tool.ruff]
extend-include = ["*.ipynb"]
fix = true

[tool.ruff.lint]
select = ["I"]
```