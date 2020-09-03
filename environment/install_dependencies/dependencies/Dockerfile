#Use is an official Python runtime, used as the parent image
FROM ubuntu
USER root
MAINTAINER varun "varun@ai-educate.com"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get install -y python-pip python-dev nginx build-essential && apt-get install -y libenchant1c2a && apt-get install -y gcc && apt-get install -y curl

#Install Java 8 for antlr 4
#RUN apt-get update
#RUN apt-get -y install software-properties-common
#RUN add-apt-repository -y ppa:webupd8team/java
#RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
#RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
#RUN apt-get -y update
#RUN apt-get -y install oracle-java8-installer
RUN apt-get install -y antlr4

#For setting timezone
RUN apt-get install -y tzdata
RUN echo "Europe/Stockholm" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

#Install python3
RUN apt-get install -y python3-tk
RUN apt-get -y install python3-pip

# set the working directory in the container to /app
WORKDIR /tutor

# add the install directory and requirements.txt file to the directory in /dee_learning_app for installing packages
ADD requirements.txt /tutor
ADD third-party-software /tutor/third-party-software

#Install all dependencies required by the project
RUN pip3 install -r requirements.txt

# Download spacy english model
RUN python3 -m spacy download en

#Install nameparaser required by latex2sympy
RUN pip3 install nameparser

# To install neuracoref package
RUN pip3 install Cython
WORKDIR third-party-software/neuralcoref
RUN pip3 install .
WORKDIR ../../

# To install latex2sympy
WORKDIR third-party-software/latex2sympy
RUN antlr4 PS.g4 -o gen
WORKDIR ../../

#To download all the nltk packages we need
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader conll2000
RUN python3 -m nltk.downloader averaged_perceptron_tagger

# Expose port 8080 for the Flask app to run on
EXPOSE 8080
# Expose port 27017 for connecting mongodb service or container
EXPOSE 27017

#All the environment variables go here.
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8 
ENV AI_TUTOR_DIR=/tutor/
ENV AI_TUTOR_MONGODB_PASSWORD=aitutordb
ENV ENABLE_SENETRY=FALSE
ENV AI_TUTOR_MONGODB_USERNAME=aitutor
ENV AI_TUTOR_FACEBOOK_APP_ID=56789678
ENV AI_TUTOR_FACEBOOK_SECRET_ID=gyhjkgfhvjb
ENV PYTHONPATH=./tutor:./tutor/third-party-software/latex2sympy/
ENV AI_TUTOR_FACEBOOK_APP_NAME=Educate
ENV GOOGLE_CAPTCHA_SECRET_KEY=6LdNiGoUAAAAAIsbLAPaVMHS_wxRoQKyQ-cSj6js
ENV SENDER_EMAIL_ID=somepassword@ai-educate.com
ENV SENDER_EMAIL_PASSWORD=somepassword
ENV AI_TUTOR_MONGODB_URL=host.docker.internal:27017/aitutordb
ENV AI_TUTOR_SENTRY_DSN=
ENV AI_TUTOR_GOOGLE_CLIENT_ID=TEST
ENV GOOGLE_CLIENT_ID=test

#WORKDIR tutor/
# execute the Flask app
#ENTRYPOINT ["python3"]
