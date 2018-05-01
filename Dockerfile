FROM python:3

WORKDIR /opt/steam_games_viewer
RUN useradd -ms /bin/sh steamuser
RUN python3 -m venv venv
RUN chown -R steamuser:steamuser venv/
USER steamuser

COPY --chown=steamuser:steamuser requirements.txt .
RUN venv/bin/pip install --require-hashes -r requirements.txt

COPY --chown=steamuser:steamuser . .

EXPOSE 4000
ENTRYPOINT ["venv/bin/python3", "__main__.py"]
