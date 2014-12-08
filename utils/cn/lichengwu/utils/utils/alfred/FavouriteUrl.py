__author__ = 'lichengwu'

# encoding=utf8

import alfred

PATH = "/Users/lichengwu/.bin/favourite.data"
MAX_SIZE = 9


def load_data(file_path):
    data = []
    for line in open(file_path):
        line = line.decode("utf8")
        info = line.strip().split("\t")
        if len(info) != 3:
            continue
        data.append((info[0], info[1], info[2]))
    return data


def build_item(key, title, url):
    return alfred.Item({"arg": url, "autocomplete": key}, title, url, "E052DC0C-DC4A-4142-91CA-1EEE0BF00C51.png")


if __name__ == '__main__':
    data = load_data(PATH)
    key = '{query}'
    items = []
    count = 0
    for item in data:
        if key in item[0] or key in item[2]:
            count += 1
            items.append(build_item(item[0], item[1], item[2]))
            if count >= MAX_SIZE:
                break
    print alfred.write(alfred.xml(items))

