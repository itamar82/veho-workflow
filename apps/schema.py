import itertools
import os

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from .resolvers import types
from .resolvers.scalars import datetime_scalar

# Register query resolvers and resolvers here.
schema = make_executable_schema(
    load_schema_from_path(os.path.dirname(__file__)),
    *list(itertools.chain(types)),
    *[datetime_scalar],
    snake_case_fallback_resolvers,
)
