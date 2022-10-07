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


## Explaining some decisions
1. Why devcontainers/docker? A: To standardize dev environments and avoid clutter.
2. Why SQLite? A: To make development faster and simpler. Django's ORM should allow us to switch DBs without major issues.
3. Why didn't you create models for area, address, nationality and basic stuff that might repeat itself a lot? A: Again, to make things simpler based on the scope of this project.
4. Why didn't you use helpful libraries such as DRF or attrs? A: Given the short life of this project, I'd like to avoid cluttering it with magic libraries.
5. Why didn't you create more services to manipulate models/simplify the views.py file? A: Basically for the same reason I didn't import useful libraries. To avoid clutter and to keep it simple.

There are a lot of things that could be improved. Classes could have some useful methods to avoid repetitive functions, magical numbers and strings could be avoided with constants, etc. What truly matters to me is that we have a good test coverage that should allow us to implement these improvements.
