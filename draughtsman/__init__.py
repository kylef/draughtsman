from cffi import FFI
from refract.json import LegacyJSONDeserialiser
from refract.contrib.apielements import registry, ParseResult


_all_ = ('parse',)


ffi = FFI()
ffi.cdef('''
typedef enum {
    DRAFTER_SERIALIZE_YAML = 0,
    DRAFTER_SERIALIZE_JSON
} drafter_format;

typedef struct {
    bool sourcemap;
    drafter_format format;
} drafter_options;

int drafter_parse_blueprint_to(const char* source,
                               char** out, const drafter_options options);
''')

drafter = ffi.dlopen('drafter')


def parse(blueprint: str) -> ParseResult:
    source = ffi.new('char []', blueprint.encode('utf-8'))
    output = ffi.new('char **')
    options = ffi.new("drafter_options *", [False, 1])
    result = drafter.drafter_parse_blueprint_to(source, output, options[0])

    if result != 0:
        raise Exception('Unknown Error')

    string = ffi.string(output[0]).decode('utf-8')
    deserialiser = LegacyJSONDeserialiser(registry=registry)
    return deserialiser.deserialise(string)
