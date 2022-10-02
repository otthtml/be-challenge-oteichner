## How to run this app?
1. Run the devcontainer
2. Inside the devcontainer, run `make run` to get the dev server up.

## How do I test this app?
1. Run the devcontainer
2. Inside the devcontainer, run `make test` to run all unit tests.

## How do I run the devcontainer?
Multiple ways.
- Easiest way is to use the "Remote Containers" extension from VSCode.
- You can also build the image with `docker build -t devcontainer -f .devcontainer/Dockerfile .` and run the container with `docker run -v ${PWD}:/workspaces -w /workspaces -it devcontainer bash`