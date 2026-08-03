FROM alpine:3
ARG TEST_BUILD_ARG
RUN test "$TEST_BUILD_ARG" = "expected-value" || (echo "TEST_BUILD_ARG not passed" && exit 1)
