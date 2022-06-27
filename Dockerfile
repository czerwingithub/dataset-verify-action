FROM python:3.8-slim

MKDIR /action
COPY entrypoint.sh /action/entrypoint.sh
ENTRYPOINT: '/action/entrypoint.sh'
