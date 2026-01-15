FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

#get seleniumbase deps
RUN apt install -y xvfb python3-tk python3-dev


#get chrome
RUN apt install -y --no-install-recommends wget && \
    wget -O /tmp/google-chrome.deb \
      https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y /tmp/google-chrome.deb && \
    rm -rf /var/lib/apt/lists/* /tmp/google-chrome.deb

#get python packages
RUN pip install seleniumbase confluent-kafka jsonschema


#setup filesystem
WORKDIR /app
COPY "./src" .
COPY "./" .

#run
ENTRYPOINT ["python", "tasks/amazon_get_search_results.py","4k television"]
