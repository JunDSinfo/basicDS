# https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927 #  Importing the Public Key
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list # Create source list file MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org
systemctl daemon-reload
systemctl start mongod
systemctl enable mongod

sudo python3 -m pip install pymongo==3.6.0