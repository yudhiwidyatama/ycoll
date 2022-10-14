import time
import random
from os import path
import yaml
import socket
import os
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
a = "docker inspect --format \"{{.GraphDriver.Data.DeviceName}}\""
b = "docker ps --format \"{{.ID}} {{.Names}}\""
dockerps = os.popen(b)

totalRandomNumber = 0
class YCollector(object):
    def __init__(self):
        pass
    def collect(self):
        myhostname = socket.gethostname()
        lvmused = GaugeMetricFamily("ycoll_lvmused","Direct LVM used bytes", labels=['hostname','containername','namespace','podname'])
        lvmfree = GaugeMetricFamily("ycoll_lvmfree","Direct LVM free bytes", labels=['hostname','containername','namespace','podname'])
        with os.popen(b) as f:
          l1 = f.readlines()
          for litem in l1:
            arr = litem.strip().split(" ")
            container_name = arr[1]
            container_id = arr[0]
            cmda = "docker inspect --format \"{{.GraphDriver.Data.DeviceName}}\" "+container_id
            with os.popen(cmda) as f2:
              l2 = f2.readlines()
              for devicename in l2:
                devsplit = devicename.split("-")
                lvmid = devsplit[3].strip()
                lvmmnt = "/var/lib/docker/devicemapper/mnt/" + lvmid
                stat1 = os.statvfs(lvmmnt);
                stat2 = {}
                stat2['hostname'] = myhostname
                stat2['lvmmnt'] = lvmmnt
                stat2['container_name'] = container_name
                stat2['freebytes'] = stat1.f_bfree * stat1.f_bsize
                stat2['usedbytes'] = (stat1.f_blocks - stat1.f_bfree) * stat1.f_bsize
                k8sname = container_name.split("_")
                if len(k8sname)>=4 :
                  namespacevalue = k8sname[3]
                  podname = k8sname[2]
                  container_name = k8sname[1]
                  lvmused.add_metric([myhostname,container_name,namespacevalue,podname],stat2['usedbytes'])
                  lvmfree.add_metric([myhostname,container_name,namespacevalue,podname],stat2['freebytes'])
                else:
                  lvmused.add_metric([myhostname,container_name],stat2['usedbytes'])
                  lvmfree.add_metric([myhostname,container_name],stat2['freebytes'])

        yield lvmused
        yield lvmfree
if __name__ == "__main__":
    start_http_server(9101)
    REGISTRY.register(YCollector())
    while True: 
        # period between collection
        time.sleep(5)
