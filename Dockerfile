FROM public.ecr.aws/lambda/python:3.11

# Copiar dependencias e instalar
COPY requirements_lambda.txt .
RUN pip install -r requirements_lambda.txt --no-cache-dir

# Copiar código fuente
COPY lambda_handler.py   ${LAMBDA_TASK_ROOT}/
COPY src/                ${LAMBDA_TASK_ROOT}/src/
COPY config/             ${LAMBDA_TASK_ROOT}/config/
COPY scripts/            ${LAMBDA_TASK_ROOT}/scripts/

CMD ["lambda_handler.lambda_handler"]
