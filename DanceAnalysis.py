import time
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter
import socket
import json

#Parameters
height = 0.1 #min/max magnitude of Gs (Gs)
threshold = 0.3 #min/max difference in Gs (Gs)
distance = 4 #min/max time between (cs)
width = 1 #min/max duration of Gs (cs)
cycles = 0
smoothing_window = 4
cycle_memory = 20
mean_window = 10

#Server Setup
HOST = "192.168.0.100"  # Standard loopback interface address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)

HOST2 = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT2 = 60010  # Port to listen on (non-privileged ports are > 1023)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()

#Other Setup
a = []
peak_count = []

while cycles <= cycle_memory:
    # Initialize Acceleration Data
    clientSocket, addr = serverSocket.accept()
    data = json.loads(clientSocket.recv(200).decode())
    clientSocket.close()

    x = np.array(data["AX"])  # X Accel
    y = np.array(data["AY"])  # Y Accel
    z = np.array(data["AZ"])  # Z Accel

    v = x + y + z  # magnitude of total vector
    a.append(v)

    cycles += 1
    print(cycles)

while True:
    # Get Acceleration Data
    clientSocket, addr = serverSocket.accept()
    data = json.loads(clientSocket.recv(200).decode())
    clientSocket.close()

    x = np.array(data["AX"])  # X Accel
    y = np.array(data["AY"])  # Y Accel
    z = np.array(data["AZ"])  # Z Accel

    v = x + y + z  # magnitude of total vector
    a.append(v)
    a = a[-cycle_memory:]   # ?s memory, cycles at ?hz

    # Smoothing
    #smoothed_accelerations = np.convolve(a, np.ones(mean_window)/mean_window)
    #print(a)

    # Analysis
    peaks = find_peaks(a, height, threshold, distance, width)
    peak_count.append(len(peaks[0]))
    peak_count = peak_count[-mean_window:]
    ma = np.convolve(peak_count, np.ones(mean_window)/mean_window, mode='valid')*1.25
    print("MA", ma)



    if len(ma)<2 and ma > 3.5 and ma < 4.5:
        engagement = "{engagement:1}"
    else:
        engagement = "{engagement:0}"

    # Send Engagement Status
    clientSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket2.connect((HOST2, PORT2))
    clientSocket2.send(engagement.encode())
    clientSocket2.close()
