from ctypes.util import find_library
from cffi import FFI
from semantic_version import Version
from refract.json import JSONDeserialiser
from refract.contrib.apielements import registry, ParseResult
from draughtsman.drafter import drafter_parse_blueprint_to


__all__ = ('parse',)


def parse(blueprint: str) -> ParseResult:
    result = drafter_parse_blueprint_to(blueprint)

    deserialiser = JSONDeserialiser(registry=registry)
    return deserialiser.deserialise(result)
