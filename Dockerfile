FROM python:3.8-slim

RUN mkdir /action
COPY entrypoint.sh /action/entrypoint.sh
ENTRYPOINT "/action/entrypoint.sh"
