from .base import Base, engine, Session  # noqa: F401
from .department import Department  # noqa: F401
from .user import User  # noqa: F401
from .client import Client  # noqa: F401
from .contract import Contract  # noqa: F401
from .event import Event  # noqa: F401

Base.metadata.create_all(engine)
