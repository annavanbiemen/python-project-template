# App

## Run using uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

Then run:
```shell
uv run app
```

## Run using Docker

Install [docker](https://docs.docker.com/get-started/get-docker/) first.

Then build, run and cleanup:
```shell
docker build --tag app .  # Build the image
docker run --rm app       # Run the app
docker rmi app            # Remove the image
```
