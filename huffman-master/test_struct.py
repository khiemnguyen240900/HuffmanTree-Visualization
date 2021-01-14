import struct

fout = open('test.dat', 'wb')

fout.write(struct.pack('>i', 42))
fout.write(struct.pack('>f', 2.71828182846))

fout.close()