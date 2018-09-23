import struct, binascii, serial
import time

# �R�}���h0x80�𑗐M����֐�
def sendTWELite(s, sendto = 0x78,
        digital = [-1, -1, -1, -1],
        analog = [-1, -1, -1, -1]):
    # �擪3�o�C�g
    data = [sendto, 0x80, 0x01]
        
    # �f�W�^���o��
    do = 0
    domask = 0
    for index, value in enumerate(digital):
        if value >= 0:
            domask |= 1 << index
            do |= (value & 1) << index
    data.append(do)
    data.append(domask)

    # �A�i���O�o��
    for index, value in enumerate(analog):
        if value >= 0 and value <= 100:
            v = int(1024 * value / 100)
            data.append(v >> 8)
            data.append(v & 0xff)
        else:
            data.append(0xff)
            data.append(0xff)

    # �`�F�b�N�T�����v�Z����
    chksum = 0
    for val in data:
        chksum = (chksum + val) & 0xff
    data.append((0x100 - chksum) & 0xff)

    # 16�i��������ɕϊ�����
    ss = struct.Struct("14B")
    outstring = binascii.hexlify(ss.pack(*data)).upper()

    # TWE-Lite�ɑ��M����
    s.write(":" + outstring + "\r\n")
    return

# COM3���J��
s = serial.Serial(2, 115200)

# 1�b���Ƃɓ_�ł���
try:
    while 1:
        # �_��
        sendTWELite(s, digital=[1, -1, -1, -1])
        time.sleep(1)
        # ����
        sendTWELite(s, digital=[0, -1, -1, -1])
        time.sleep(1)
except KeyboardInterrupt:
    pass

# COM�����
s.close()
