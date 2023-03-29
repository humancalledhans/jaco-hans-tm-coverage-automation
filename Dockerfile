FROM python:3.10.2-bullseye
# FROM python:3.9.0-alpine

COPY . .

ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg-agent \
#     software-properties-common \
#     libglib2.0-0=2.50.3-2 \
#     libnss3=2:3.26.2-1.1+deb9u1 \
#     libgconf-2-4=3.2.6-4+b1 \
#     libfontconfig1=2.11.0-6.7+b1

# RUN apt-get install -y libglib2.0-0=2.50.3-2 
# RUN apt-get install -y libnss3=2:3.26.2-1.1+deb9u1 
# RUN apt-get install -y libgconf-2-4=3.2.6-4+b1 
# RUN apt-get install -y libfontconfig1=2.11.0-6.7+b1

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

# # for alpine:
# RUN apk update && \
#     apk add install -y openjdk-11-jre-headless && \
#     apk add clean;

# this is the previous block that worked. the following three lines.
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# RUN mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
# RUN brew install
# RUN eval "$(homebrew/bin/brew shellenv)" \
#     brew update --force --quiet \
#     chmod -R go-w "$(brew --prefix)/share/zsh"

# tried the solution from the website https://gerg.dev/2021/06/making-chromedriver-and-chrome-versions-match-in-a-docker-image/

# RUN brew install google-chrome
RUN pip3 install selenium
RUN pip3 install webdriver_manager
RUN pip3 install Pillow
RUN pip3 install anticaptchaofficial
RUN pip3 install mysql-connector
RUN pip3 install pytz
RUN pip3 install thefuzz

CMD ["python3", "thread_asgn.py"]