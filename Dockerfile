FROM public.ecr.aws/lambda/python:3.10

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

COPY lambda_requirements.txt .

RUN pip3 install -r lambda_requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [lambda_function.lambda_handler]