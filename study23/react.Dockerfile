FROM node:24.13.0

WORKDIR /workspace
COPY ./frontend /workspace

RUN npm i

EXPOSE 5173
