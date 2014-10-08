#!/usr/bin/env python

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

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
