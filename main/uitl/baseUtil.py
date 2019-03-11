import json
import sys

from log.log import MLog


def sysExit(reason):
    MLog.error(u"baseUtil exitWith: exit Application , reason is " + reason)
    sys.exit(reason)


def utf8(file_name):
    return file_name.decode('utf-8')


def list2str(list):
    return str(list).decode('unicode-escape')


def write_json(json_data, json_file_name):
    fileObject = open(json_file_name, 'w')
    fileObject.write(json.dumps(json_data, ensure_ascii=False).decode('utf8'))
    fileObject.close()


def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data
