FROM alpine

ARG CUSTOM_ARG=default

WORKDIR /app

RUN --mount=type=secret,id=SECRET_TOKEN \
    cp /run/secrets/SECRET_TOKEN secret.txt

RUN echo "${CUSTOM_ARG}" > build-arg.txt

CMD ["sh", "-c", "cat secret.txt && cat build-arg.txt"]
