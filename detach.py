#!/usr/bin/env python

import re

from subprocess import call, Popen, PIPE

lsusb = Popen(['lsusb', '-v'], stdout=PIPE)

result = lsusb.communicate()[0]

pattern = re.compile("Bus (\d+) Device (\d+): ID.+Huawei")

for line in result.splitlines():
    for match in re.finditer(pattern, line):
        bus, device = match.groups()
        xml = "<hostdev type='usb'><source><address bus='%s' device='%s' /></source></hostdev>"  % (int(bus), int(device)) 
        with open('/tmp/hostdev.xml', 'w') as xml_file:
            xml_file.write(xml)
        status = call('virsh detach-device --domain Ubuntu --file /tmp/hostdev.xml', shell=True)
