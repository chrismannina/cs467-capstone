#!/bin/bash

set -e

venv_dir="myenv"
requirements_file="requirements.txt"

GREEN='\033[0;32m'
NC='\033[0m' # No Color

function create_venv() {
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv "$venv_dir"
}

function activate_venv() {
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source "$venv_dir/bin/activate"
}

function install_requirements() {
    if [ -f "$requirements_file" ]; then
        echo -e "${GREEN}Checking for new requirements...${NC}"
        pip freeze > installed.txt
        while IFS= read -r line
        do
            package=${line%%=*}
            if ! grep -q "^$package==" installed.txt; then
                echo -e "${GREEN}Installing new package: $package${NC}"
                if ! pip install "$package"; then
                    echo -e "${GREEN}Failed to install $package.${NC}"
                    exit 1
                fi
            fi
        done < "$requirements_file"
        rm installed.txt
    else
        echo -e "${GREEN}Requirements file not found. Skipping installation.${NC}"
    fi
}

# Check if virtual environment directory exists
if [ -d "$venv_dir" ]; then
    # Check if virtual environment is already activated
    if [[ $VIRTUAL_ENV != *"$venv_dir"* ]]; then
        # Activate the virtual environment
        activate_venv
    fi
else
    # Create a virtual environment
    create_venv

    # Activate the virtual environment
    activate_venv
fi

# Install requirements
install_requirements
