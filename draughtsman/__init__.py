from refract.json import JSONDeserialiser
from refract.contrib.apielements import registry, ParseResult
from draughtsman.drafter import drafter_parse_blueprint_to


__all__ = ('parse',)


def parse(blueprint: str, generate_source_map: bool = False) -> ParseResult:
    result = drafter_parse_blueprint_to(
        blueprint,
        generate_source_map=generate_source_map
    )

    deserialiser = JSONDeserialiser(registry=registry)
    return deserialiser.deserialise(result)
