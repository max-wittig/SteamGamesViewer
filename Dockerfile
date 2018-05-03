FROM python:3

WORKDIR /opt/steam_games_viewer
RUN useradd -ms /bin/sh steamuser
RUN python3 -m venv venv
RUN chown -R steamuser:steamuser venv/

COPY requirements.txt .
RUN venv/bin/pip install --require-hashes -r requirements.txt

COPY . .
RUN chown -R steamuser:steamuser .

USER steamuser
EXPOSE 4000
ENTRYPOINT ["venv/bin/python3", "__main__.py"]
