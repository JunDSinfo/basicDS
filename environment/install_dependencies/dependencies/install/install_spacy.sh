# This script installs spacy with appropriate dependencies for Python 3
sudo python3 -m pip install spacy
sudo python3 -m spacy download en
python3 -m spacy download en_core_web_sm-2.0.0 --direct