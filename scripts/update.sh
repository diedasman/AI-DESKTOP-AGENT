#!/bin/bash

echo "Updating CUE..."

git pull

source venv/bin/activate

pip install -r requirements.txt

echo "Update complete."