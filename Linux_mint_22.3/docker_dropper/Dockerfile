FROM python:3.12

WORKDIR /src

COPY . /src

RUN python3 -m venv .venv && . .venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

