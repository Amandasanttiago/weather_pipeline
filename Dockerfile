FROM astrocrpublic.azurecr.io/runtime:3.1-13
USER root

RUN apt-get update && apt-get install -y git

USER astro


# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate

