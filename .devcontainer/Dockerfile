# Start from basic ubuntu base image
FROM ubuntu

# Update packages
RUN apt update
RUN apt upgrade -y

# Add software
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install graphviz -y

# Add user for vscode
RUN useradd -ms /bin/bash vscode

# Install python dependencies
COPY .devcontainer/requirements.txt /tmp/pip-tmp/
RUN pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Fix TensorFlow-IO quirks
RUN python3 -m pip --quiet install --upgrade pip setuptools wheel
RUN python3 -m pip --quiet install --upgrade 'tensorflow-io[tensorflow]==0.31.0'
