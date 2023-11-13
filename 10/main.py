import socket
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def centroid(labeled, label=1):
    pos = np.where(labeled == label)
    return pos[0].mean(), pos[1].mean()

host = "84.237.21.36"
port = 5152

# plt.ion()
# plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    beat = b"nope"
    sock.connect((host, port))
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)
        # print(len(bts))

        img = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])
        img[img>0]=1
        labeled = label(img)
        pos1 = centroid(labeled, 1)
        pos2 = centroid(labeled, 2)
    # print(np.abs(np.array(pos1) - np.array(pos2)))
        res = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
        print(res)
        sock.send(f"{round(res, 1)}".encode())
        print(sock.recv(4).decode())

        sock.send(b"beat")
        beat = sock.recv(20)

    # plt.clf()
        # plt.subplot(121)
    # plt.title(str(pos1))
    # plt.imshow(labeled)
    # plt.subplot(122)
    # plt.title(str(pos2))
    # plt.imshow(img2)
    # plt.pause(10)
