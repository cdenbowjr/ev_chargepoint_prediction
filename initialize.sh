#!/bin/sh
echo "Running poetry installation script"
pip install poetry==1.8.3
poetry -V
pip install ipykernel jupyter_events
poetry config virtualenvs.in-project true
poetry add ipykernel jupyter_events
poetry install
project_name=$(grep -Po 'name \= \"\K[^\"]+' pyproject.toml | head -n 1)
echo $project_name "kernel name will be used"
poetry run python -m ipykernel install --user --name=$project_name
