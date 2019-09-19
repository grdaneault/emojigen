FROM node:11.7.0-alpine

WORKDIR /code/

RUN npm install -g http-server && \
    adduser -h /code -D emojigen

COPY package*.json ./

RUN npm install

COPY . .

RUN  npm run build

EXPOSE 8080
CMD [ "http-server", "build" ]