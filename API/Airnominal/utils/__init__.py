from contextlib import contextmanager
from unittest.mock import Mock

from ..database import Session
from flask import Blueprint, render_template, abort, Flask, request, jsonify, make_response

@contextmanager
def session_scope():
    """Wrap SQLAlchemy session into `with` block."""

    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create(session, model, **kwargs):
    """Get or create a new SQLAlchemy model."""

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False

    instance = model(**kwargs)
    session.add(instance)
    session.flush()
    return instance, True

def with_transaction(pass_transaction=False, **kwargs):
    """
    Wrap the function inside the Sentry transaction if the Sentry
    is installed, otherwise return transaction stub/mock.
    :param bool pass_transaction: Should the transaction be passes to wrapped function?
    :return: The function decorator
    """

    def _transaction_decorator(function):
        def _transaction_wrapper(*fargs, **fkwargs):
            if pass_transaction:
                fkwargs["transaction"] = Mock()
            return function(*fargs, **fkwargs)

    return _transaction_decorator

def returnError(error):
    response = make_response(
                jsonify(
                {
                    "success": False,
                    "error" : error
                }
            ),
            400,
        )
    response.headers["Content-Type"] = "application/json"
    return response