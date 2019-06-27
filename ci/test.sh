#!/usr/bin/env bash

# Exit when any command fails
set -e

# Download Miniconda if necessary
mkdir -p downloads
if [ ! -f downloads/miniconda.sh ]
then
  if [ $TRAVIS_OS_NAME = "osx" ]
  then
    fname=Miniconda3-latest-MacOSX-x86_64.sh
  else
    fname=Miniconda3-latest-Linux-x86_64.sh
  fi
  wget https://repo.continuum.io/miniconda/$fname -q -O downloads/miniconda.sh
fi

# Install and update Miniconda
MINICONDA_PATH=$HOME/miniconda
chmod +x downloads/miniconda.sh && ./downloads/miniconda.sh -b -p $MINICONDA_PATH
export PATH=$MINICONDA_PATH/bin:$PATH
conda update --yes conda

# Create and activate a test environment
PYTHON_VERSION=$1
conda create --yes --name testenv python=$PYTHON_VERSION
source activate testenv

# Install dependencies required for testing
python setup.py develop
pip install -e ".[dev]"
pip install codecov

# Run tests and coverage
pytest --cov=creme
codecov
