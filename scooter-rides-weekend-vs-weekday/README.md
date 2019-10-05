# Scooter Report Card
The goal of this analysis was to compare weekday and weekend scooter traffic.

## File Structure
The [Rlang] script (.R) is both a place to run / develop code and a report of the results.

The renv.lock file controls the Rlang dependencies (via [renv]).
This helps you ensure you have everything you need to run the code.

The other files are artifacts that derive from the script.

## Usage
The first time, you may need to install the Rlang dependencies with:
```
renv::init()
```
This will only work if you have [renv] installed.

To start the script, run:
```
Rscript scooter-report-card.ipynb
```

[Rlang]: https://www.r-project.org/
[renv]: https://rstudio.github.io/renv/index.html
