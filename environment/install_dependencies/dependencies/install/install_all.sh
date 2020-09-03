#!/usr/bin/env bash
# Installs all dependencies in Python 3
sudo apt install python3-pip
sudo pip3 install --upgrade pip
sudo apt-get install python3.5-dev
sudo apt-get install python3-tk
sudo apt-get install nginx
sudo python3 -m pip install numpy scipy matplotlib ipython jupyter pandas xlrd sympy nose unidecode passlib Flask-Social pytz jsonpickle requests
sudo pip3 install https://github.com/sbook/flask-mongoengine/tarball/master
sudo pip3 install http://github.com/pythonforfacebook/facebook-sdk/tarball/master
sudo pip3 install urllib3
sudo pip3 install oauth2client google-api-python-client
sudo pip3 install social-auth-app-flask-mongoengine
sudo pip3 install imblearn
sudo pip3 install pyenchant
sudo pip3 install pydrive
sudo pip3 install pathlib
sudo pip3 install cachetools
sudo pip3 install locustio
sudo pip3 install textacy
sudo pip install python-dateutil
sudo pip3 install urlparse
sudo pip3 install nameparser
sudo pip3 install python-crontab
sudo pip3 install --upgrade google-auth-oauthlib
sudo pip3 install_flask.sh
sudo pip3 install inflect configparser
sudo pip3 install gunicorn
sudo pip3 install supervisor
sudo pip3 install --upgrade google-auth
sudo pip3 install multiprocessing
pip install pyyaml ua-parser user-agents
pip install --upgrade sentry-sdk[flask]==0.4.0
sudo python3 -m pip install boto --upgrade
sudo pip3 install hearstPatterns==0.1.3
alias python=python3
sudo sh install_neuralcoref.sh
sudo sh install_sympy.sh
sudo sh install_latex2sympy.sh
sudo sh install_theano.sh
sudo sh install_pytorch.sh
sudo sh install_gensim.sh
sudo sh install_nltk.sh
sudo sh install_spacy.sh
sudo sh install_flask.sh
echo ""
echo ""
echo ""
echo "Recommended: Set environment variable 'AI_TUTOR_DIR' inside '~/.bashrc'"
echo "Recommended: Add 'alias python=python3' inside '~/.bashrc'"
echo "Recommended: Follow instructions in 'install_kenlm.txt' to install kenlm"
echo ""
echo "Beginning download of Google Drive files... Please allow sufficient time for this process to complete"
sudo sh download_google_drive_files.sh
