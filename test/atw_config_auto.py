__author__ = 'lichengwu'


def get_groups(sharding):
    sc = (int(sharding) - 1) * 8
    group_list = ""
    for s in xrange(sc, sc + 8):
        group_list += str(s) + ","
    return group_list[:-1]


def get_note(host):
    v = host[3]
    if v == 'm':
        return 'message_' + host[17:]
    else:
        t = host[4]
        if t == 'o':
            return 'b2c_' + v + '_' + host[19:]
        elif t == 'r':
            return 'rt_' + v + '_' + host[19:]
        elif t == 'b':
            return "b2b_" + v + '_' + host[18:]


if __name__ == "__main__":
    config = """atw7b010100054060.et2\t10.100.54.60
atw8b010100054070.et2\t10.100.54.70
atw5b010100054057.et2\t10.100.54.57
atw6b010100054058.et2\t10.100.54.58
atw5b010179212040.s.et2\t10.179.212.40
atw6b010179213116.s.et2\t10.179.213.116
atw7b010179213117.s.et2\t10.179.213.117
atw8b010179213164.s.et2\t10.179.213.164"""
    for line in config.split("\n"):
        pair = line.split("\t")
        host = pair[0].strip()
        ip = pair[1].strip()
        sharding = host[3]
        if sharding == 'm':
            print "insert into atw_server_config(gmt_create, gmt_modified, server_ip, biz_type, note, group_list, start_mode) values(now(), now(), '%s', 3, '%s', '0', 2);" % (
            ip, get_note(host))
        else:
            print "insert into atw_server_config(gmt_create, gmt_modified, server_ip, biz_type, note, group_list, start_mode) values(now(), now(), '%s', 3, '%s', '%s', 2);" % (
            ip, get_note(host),get_groups(sharding))




