import json
import socket
import os
a = "docker inspect --format \"{{.GraphDriver.Data.DeviceName}}\""
b = "docker ps --format \"{{.ID}} {{.Names}}\""
c = "docker ps --format \"{{.ID}}\" | xargs docker inspect -f \"{{.ID}} {{.Name}} {{.GraphDriver.Data.DeviceName}}\""
# dockerps = os.popen(b)
hostname = socket.gethostname()
# print "["
hasbefore = 0
with os.popen(c) as f:
   l1 = f.readlines()
   for litem in l1:
      arr = litem.strip().split(" ")
      container_name = arr[1]
      container_id = arr[0]
      devicename = arr[2]
      devsplit = devicename.split("-")
      lvmid = devsplit[3].strip()
      lvmmnt = "/var/lib/docker/devicemapper/mnt/" + lvmid 
#              print("lvmid = "+ lvmid + " for container " + container_name + " #" + container_id)

      stat1 = os.statvfs(lvmmnt);
      stat2 = {}
      stat2['hostname'] = hostname
      stat2['lvmmnt'] = lvmmnt 
      stat2['container_name'] = container_name
      stat2['freebytes'] = stat1.f_bfree * stat1.f_bsize
      stat2['usedbytes'] = (stat1.f_blocks - stat1.f_bfree) * stat1.f_bsize
      stat3 = json.dumps(stat2)
#              if hasbefore>0 :
#                  print(",")
      print(stat3)
      hasbefore=1
