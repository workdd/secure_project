with open('../ETPAE9A6E0LS4.2021-11-03-00.f5c8dbff') as f:
    data = f.read()

data = data.split('\n')
data = data[2:]

ips = [data[idx].split('\t')[4] for idx in range(len(data) - 1)]
print(ips)



#!/usr/bin/env python




