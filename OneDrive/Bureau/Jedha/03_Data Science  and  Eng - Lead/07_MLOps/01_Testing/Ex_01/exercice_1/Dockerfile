FROM python:3.10
WORKDIR /home
COPY . .

RUN pip install -r requirements.txt
ENV PYTHONPATH=/home
CMD ["-m", "pytest", "tests/"]