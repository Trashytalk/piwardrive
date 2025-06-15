R Integration
-------------

``scripts/health_summary.R`` reads a CSV or JSON file of
``HealthRecord`` rows. The function ``health_summary`` returns averages
for CPU temperature, usage and more, and optionally saves a CPU
temperature plot.

Enable this optional feature by installing the ``rpy2`` package and the
R libraries ``ggplot2`` and ``jsonlite``::

   pip install rpy2
   sudo apt install r-base
   Rscript -e "install.packages(c('ggplot2','jsonlite'), repos='https://cloud.r-project.org')"

Use :func:`r_integration.health_summary` to invoke the R code from
Python.
