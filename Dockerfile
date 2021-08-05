FROM estnltk/estnltk-notebook

USER nobody

COPY ./server.py ./server.py

CMD ["python", "-u", "server.py"]
