FROM amazonlinux:2
ENV WORKDIR=/opt/app
ENV NODE_VERSION=16.14.0
ENV PYTHON_VERSION=3.9.12
ENV NPM_VERSION=8.13.0
ENV YARN_VERSION=1.21.1
ENV AWSCLI_VERSION=1.18.219
ENV PYTHON_MINOR_VERSION=3.9

RUN yum -y update
RUN yum install -y wget tar xz git gcc-c++ make \
 libssl-dev zlib zlib1g-dev zlib-devel bzip2 bzip2-devel readline-devel \
 openssl-devel which libffi-devel java-1.8.0-openjdk.aarch64

WORKDIR ${WORKDIR}

RUN set -x; git clone https://github.com/anyenv/anyenv ${HOME}/.anyenv \
    && echo 'export PATH="$HOME/.anyenv/bin:$PATH"' >> ~/.bash_profile \
    && echo 'eval "$(anyenv init -)"' >> ~/.bash_profile

RUN ${HOME}/.anyenv/bin/anyenv install --force-init
SHELL ["/bin/bash", "-l", "-c"]
ENV PATH ${HOME}/.anyenv/bin:$PATH

RUN anyenv install nodenv && anyenv install pyenv

RUN nodenv install "${NODE_VERSION}" && nodenv local "${NODE_VERSION}"
RUN pyenv install "${PYTHON_VERSION}" && pyenv local "${PYTHON_VERSION}"
RUN set -ex; npm install -g "npm@${NPM_VERSION}" "yarn@${YARN_VERSION}"
RUN echo 'export LANG=C.UTF-8' >> ~/.bash_profile
RUN echo 'export LANGUAGE=en_US:' >> ~/.bash_profile
RUN echo 'export PYTHONPATH="${WORKDIR}:$PYTHONPATH"' >> ~/.bash_profile

ADD package.json package.json
RUN yarn init -y && yarn install
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 3000 8000