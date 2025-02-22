FROM python:3.8

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
