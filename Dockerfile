FROM python:3.7-slim as base

# inspired from https://sourcery.ai/blog/python-docker/

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN apt-get update \
    && apt-get install -y less \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# create user account, and create user home dir
RUN useradd -ms /bin/bash pi_runner

WORKDIR /home/pi_runner
# cp source files
RUN mkdir /home/pi_runner/src
COPY src /home/pi_runner/src/

RUN pip install --upgrade pip

RUN pip install -r src/pi_walk_slope/requirements.txt

RUN pip install -e src/pi_walk_slope

# set the user as owner of the copied files.
RUN chown -R pi_runner:pi_runner /home/pi_runner/

USER pi_runner
WORKDIR /home/pi_runner
