FROM python:alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

# RUN apk --no-cache add python3 \
#                        build-base \
#                        python3-dev \
#                        # wget dependency
#                        openssl \
#                        # dev dependencies
#                        git \
#                        bash \
#                        sudo \
#                        py3-pip \
#                        # Pillow dependencies
#                        jpeg-dev \
#                        zlib-dev \
#                        freetype-dev \
#                        lcms2-dev \
#                        openjpeg-dev \
#                        tiff-dev \
#                        tk-dev \
#                        tcl-dev \
#                        harfbuzz-dev \
#                        fribidi-dev \
#                        # tesseract-ocr dependencies
#                        tesseract-ocr-dev

# RUN apk add libexif udev chromium chromium-chromedriver
RUN pip install -r requirements.txt

CMD gunicorn app:app --error-logfile gunicorn_error.log -b 0.0.0.0:8080 --thread 5
