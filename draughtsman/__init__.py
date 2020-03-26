from ctypes.util import find_library
from cffi import FFI
from refract.json import JSONDeserialiser
from refract.contrib.apielements import registry, ParseResult


_all_ = ('parse',)


ffi = FFI()
ffi.cdef('''
typedef enum {
    DRAFTER_SERIALIZE_YAML = 0,
    DRAFTER_SERIALIZE_JSON
} drafter_format;

typedef struct {
    bool requireBlueprintName;
} drafter_parse_options;

typedef struct {
    bool sourcemap;
    drafter_format format;
} drafter_serialize_options;

typedef enum
{
    DRAFTER_OK = 0,
    DRAFTER_EUNKNOWN = -1,
    DRAFTER_EINVALID_INPUT = -2,
    DRAFTER_EINVALID_OUTPUT = -3,
} drafter_error;

drafter_error drafter_parse_blueprint_to(const char* source,
    char** out,
    const drafter_parse_options parse_opts,
    const drafter_serialize_options serialize_opts);
''')
drafter = ffi.dlopen(find_library('drafter'))


def parse(blueprint: str) -> ParseResult:
    source = ffi.new('char []', blueprint.encode('utf-8'))
    output = ffi.new('char **')
    parse_options = ffi.new("drafter_parse_options *", [False])
    serialize_options = ffi.new('drafter_serialize_options *', [False, 1])

    result = drafter.drafter_parse_blueprint_to(
        source,
        output,
        parse_options[0],
        serialize_options[0]
    )

    if result != 0:
        raise Exception('Unknown Error')

    string = ffi.string(output[0]).decode('utf-8')
    deserialiser = JSONDeserialiser(registry=registry)
    return deserialiser.deserialise(string)
