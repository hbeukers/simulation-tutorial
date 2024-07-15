To make this repo you need rye [installed](https://rye.astral.sh/guide/installation/).

To make the repo run install rye and clone the repo.
Go to the repo folder and run:

```shell
rye sync
```
 
This should be enough to set everything up, including python version.


The repo was set up using the following commands:

Go to the folder were you have your repositories

```shell
rye init simulation_tutorial
```

To install the wanted packages 
```shell
rye add jupyter
rye add numpy
rye add xarray
rye add matplotlib
rye add multiprocess
rye add tqdm
```

Change python version
```shell
rye pin 3.11
rye sync
```

Add the following line to pyproject.toml such that the project becomes an editable install and we can import modules from our own repository.
```toml
[tool.rye.workspace]
```

Add the following lines to pyproject.toml to also format jupyter notebooks, directly fix linting issues and also sort the imports
```toml
[tool.ruff]
extend-include = ["*.ipynb"]
fix = true

[tool.ruff.lint]
select = ["I"]
```




