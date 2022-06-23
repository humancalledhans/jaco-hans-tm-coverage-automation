FROM python:3.10.2-bullseye

COPY . .

# RUN apt-get update -y
# # We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
# RUN apt-get install -y wget xvfb unzip
# # Set up the Chrome PPA
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# # Update the package list and install chrome
# RUN apt-get update -y
# RUN apt-get install -y google-chrome-stable
# # Set up Chromedriver Environment variables
# ENV CHROMEDRIVER_VERSION 97.0.4692.71
# ENV CHROMEDRIVER_DIR /chromedriver
# RUN mkdir $CHROMEDRIVER_DIR
# # Download and install Chromedriver
# RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
# RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
# # Put Chromedriver into the PATH
# ENV PATH $CHROMEDRIVER_DIR:$PATH

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

RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# RUN mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
# RUN brew install
# RUN eval "$(homebrew/bin/brew shellenv)" \
#     brew update --force --quiet \
#     chmod -R go-w "$(brew --prefix)/share/zsh"

# RUN brew install google-chrome
RUN pip3 install selenium
RUN pip3 install webdriver_manager
RUN pip3 install Pillow
RUN pip3 install anticaptchaofficial
RUN pip3 install mysql-connector

CMD ["python3", "thread_asgn.py"]