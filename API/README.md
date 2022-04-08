# Airnominal API

## About

The Airnominal API is currently written in in Python using the [Flask](https://flask.palletsprojects.com/) micro web framework and [SQLAlchemy](https://www.sqlalchemy.org/) ORM. The server collects data from stations, stores them in a database and provides them to a frontend website, and allows registration, validation and management of the equipment.

## Installation

Airnominal API requires Python 3.10 or later, and [Poetry](https://python-poetry.org/) dependency manager.

You can clone this repository and install it using Poetry:

```bash
git clone github.com/ChristofferNorgaard/Airnominal.git
cd Airnominal/API
poetry install
```

This will download and install all required dependencies and add `airnominal` as command. Note that depending on your Poetry configuration, you might need to activate its virtual environment to use the command.

You will also need to install [one of SQLAlchemy dialects](https://docs.sqlalchemy.org/en/13/dialects/index.html) to use databases other than SQLite. The `mysql` and `pymysql` dialects are already specified as package extras.

## Usage

### Configuration

Airnominal API uses YAML file for configuration. Example file can be found at [`config.yaml.sample`](config.yaml.sample). Before running the API, you need to set the configuration file as the `AIRNOMINAL_CONFIG` environment variable.

### Running & Deployment

The development server can be started with `airnominal run`. It is based on the default Flask's built-in server and will respect all of its environment variables (except `FLASK_APP` which is configured automatically).

It is not recommended using this server in production. Instead, you should use any WSGI-compatible server. See [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/) for more details. Airnominal uses the app factory located at `Airnominal.create_app` to create the application.

### Documentation

The API documentation can be found [here](API-en.md).
