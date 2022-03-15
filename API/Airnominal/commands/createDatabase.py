from flask import current_app
from flask.cli import with_appcontext

from ..database import Base
from ..utils import session_scope, with_transaction
print(current_app)
Base.metadata.create_all(current_app.airnominal.engine)
