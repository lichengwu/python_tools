__author__ = 'lichengwu'

# coding=utf8

import json
import commands

if __name__ == "__main__":
    text = ""
    for line in open("/Users/lichengwu/Downloads/a"):
        text += line
    text = text.strip().replace("\n", "")
    text = text[1:-1]
    text = text[0: text.rfind('beanName') - 3]
    data = json.loads(text)
    rs = {}
    raw = data['returnValue']
    for db in raw:
        rs[db] = {}
        print db
        cd = raw[db]
        for city in cd:
            city = city.replace('-', '')
            key = int(commands.getstatusoutput("java -cp '/Users/lichengwu/Downloads' hashcode " + city)[1])
            print key

    print commands.getstatusoutput('java -cp "/Users/lichengwu/Downloads" hashcode 1111')[1]
    print data['returnValue']