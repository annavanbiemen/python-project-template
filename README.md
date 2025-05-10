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

## Just recipes

Install [just](https://just.systems/man/en/packages.html) first.

Then invoke just to learn about available recipes:
```shell
$ just
Available recipes:
    sh     # Shell into venv (!! experimental !!)
    check  # Check code
    fix    # Fix code
    test   # Test for bugs
    behave # Test behaviour
    scan   # Scan for vulnerabilities
    run    # Run the app
```
