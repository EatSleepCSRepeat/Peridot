import sys
import os
import shlex
import re

varid = {}
sys.argv = sys.argv[1:]
if len(sys.argv) >= 1:
    try:
        sys.argv[0] = str(sys.argv[0])
    except Exception as e:
        print("?error: " + str(e).lower())
        sys.exit(1)
    
    if os.path.exists(sys.argv[0]):
        with open(sys.argv[0], 'r') as f:
            for line in f.readlines():
                line = line.strip()
                match shlex.split(line)[0]:
                    case 'display':
                        if len(shlex.split(line)) >= 1:
                            try:
                                print(shlex.split(line)[1])
                            except Exception as e:
                                print("?error: " + str(e).lower())
                    # this will be the ONLY function for now, in like 1 days there will be more
                    case _:
                        print("?error: unknown statement or variable " + line.split(' ')[0])
                        sys.exit(1)

    else:
        print("?error: file selected does not exist")
        sys.exit(1)
