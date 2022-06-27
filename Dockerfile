FROM python:3.8-slim

ENV SCALYR_TOOL_SHA="89b82fd1a761674c9b8e36f7268dea1e9a7d80db"
RUN mkdir /action

COPY remove_empty_args_and_invoke.sh /action/
COPY dataset_verify.py /action/
ADD https://https://raw.githubusercontent.com/scalyr/scalyr-tool/{$SCALYR_TOOL_SHA}/scalyr /action/scalyr

RUN chmod a+x /action/remove_empty_args_and_invoke.sh
RUN chmod a+x /action/dataset_verify.py
RUN chmod a+x /action/scalyr


ENTRYPOINT "/action/remove_empty_args_and_invoke.sh"
