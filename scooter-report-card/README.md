# Scooter Report Card
![Scooter Company Usage Report Card]

The goal of this analysis was to gather basic summary statistics on each scooter company.

To see the results, go straight to the [![Scooter Company Usage Report Card]][report].

## File Structure
The [jupyter] notebook (.ipynb) is both a place to run / develop code and a report of the results.

`Pipfile` and `Pipfile.lock` control the pythn dependencies (via [pipenv]).
This is helps you ensure you have everything you need to run the code.

The other files are artifacts that derive from the notebook.

## Usage
The first time, you may need to install the python dependencies with:
```
pipenv install
```
This will only work if you have [pipenv] installed.
Or you can use your own python package manager to install the requirements in the `Pipfile`.

To start the notebook, run:
```
pipenv run jupyter notebook scooter-report-card.ipynb
```

## Saving Changes
Whenever you make changes to the notebook, please download a python (.py) version of it.
This is more useful in source control since it just shows the code (without formatting or results).
If you don't want to click and drag to move it from your downloads, you can run:
```
pipenv run jupyter nbconvert --to python *.ipynb
```
Please run the same command with `html` (in place of `python`).


[jupyter]: https://jupyter.org/index.html
[pipenv]: https://pipenv-fork.readthedocs.io/en/latest/
[report]: ./scooter-report-card.html
[Scooter Company Usage Report Card]: ./scooter-report-card.png
