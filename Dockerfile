ARG BASE_IMAGE_BUILDER=python:3.11-alpine
ARG BASE_IMAGE_APP=alpine:3


FROM ${BASE_IMAGE_BUILDER} as builder

RUN apk add --no-cache binutils gcc libffi-dev  make cmake g++ zlib-dev \
    && pip install --disable-pip-version-check --no-cache-dir pyinstaller wheel

WORKDIR /src

COPY requirements.txt .

RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY app.py .

RUN pyinstaller -F app.py


FROM ${BASE_IMAGE_APP} as bin

USER 1000

WORKDIR /app

COPY --from=builder /src/dist/app ./

ENTRYPOINT [ "/app/app" ]
