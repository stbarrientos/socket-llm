FROM python:3.9

WORKDIR /usr/llm/app

COPY ./requirements.txt /usr/llm/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /usr/llm/requirements.txt

CMD [ "python", "app.py" ]