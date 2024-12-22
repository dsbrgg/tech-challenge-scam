FROM node:18

RUN apt-get update && apt-get install -y strace inotify-tools tcpdump

WORKDIR /usr/src/app

COPY script.js .
COPY package.json .

RUN npm install --legacy-peer-deps

ENTRYPOINT ["bash"]
