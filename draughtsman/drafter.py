from ctypes.util import find_library
from cffi import FFI
from semantic_version import Version

ffi = FFI()
ffi.cdef('''
const char* drafter_version_string(void);
''')

drafter_library = find_library('drafter')
if not drafter_library:
    raise ImportError('Draughtsman require drafter to be installed')

drafter = ffi.dlopen(drafter_library)


def get_drafter_version():
    output = drafter.drafter_version_string()
    string = ffi.string(output).decode('utf-8')
    return string.replace('v', '')


def drafter4_parse_blueprint_to(blueprint: str,
                                generate_source_map: bool = False) -> str:
    source = ffi.new('char []', blueprint.encode('utf-8'))
    output = ffi.new('char **')
    parse_options = ffi.new('drafter_parse_options *', [False])
    serialize_options = ffi.new(
        'drafter_serialize_options *',
        [generate_source_map, 1]
    )

    result = drafter.drafter_parse_blueprint_to(
        source,
        output,
        parse_options[0],
        serialize_options[0]
    )

    if result != 0:
        raise Exception('Unknown Error')

    string = ffi.string(output[0]).decode('utf-8')
    return string


def drafter5_parse_blueprint_to(blueprint: str,
                                generate_source_map: bool = False) -> str:
    source = ffi.new('char []', blueprint.encode('utf-8'))
    output = ffi.new('char **')

    serialize_options = drafter.drafter_init_serialize_options()
    drafter.drafter_set_format(serialize_options, 1)

    if generate_source_map:
        drafter.drafter_set_sourcemaps_included(serialize_options)

    try:
        result = drafter.drafter_parse_blueprint_to(
            source,
            output,
            ffi.NULL,
            serialize_options
        )
    finally:
        drafter.drafter_free_serialize_options(serialize_options)

    if result != 0:
        raise Exception('Unknown Error')

    string = ffi.string(output[0]).decode('utf-8')
    return string


drafter_version = Version(get_drafter_version())
if drafter_version.major == 4:
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

    drafter_parse_blueprint_to = drafter4_parse_blueprint_to
elif drafter_version.major == 5:
    ffi.cdef('''
    typedef enum
    {
        DRAFTER_OK = 0,
        DRAFTER_EUNKNOWN = -1,
        DRAFTER_EINVALID_INPUT = -2,
        DRAFTER_EINVALID_OUTPUT = -3,
    } drafter_error;

    typedef struct drafter_parse_options drafter_parse_options;
    typedef struct drafter_serialize_options drafter_serialize_options;

    drafter_serialize_options* drafter_init_serialize_options();
    typedef enum {
        DRAFTER_SERIALIZE_YAML = 0,
        DRAFTER_SERIALIZE_JSON
    } drafter_format;
    void drafter_set_format(drafter_serialize_options*, drafter_format);
    void drafter_set_sourcemaps_included(drafter_serialize_options*);
    void drafter_free_serialize_options(drafter_serialize_options*);

    drafter_error drafter_parse_blueprint_to(const char* source,
        char** out,
        const drafter_parse_options* parse_opts,
        const drafter_serialize_options* serialize_opts);
    ''')

    drafter_parse_blueprint_to = drafter5_parse_blueprint_to
else:
    raise ImportError(
        'Unsupported version of drafter (found {}), '
        'Draughtsman requires drafter >= 4.0.0,<5'.format(drafter_version))
