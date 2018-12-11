import sys

from log.log import MLog


def sysExit(reason):
    MLog.error(u"baseUtil exitWith: exit Application , reason is " + reason)
    sys.exit(reason)
