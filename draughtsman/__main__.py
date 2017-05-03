import sys
import code

from draughtsman import parse


if len(sys.argv) != 2:
    print('Usage: {} <file>'.format(sys.argv[0]))
    exit(0)


with open(sys.argv[1]) as fp:
    parse_result = parse(fp.read())

banner = '>>> parse_result\n{}'.format(repr(parse_result))
code.interact(banner=banner, local={'parse_result': parse_result})
