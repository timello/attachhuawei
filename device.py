#!/usr/bin/env python

import optparse
import re

from subprocess import call, Popen, PIPE


XML_FILE = '/tmp/hostdev.xml'
HOSTDEV_XML = (
    "<hostdev type='usb'>"
    "  <source>"
    "    <address bus='%s' device='%s' />"
    "  </source>"
    "</hostdev>")
PATTERN = "Bus (\d+) Device (\d+): ID.+Huawei"


def main():
    usage = 'Usage: %s [options] [attach or detach]'
    optparser = optparse.OptionParser(usage=usage)
    optparser.add_option('-d', '--domain', help='Domain', default=None)
    opts, args = optparser.parse_args()

    lsusb = Popen(['lsusb', '-v'], stdout=PIPE)
    result = lsusb.communicate()[0]

    pattern = re.compile(PATTERN)
    command = 'virsh %s-device --domain %s --file %s' % (
            args[0], opts.domain, XML_FILE)

    for line in result.splitlines():
        for match in re.finditer(pattern, line):
            bus, device = match.groups()
            with open('/tmp/hostdev.xml', 'w') as xml_file:
                xml_file.write(HOSTDEV_XML % (int(bus), int(device)))
            status = call(command, shell=True)


if __name__ == '__main__':
    main()
