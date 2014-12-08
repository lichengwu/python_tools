__author__ = 'lichengwu'

# coding=utf8

import simplejson as json
import sys
import monitor
from sys import path

path.append("~/")


def union_all(_data, _delta):
    if not _data:
        _data = {}
    for k, v in _delta.items():
        if _data.has_key(k):
            _data[k] = _data[k] + v
        else:
            _data[k] = v
    return _data


def stat(_path, types, key):
    rs = {}
    for line in open(_path):
        line = line.replace("/\\n", '')
        line = line.replace("<br>", ',')
        raw_data = json.loads(line)
        for k in raw_data:
            if not key in k:
                continue
            for item in raw_data[k][2:-2].split(","):
                kv = item.split(":")
                if len(kv) == 2 and kv[0] in types:
                    if not rs.has_key(kv[0]):
                        rs[kv[0]] = int(kv[1])
                    else:
                        rs[kv[0]] += int(kv[1])

    return rs


if __name__ == "__main__":
    path = sys.argv[1]

    ow = stat(path, ["PUBLIC_FARE", "DISCOUNT_FARE", "DYNAMIC_POLICY",
                     "FARE_POLICY", "DEFAULT_POLICY"], "ow")
    rt = stat(path, ["PUBLIC_FARE", "DISCOUNT_FARE", "DYNAMIC_POLICY",
                     "FARE_POLICY", "DEFAULT_POLICY", "ROUND_DECREASE_POLICY"], "rt")
    b2b = stat(path, ["INTER_FARE"], "b")

    all_data = union_all(ow, rt)
    all_data = union_all(all_data, b2b)
    # change key
    data = {}
    for k, v in all_data.items():
        data["atw_data_" + k.lower()] = v
    # send to monitor
    monitor.put("data_collect", data)


