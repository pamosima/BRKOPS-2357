# Use the official Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install sudo
RUN apt-get update && apt-get install -y sudo

# Prepare the user environment
ARG USER=docker
RUN useradd -m $USER && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER && \
    chmod 0440 /etc/sudoers.d/$USER

# Switch to the new user
USER $USER

# Add local bin directory to PATH for user-installed packages
ENV PATH="$PATH:/home/$USER/.local/bin"

# Install necessary packages and clean up
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        openconnect && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Configure pip and install Python packages
RUN python3 -m pip config set global.break-system-packages true && \
    python3 -m pip install --user pyats[library] pyats.contrib pynetbox --upgrade

# Create pyats config directory and disable reporter to prevent Docker IPC issues
RUN mkdir -p /home/docker/.pyats && \
    echo "[reporter]" > /home/docker/.pyats/pyats.conf && \
    echo "enabled = false" >> /home/docker/.pyats/pyats.conf