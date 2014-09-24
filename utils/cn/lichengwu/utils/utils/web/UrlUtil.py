

import urllib

def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = [v]

    return d

if __name__ == '__main__':
    str = """http://uc.sankuai.com/api/users?ids=%5B20807%5D&entityType=5"""
    print urldecode(str)