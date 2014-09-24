#!/usr/bin/python
__author__ = 'lichengwu'

import datetime
import os


def collect(_date):
    stat = {}
    metric_path = "/home/admin/at/logs/metric.log.%s" % _date
    for line in open(metric_path):
        if "chosenFlightStat" in line:
            kv = line.split(",")
            if len(kv) < 3:
                continue
            kv = kv[2:]
            for p in kv:
                er = p.strip().split("=")
                if len(er) != 2:
                    continue
                k = er[0]
                v = er[1]
                if not stat.has_key(k) or int(v) > stat[k]:
                    stat[k] = int(v)

    for k, v in stat.items():
        print "%s=%s" % (k, v)


def sum(_date):
    col = {"PARAM_CITY_CODE": "CITY_CODE_ERROR", "PARAM_AGENT_ID": "NO_AGENT_ID",
           "PARAM_AGENT_CITY": "AGENT_CITY_ERROR",
           "PARAM_TRIP_TYPE": "TRIPTYPE_ERROR", "PARAM_PASSENGER_NUM": "PASSENGER_NUM_ERROR",
           "PARAM_NO_BUSS": "BUSS_ERROR",
           "PARAM_NO_B2G_USER_INFO": "PARAM_NO_B2G_USER_INFO", "PARAM_NO_SEGMENT": "PARAM_NO_SEGMENT",
           "PARAM_NO_ITEM": "NO_ITEM", "PARAM_DEP_DATE": "DEP_DATE_ERROR", "B2G_NO_CONFIG": "B2G_PARAM_ERROR",
           "SEARCH_ERROR": "SEARCH_ERROR", "QUERY_STOCK_ERROR": "QUERY_STOCK_ERROR",
           "QUERY_FARE_ERROR": "QUERY_FARE_ERROR",
           "QUERY_POLICY_ERROR": "QUERY_POLICY_ERROR", "KA_AGENT": "KA_AGENT_INVALID", "KA_NO_RESULT": "KA_NO_RESULT",
           "QUERY_TGQ": "QUERY_TGQ_ERROR", "CHECK_FARE": "CHECK_FARE", "CHECK_POLICY": "CHECK_POLICY",
           "BUILD_AND_OIL": "BUILD_OIL_ERROR",
           "CHECK_RD": "CHECK_RD", "WAIT_HSF": "WAIT_HSF_TIMEOUT"}
    rs = {}
    tmp = "/tmp/stat_chosen_err.atw"
    os.system("rrun atx \"python stat_chosen_err.py\" > %s" % tmp)
    for line in open(tmp):
        if "atw" in line:
            continue
        kv = line.split("=")
        if len(kv) != 2:
            continue
        if not rs.has_key(kv[0]):
            rs[kv[0]] = int(kv[1])
        else:
            rs[kv[0]] = int(kv[1]) + int(rs[kv[0]])

    iCount = 0
    for k, v in rs.items():
        if col.has_key(k):
            iCount += v

    content = "<table border='1' ><tr><th>Reason</th><th>Times</th><th>%%</th></tr>%s</table>"

    cell = "<tr><td>%s</td><td>%s</td><td>%.2f%%</td></tr>"
    tmp = ""
    for k, v in rs.items():
        if col.has_key(k):
            tmp += cell % (col[k], v, int(v) * 100.0 / iCount)

    tmp += cell % ('', iCount, 100.0)

    c = content % tmp
    c.replace("\n", '')
    print c
    cmd = "java -jar /home/admin/tool/alimail.jar  %s \"%s\" \"%s\"" % (
        "chengwu.lcw@taobao.com", ("%s chosen error statistics" % _date), c)
    print cmd
    os.system(cmd)


if __name__ == "__main__":
    _date = str(datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), '%Y-%m-%d'))
    print _date
    sum(_date)
