__author__ = 'lichengwu'

from sys import path

path.append("/home/chengwu.lcw/stat/")
import simplejson as json
import sys
import monitor

if __name__ == "__main__":
    path = sys.argv[1]
    data = ""
    for line in open(path):
        data += line
    data = data.strip().replace("\\n", "")
    data = data.replace("/", ",")
    # print "data:"
    # print data
    raw = json.loads(data)
    rs = {}
    for k in raw:
        p = raw[k].split(",")
        if len(p) <= 0:
            continue
        for kv in p:
            if len(kv) <= 0:
                continue
            stat = kv.split("=")
            if len(stat) != 2:
                continue
            if not rs.has_key(stat[0]):
                rs[stat[0]] = int(stat[1])
            else:
                rs[stat[0]] = int(stat[1]) + int(rs[stat[0]])
    iCount = 0
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
    for k, v in rs.items():
        if col.has_key(k):
            iCount += v
    content = "<table border='1' ><tr><th>Reason</th><th>Times</th><th>%%</th></tr>%s</table>"
    cell = "<tr><td>%s</td><td>%s</td><td>%.2f%%</td></tr>"
    tmp = ""
    monitor_data = {"chosen_err_total": iCount}
    for k, v in rs.items():
        if col.has_key(k):
            tmp += cell % (col[k], v, int(v) * 100.0 / iCount)
            mk = None
            if "PARAM_" in k:
                mk = "chosen_err_param"
            else:
                mk = "chosen_err_" + k.lower()
            if monitor_data.has_key(mk):
                monitor_data[mk] += int(v)
            else:
                monitor_data[mk] = int(v)
    # send data to alimonitor
    monitor.put("data_collect", monitor_data)

    tmp += cell % ('', iCount, 100.0)
    c = content % tmp
    c.replace("\n", '')
    print c