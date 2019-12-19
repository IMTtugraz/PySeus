#Download base image python buster
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive 
ENV DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt-get update

RUN apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-tk && \
    apt-get install -y libsm6 libxext6 libxrender-dev &&\
    apt-get install -y git &&\
    apt-get install -y ibgl1-mesa-glx

ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT 50000
RUN useradd -d "$JENKINS_HOME" -u 971 -m -s /bin/bash jenkins
VOLUME /var/jenkins_home

RUN ls -lah /var/jenkins_home

ENV PATH="/var/jenkins_home/.local:${PATH}"

RUN pip3 install cython &&\
    pip3 install pytest &&\
    pip3 install pytest-cov &&\
    pip3 install pylint &&\
    pip3 install pylint_junit

