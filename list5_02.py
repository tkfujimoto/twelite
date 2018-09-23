import struct, binascii, serial
import time

# コマンド0x80を送信する関数
def sendTWELite(s, sendto = 0x78,
        digital = [-1, -1, -1, -1],
        analog = [-1, -1, -1, -1]):
    # 先頭3バイト
    data = [sendto, 0x80, 0x01]
        
    # デジタル出力
    do = 0
    domask = 0
    for index, value in enumerate(digital):
        if value >= 0:
            domask |= 1 << index
            do |= (value & 1) << index
    data.append(do)
    data.append(domask)

    # アナログ出力
    for index, value in enumerate(analog):
        if value >= 0 and value <= 100:
            v = int(1024 * value / 100)
            data.append(v >> 8)
            data.append(v & 0xff)
        else:
            data.append(0xff)
            data.append(0xff)

    # チェックサムを計算する
    chksum = 0
    for val in data:
        chksum = (chksum + val) & 0xff
    data.append((0x100 - chksum) & 0xff)

    # 16進数文字列に変換する
    ss = struct.Struct("14B")
    outstring = binascii.hexlify(ss.pack(*data)).upper()

    # TWE-Liteに送信する
    s.write(":" + outstring + "\r\n")
    return

# COM3を開く
s = serial.Serial(2, 115200)

# 1秒ごとに点滅する
try:
    while 1:
        # 点灯
        sendTWELite(s, digital=[1, -1, -1, -1])
        time.sleep(1)
        # 消灯
        sendTWELite(s, digital=[0, -1, -1, -1])
        time.sleep(1)
except KeyboardInterrupt:
    pass

# COMを閉じる
s.close()
