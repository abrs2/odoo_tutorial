FROM odoo:14.0
ARG PYTHON_VERSION=3.8.5

### Setup python:{version} ###
# helpful links:
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
# https://github.com/pyenv/pyenv/blob/32922007863c4a54feca2a95226c8307cfdfea3d/plugins/python-build/README.md
# https://github.com/pyenv/pyenv/issues/990
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        curl \
        git \
        libbz2-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        llvm \
        make \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev \
        tkinter

# Python defaults to ASCII encoding. Switch to UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer \
    | bash
ENV PATH=$HOME/.pyenv/bin:$PATH
RUN git clone git://github.com/pyenv/pyenv.git /tmp/pyenv && \
    cd /tmp/pyenv/plugins/python-build && \
    ./install.sh && \
    rm -rf /tmp/pyenv

RUN python-build $PYTHON_VERSION /usr/local/

# Install pip (conditionally), then install pipenv
RUN if command pip >/dev/null 2>&1; then \
        echo "pip already installed. Skipping manual installation."; \
    else \
        echo "Installing pip manually"; \
        curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
            chmod 755 /tmp/get-pip.py && \
            /tmp/get-pip.py && \
            rm /tmp/get-pip.py; \
    fi
RUN pip install pipenv
