# syntax=docker/dockerfile:1
FROM node:20-slim
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY server.js .
EXPOSE 7000
CMD ["npm", "start"]
