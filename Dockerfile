FROM node:18

RUN apt-get update && apt-get install -y strace inotify-tools tcpdump telnet

WORKDIR /usr/src/app

COPY tech-vantage/script.js .
COPY tech-vantage/package.json .

COPY cryptolope/search.min.js .

RUN npm install --legacy-peer-deps

ENTRYPOINT ["bash"]
