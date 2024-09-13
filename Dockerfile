FROM python:3.11

WORKDIR /code

COPY src/samdul06food/main.py /code/

#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir --upgrade git+https://github.com/Nicou11/samdul06food.git@0.2.0/aws

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
