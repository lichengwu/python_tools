__author__ = 'lichengwu'

# coding=utf8

import simplejson as json
import sys
import re


def union_all(data, deta):
    if not data:
        data = {}
    for k in deta:
        if data.get(k):
            if int(k) == -1:
                data[k] = max((int(data[k]), int(deta[k])))
            else:
                data[k] = int(data[k]) + int(deta[k])
        else:
            data[k] = int(deta[k])
    return data


def select_entity(rs, entity, type):
    data = entity.get(type)
    if data:
        rs[type] = union_all(rs.get(type), data)


def stat(path, types, key):
    rs = {}
    for line in open(path):
        line = line.replace("/\\n", '')
        data = json.loads(line)
        for k in data:
            if not key in k:
                continue
            entity = json.loads(data[k])
            for type in types:
                select_entity(rs, entity, type)

    output = "<table border='1'><tr><td>Entity</td><td>*</td>"

    for group in xrange(0, 65):
        output += "<td>" + str(group) + "</td>"
    output += "</td>"
    line = ""
    for k in rs:
        line += "<tr><td>" + k + "</td>"
        for group in xrange(-1, 65):
            line += "<td>" + strConv(rs[k].get(str(group))) + "</td>"
        line += "</tr>"

    return output + line + "</table>"


def strConv(s):
    s = str(s)
    while True:
        (s, count) = re.subn(r"(\d)(\d{3})((:?,\d\d\d)*)$", r"\1,\2\3", s)
        if count == 0: break
    return s


if __name__ == "__main__":
    path = sys.argv[1]
    print "<h2>B2C Group<h2>"
    print stat(path,
               ["PUBLIC_FARE", "DISCOUNT_FARE", "DYNAMIC_POLICY",
                "FARE_POLICY", "DEFAULT_POLICY"], "ow")
    print "<h2>B2B Group<h2>"
    print stat(path,
               ["PUBLIC_FARE", "DEFAULT_POLICY", "INTER_FARE",
                "DISCOUNT_FARE"], "b")
    print "<h2>RT Group<h2>"
    print stat(path,
               ["PUBLIC_FARE", "DISCOUNT_FARE", "DYNAMIC_POLICY",
                "FARE_POLICY", "DEFAULT_POLICY", "ROUND_DECREASE_POLICY"], "rt")
