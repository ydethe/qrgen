# sudo docker build -t ydethe/qrgen:latest .
# sudo docker push ydethe/qrgen:latest
FROM python:3.10-alpine

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /code
COPY dist/*.whl /code
RUN pip install /code/*.whl
EXPOSE 3566
CMD ["sh", "-c", "waitress-serve --host=0.0.0.0 --port 3566 --call 'qrgen.server:create_app'"]
