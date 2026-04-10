FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Atualiza os pacotes e instala o FontForge e seus bindings para Python
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends fontforge python3-fontforge \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*