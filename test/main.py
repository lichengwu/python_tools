__author__ = 'lichengwu'
# encoding=utf8

data = {}

if __name__ == "__main__":
    line = '2014-10-27 17:46:05.882 [ERROR] [pool-98-thread-11] B2BGetPolicyHandler - RequestId:1414403165716_4405_300232-代理商ID:4405-平台ID:300232|增量接口返回错误 ,ERROR CODE:-1 ERROR MESSAGE:系统异常，错误信息:没有找到用户SYZTTB开启的投放任务'
    for line in open("file_path"):
        arr = line.split(":")
        agent_id = arr[3].split('_')[1]
        err = "".join(arr[7:])
        key = agent_id + err
    if not data.has_key(key):
        data[key] = 1
    else:
        data[key] = int(data[key]) + 1
    for k, v in data.iteritems():
        print v, k