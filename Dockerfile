FROM python:3.8-slim

RUN mkdir /action
COPY remove_empty_args_and_invoke.sh /action/remove_empty_args_and_invoke.sh
RUN chmod a+x /action/remove_empty_args_and_invoke.sh
ENTRYPOINT "/action/remove_empty_args_and_invoke.sh"
