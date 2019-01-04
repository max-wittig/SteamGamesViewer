# SteamGamesViewer

## docker image

```bash
  export STEAM_API_KEY=********
```

```bash
  docker run -e STEAM_API_KEY=$STEAM_API_KEY -p 4000:4000 maxwittig/steamgamesviewer
```

## installation

> [Poetry](https://github.com/sdispater/poetry) is required

```bash
poetry install
```

## usage

* Set steam API key environment variable
  ```bash
  export STEAM_API_KEY=*********
  ```

* Start the server
  ```bash
  poetry run web
  ```

* Goto localhost:4000 to see the result
  
## result

![image](https://user-images.githubusercontent.com/6639323/39488769-8b398d0c-4d83-11e8-8616-d966af25331e.png)

