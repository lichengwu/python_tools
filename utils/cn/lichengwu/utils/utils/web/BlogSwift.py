__author__ = 'lichengwu'

POST_PATH = "/Users/lichengwu/workspace/lichengwu.github.com/_posts"

SAVE_PATH = "/Users/lichengwu/tmp/hpstr-jekyll-theme"

import os

import re
import urllib2


def get_all_files(path, rs):
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if os.path.isfile(full_path):
            if full_path.endswith(".md"):
                rs.append(full_path)
        else:
            get_all_files(full_path, rs)


def get_name(path, full_path):
    short = full_path.split(path)[1]
    return short.split('/')[1]


def save_img(url, path):
    try:
        pr = path[0:path.rindex("/")]
        if not os.path.exists(pr):
            os.makedirs(pr)
        # resp = urllib2.urlopen(url)
        # f = open(path, 'w')
        # f.write(resp.read())
        # f.close()
        print "[save_img]:%s" % path
    except:
        print url


def save_md(full_path, _data):
    f = open(full_path, 'w')
    f.write(_data)
    f.close()
    print "[save_md]:%s" % full_path


def title_md(line):
    if not line.startswith('#'):
        return line
    pre = ''
    i = 0
    for c in line:
        if c == '#':
            pre += c
        elif c == ' ':
            return line
        else:
            nl = pre + ' ' + line[i:]
            print nl
            return nl
        i += 1


if __name__ == '__main__':

    p = re.compile("http.+?photobucket.+?png")

    rs = []
    get_all_files(POST_PATH, rs)

    pre_line = None

    for name in rs:
        category = get_name(POST_PATH, name)
        content = ""
        for line in open(name):
            if "JB/setup" in line:
                continue
            if "4_zpsce4a2696.png" in line:
                print line
                print  name
            match = p.search(line)
            if match:
                img = match.group()
                short_path = "/images/" + category + "/" + img.split("/")[-1]
                img_full_path = SAVE_PATH + short_path
                line = line.replace(img, short_path)
                save_img(img, img_full_path)
            # line = title_md(line)

            if line.startswith("#") and pre_line.strip() != '':
                line = "\n" + line + "\n"

            content += title_md(line)
            pre_line = line
        save_md(name, content)
    print rs
