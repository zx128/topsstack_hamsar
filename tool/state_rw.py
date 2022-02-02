import os
import sys

import json

INDENT = 2

WORK_DIR_PATH = "."

STATE_FILE_NAME = "_state.json"

def read(name):
    filePath = os.path.join(WORK_DIR_PATH, STATE_FILE_NAME)
    try:
        with open(filePath, 'r') as fin:
            d = json.load(fin)
    except Exception as e:
        raise Exception('unable to read file: %s' % e)
    return d[name]

def write(name, value):
    filePath = os.path.join(WORK_DIR_PATH, STATE_FILE_NAME)
    try:
        with open(filePath, 'r') as fin:
            d = json.load(fin)
    except Exception as e:
        raise Exception('unable to read file: %s' % e)
    d[name] = value
    try:
        with open(filePath, 'w') as fout:
            json.dump(d, fout, indent=INDENT)
        return
    except Exception as e:
        raise Exception('unable to write file: %s' % e)


def main():
    if len(sys.argv) not in [3, 4]:
        print("Usage: (read name|write name value)")
        sys.exit(1)

    action = sys.argv[1]
    name = sys.argv[2]
    value = None
    if len(sys.argv) == 4:
        value = sys.argv[3]

    if action == "read":
        # not this!
        #print(json.dumps(read(name), indent=INDENT))
        print(read(name))
        return

    if action == "write":
        write(name, value)
        return

    print("Unknown action {}".format(action))
    sys.exit(1)


if __name__ == "__main__":
    main()
