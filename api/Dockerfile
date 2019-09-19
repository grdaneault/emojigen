FROM python:3-alpine

WORKDIR /code/

RUN apk --no-cache add python3-dev \
                       build-base \
                       openssl \
                       # Pillow dependencies
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev


ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .

EXPOSE 5000
CMD ./entrypoint.sh
