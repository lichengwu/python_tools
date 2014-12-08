__author__ = 'lichengwu'
# encoding=utf8

import sys
import simplejson as json

if __name__ == '__main__':
    path = sys.argv[1]
    # path = "/Users/lichengwu/tmp/aa.log"
    print "path:%s" % path

    data = {}

    for line in open(path):
        try:
            start = line.find("{")
            if start < 0 or 'TYPE' not in line:
                continue
            str = line[start:]
            str = str.replace(":{", ':"{')
            str = str.replace("},", '}",')
            msg = json.loads(str)
            entity = msg['entity']
            op = msg['operation']
            op_info = data.get(entity)
            if not op_info:
                op_info = {}
                data[entity] = op_info
            if op_info.has_key(op):
                op_info[op] = op_info[op] + 1
            else:
                op_info[op] = 1
        except Exception, e:
            print str
            print line
    print data
