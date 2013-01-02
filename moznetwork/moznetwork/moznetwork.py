# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import socket
import array
import struct
if os.name != 'nt':
    import fcntl


def _get_interface_list():
    max_iface = 32  # Maximum number of interfaces(Aribtrary)
    bytes = max_iface * 32
    is_32bit = (8 * struct.calcsize("P")) == 32  # Set Architecture
    struct_size = 32 if is_32bit else 40

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    return [(namestr[i:i + 32].split('\0', 1)[0],
            socket.inet_ntoa(namestr[i + 20:i + 24]))\
            for i in range(0, outbytes, struct_size)]


def get_lan_ip():
    try:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:  # for Mac OS X
            ip = socket.gethostbyname(socket.gethostname() + ".local")
    except socket.gaierror:
        # sometimes the hostname doesn't resolve to an ip address, in which
        # case this will always fail
        ip = None

    if (ip is None or ip.startswith("127.")) and os.name != "nt":
        interfaces = _get_interface_list()
        for ifconfig in interfaces:
            if ifconfig[0] == 'lo':
                continue
            else:
                return ifconfig[1]
    return ip
