#!/bin/bash

# Step 1: Update the README
python update_readme.py

# Step 2: Commit and push changes
git add .
git commit -m "New update"
git push origin -u main
