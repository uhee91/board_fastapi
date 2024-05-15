FROM python:3.12.0

COPY . /board_fastapi

WORKDIR /board_fastapi

RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile
    # && pipenv sync \
    # && pipenv install --ignore-pipfile