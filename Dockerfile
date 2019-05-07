FROM python:3-alpine

RUN apk update && apk add libpq
RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD . .

RUN pip install --no-cache-dir -r requirements.txt

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps