import itertools
import os

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from .resolvers import types

# Register query resolvers and resolvers here.
schema = make_executable_schema(
    load_schema_from_path(os.path.dirname(__file__)),
    *list(itertools.chain(types)),
    *[],
    snake_case_fallback_resolvers,
)
