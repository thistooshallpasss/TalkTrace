#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Download NLTK data into a local project folder
python -c "import nltk; nltk.download('vader_lexicon', download_dir='./nltk_data')"