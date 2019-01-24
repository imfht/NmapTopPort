# @author: jinxufang
# @time: 2019/01/24

import re
from subprocess import Popen, PIPE


def convert_nmap_port(nmap_port):
    for i in nmap_port.split(","):
        if '-' in i:
            start, end = i.split("-")
            for i in range(int(start), int(end) + 1):
                yield int(i)
        else:
            yield int(i)


def get_list(topN=1000):
    process = Popen("nmap -oG - -v --top-ports %d" % topN, shell=True, stdout=PIPE)
    stdout = process.communicate()[0].decode('utf-8')
    nmap_port = re.findall("TCP\\(%d;(.*?)\)" % topN, stdout)[0]
    with open("./nmap-top-%d.txt" % topN, 'w+') as f:
        for port in convert_nmap_port(nmap_port):
            f.writelines("%d\n" % port)


if __name__ == '__main__':
    x = 2
    while x <= 8306:  # nmap 7.70 only have 8306 built-in port.
        print(x)
        get_list(x)
        x *= 2
    get_list(8306)
