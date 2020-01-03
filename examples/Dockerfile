FROM python:3-alpine

ENV BROWSER=headlesschrome
ENV BROWSER_OPTIONS='add_argument("--no-sandbox"); add_argument("--disable-gpu")'

RUN apk add chromium chromium-chromedriver
RUN pip install pullnrun boto3 robotframework robotframework-seleniumlibrary

WORKDIR /workspace
ENTRYPOINT ["pullnrun"]
CMD ["--env"]
