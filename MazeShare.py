import requests
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import sys

step_url = "https://puzzle.gztime.cc/api/maze/step"
reset_url = "https://puzzle.gztime.cc/api/maze/reset"
head = {
    "cookie": "" # 这里填你自己的cookie
}


def reset():
    requests.post(reset_url, headers=head)


# status[上下左右]
def get_status(x):
    return [int(i) for i in bin(x)[2:].zfill(4)][::-1]


def go(x, y, status, bdrc):
    global t, log, ct
    ct += 1
    print(ct, x, y, status)
    if x == 63 and y == 63: os.system("pause")
    t[x][y] = status
    status = get_status(status)
    if not status[0] and not t[x][y + 1] and ((0 <= x <= 63) and (0 <= y + 1 <= 63)):  # 上
        r = requests.post(step_url, headers=head, data={'drc': 'n'})
        # log.append(r)
        go(x, y + 1, json.loads(r.text)['newedges'], 's')
    if not status[1] and not t[x][y - 1] and ((0 <= x <= 63) and (0 <= y - 1 <= 63)):  # 下
        r = requests.post(step_url, headers=head, data={'drc': 's'})
        # log.append(r)
        go(x, y - 1, json.loads(r.text)['newedges'], 'n')
    if not status[2] and not t[x - 1][y] and ((0 <= x - 1 <= 63) and (0 <= y <= 63)):  # 左
        r = requests.post(step_url, headers=head, data={'drc': 'w'})
        # log.append(r)
        go(x - 1, y, json.loads(r.text)['newedges'], 'e')
    if not status[3] and not t[x + 1][y] and ((0 <= x + 1 <= 63) and (0 <= y <= 63)):  # 右
        r = requests.post(step_url, headers=head, data={'drc': 'e'})
        # log.append(r)
        go(x + 1, y, json.loads(r.text)['newedges'], 'w')
    requests.post(step_url, headers=head, data={'drc': bdrc})


def save():
    l = [[int(x)] for i in t for x in i]
    with open("test.json", "w") as f:
        f.write(json.dumps(l))


global t, log, ct
ct = 0
sys.setrecursionlimit(1000000)
log = []
t = np.zeros((64, 64), dtype=np.int32)
reset()
go(0, 0, 6, 0)
