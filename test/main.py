__author__ = 'lichengwu'
# encoding=utf8


import time

if __name__ == '__main__':

    query = '{query}'

    t = 0

    if len(query) > 10:
        t = long(query) / 1000
    else:
        t = long(query)

    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t))

    print """
    <items>
        <item arg="%s" autocomplete=""><title>转换结果</title><subtitle>%s</subtitle><icon></icon></item>
    </items>
    """ % (time_str, time_str)
