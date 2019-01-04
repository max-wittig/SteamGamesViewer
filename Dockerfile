FROM python:3.7-alpine

WORKDIR /opt/steam_games_viewer
RUN adduser --disabled-password steamuser && \
    chown -R steamuser:steamuser /home/steamuser && \
    chown -R steamuser:steamuser /opt/steam_games_viewer && \
    pip install poetry

COPY --chown=steamuser:steamuser . .
USER steamuser
RUN poetry install -n

EXPOSE 4000
ENTRYPOINT ["poetry", "run", "web"]
