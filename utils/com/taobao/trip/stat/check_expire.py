__author__ = 'lichengwu'

import simplejson as json
import time
import sys

if __name__ == "__main__":
    path = sys.argv[2]
    type = str(sys.argv[1])
    total = 0
    expired = 0
    now = int(time.time()) * 1000

    for line in open(path + type + ".atw"):
        total += 1
        if total % 9999 == 0:
            print "process:%s,\texpired:%s" % (str(total), str(expired))
        data_object = json.loads(line)
        if type == "discount_fare":
            if int(data_object['segments'][0]['travelDateEnd']) < now:
                expired += 1
        elif type == "fare_policy":
            if int(data_object['travelDateEnd']) < now or int(data_object['endDate']) < now:
                expired += 1
        else:
            print 'unsupported type:%s' % type
            break

    print "total:%s" % str(total)
    print "expired:%s" % str(expired)





