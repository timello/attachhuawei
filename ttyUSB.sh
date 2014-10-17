#!/bin/sh

# Too hacky for a description

E220_BUS=`lsusb  | grep E220 | cut -d' ' -f2`
E220_DEV=`lsusb  | grep E220 | cut -d' ' -f4 | cut -d':' -f1`

audio=''
data=''
found_audio=false

for tty in `ls /dev/ttyUSB* | sort --version-sort`; do
    address=`udevadm info --name=$tty --attribute-walk | sed -n 's/\s*ATTRS{\(\(devnum\)\|\(busnum\)\)}==\"\([^\"]\+\)\"/\1\ \4/p' | head -n 2 | awk '{$1 = sprintf("%s:%03d", $1, $2); print $1;}'`
    bus=`echo $address | cut -d' ' -f1 | cut -d':' -f2`
    dev=`echo $address | cut -d' ' -f2 | cut -d':' -f2`
    if [ "$bus" = "$E220_BUS" ] && [ "$dev" = "$E220_DEV" ]; then
        if [ "$found_audio" = false ]; then
            audio=$tty
            found_audio=true
        else
            data=$tty
            break
        fi
    fi
done

export audio
export data

perl -0 -pi.bak1 -e 's|\CLARO-03|CLARO-03|g;s|(CLARO-03.*\n.*)audio=.+|\1audio=$ENV{audio}|g' /etc/asterisk/dongle.conf
perl -0 -pi.bak2 -e 's|\CLARO-03|CLARO-03|g;s|(CLARO-03.*\n.*\n.*)data=.+|\1data=$ENV{data}|g' /etc/asterisk/dongle.conf

asterisk -rx 'dongle reload now'
