sudo python3 -m pip install flask flask-compress Flask-SSLify pyopenssl Flask-Social
sudo python3 -m pip install https://github.com/sbook/flask-mongoengine/tarball/master
sudo python3 -m pip install social-auth-app-flask-mongoengine
echo "Modify '/usr/local/lib/python3.5/dist-packages/flask_oauth.py' such that 'from urlparse import urljoin' -> 'from urllib.parse import urljoin'"
