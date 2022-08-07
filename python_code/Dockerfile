FROM public.ecr.aws/lambda/python:3.8

ARG FUNCTION_DIR

# Copy function code
# COPY app/* ${FUNCTION_DIR}
COPY requirements.txt  .
COPY * .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR ${FUNCTION_DIR}

CMD [ "app.handler" ]
# CMD [ "./app.py" ]
