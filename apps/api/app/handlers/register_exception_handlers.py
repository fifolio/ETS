from appwrite.exception import AppwriteException
from fastapi import FastAPI

from app.exceptions.configuration_error import ConfigurationError
from app.exceptions.cv_validation_error import CVValidationError
from app.handlers.appwrite_error_handler import appwrite_error_handler
from app.handlers.configuration_error_handler import configuration_error_handler
from app.handlers.cv_validation_error_handler import cv_validation_error_handler


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ConfigurationError, configuration_error_handler)
    app.add_exception_handler(AppwriteException, appwrite_error_handler)
    app.add_exception_handler(CVValidationError, cv_validation_error_handler)
