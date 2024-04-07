
from scapy.all import *
from scapy.layers.inet import IP, UDP

from response import Response
from parsers.arin_parser import ArinParser
from parsers.lacnic_parser import LacnicParser
from parsers.default_parser import DefaultParser


def get_response(ip):
    rirs = ["arin", "ripe", "apnic", "lacnic", "afrinic"]

    for rir in rirs:
        conn = socket.create_connection((f"whois.{rir}.net", 43))
        conn.sendall(f"{ip}\n".encode("utf-8"))

        data = read_data(conn)
        response = get_parser(rir).parse(data)
        if all(response.to_list()):
            return response

    return Response()


def read_data(connection):
    data = ""

    while True:
        buffer = connection.recv(1024)
        if len(buffer) == 0: break
        data += buffer.decode("utf-8")

    return data


def get_parser(rir):
    if rir == "arin":
        return ArinParser()
    if rir == "lacnic":
        return LacnicParser()

    return DefaultParser()


def trace(destination, max_hops, timeout):
    ip_list = list()
    ip_dst = socket.gethostbyname(destination)

    for ttl in range(max_hops):
        pack = IP(dst=ip_dst, ttl=ttl) / UDP(dport=33434)
        response = sr1(pack, timeout=timeout, verbose=False)

        if response:
            ip_list.append(response.src)
            if response.type == 3:
                break

    return ip_list + [ip_dst]


if __name__ == '__main__':
    trace = trace("vk.com", 16, 1)
    for ip in trace:
        print(*([ip] + get_response(ip).to_list()))
