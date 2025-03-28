#!/bin/bash
# Install dependencies for the Django application

echo "Installing dependencies..."

# Activate the virtual environment (if available)
if [ -d "/var/app/venv/staging-LQM1lest" ]; then
    source /var/app/venv/staging-LQM1lest/bin/activate
fi

# Ensure pip is up-to-date
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r /var/app/current/requirements.txt

echo "Dependencies installed successfully."
