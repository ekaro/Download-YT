import socket, os, struct

def analyze_ether_header(data):
    eth_hdr  = sruct.unpack("!6s6sH", data[:14]) #IPv4 = 0x0800
    dest_mac = eth_hdr[0] #Destination Address
    src_mac  = eth_hdr[1] #Source Address
    proto    = eth_hdr[2] #Next protocol

    print dest_mac
    print src_mac
    print hex(proto)

    data = data[14:]
    return data

def main():
    sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    recv_data = sniffer_socket.recv(2048)

    data = analyze_ether_header(recv_data)
    
main()
