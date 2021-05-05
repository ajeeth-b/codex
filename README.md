# codex

## Installation

#### Software requirements
- Python 3.8
- Docker

#### Steps
- Install python packages from **requirements.txt**.
- Start the docker service.
- Building docker image for code executor.
  - You can find a directory **[../code/Dockerfile/](https://github.com/ajeeth-b/codex/tree/main/codex/Dockerfile)** with sub directory naming the supported languages.
  - In each sub dir there is dockefile.
  - ** NEED TO BUILD THEM WITH PROPER TAG NAME ** for application to access containers.
  - Build each image with tag name ```lang-< language name >```. (language name is the sub dir name).
    - currently supporting two language and their commands.
      - [/home/codex/Dockerfile/python3$](https://github.com/ajeeth-b/codex/tree/main/codex/Dockerfile/python3) ```sudo docker build -t lang-python3 .``` .
      - [/home/codex/Dockerfile/c$](https://github.com/ajeeth-b/codex/tree/main/codex/Dockerfile/c) ```sudo docker build -t lang-c .``` .
- updating application configuration file at **[../codex/app/config.py](https://github.com/ajeeth-b/codex/blob/main/codex/app/config.py)**
  - __UNFORGE_URL__ should point to the main unforge application.
  - __UNFORGE_KEY__ this key should be same as the __TESTCASE_API_KEY__ in the unforge config.

- from **run.py** you can find a variable name pointing to app pointing to flask applicaiton. use the vaible for deploying with application server.
