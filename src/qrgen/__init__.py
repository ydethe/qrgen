# -*- coding: utf-8 -*-
"""

.. include:: ../../README.md

# Testing

## Run the tests

To run tests, just run:

    pdm run pytest

## Test reports

[See test report](../tests/report.html)



[See coverage](../coverage/index.html)

.. include:: ../../CHANGELOG.md

"""
import logging

import logfire
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    secret_key: str
    logfire_token: str
    loglevel: str


settings = Settings()

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("qrgen_logger")
logger.setLevel(settings.loglevel.upper())

logfire.configure(token=settings.logfire_token)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("fireset_logger")
logger.setLevel(settings.loglevel.upper())
logger.addHandler(logfire.LogfireLoggingHandler())
