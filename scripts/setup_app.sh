#!/bin/bash

apt update
apt upgrade -y
apt autoremove -y

# Install dependencies
apt install -y gnupg2 curl dialog apt-utils build-essential libssl-dev libffi-dev python3-dev

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update -y

ACCEPT_EULA=Y apt-get install -y msodbcsql17
ACCEPT_EULA=Y apt-get install -y mssql-tools

echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

# Optional: For unixODBC development headers and kerberos library for debian-slim distributions
apt-get install -y unixodbc-dev libgssapi-krb5-2

# Setup Poetry
poetry config virtualenvs.create false
poetry install $(test "$APP_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
