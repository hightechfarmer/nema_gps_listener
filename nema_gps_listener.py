import logging
import socket
import pynmea2

logging.basicConfig(filename='udp.log', level=logging.DEBUG)


def parse_nema(msg):
    try:
        parsed_message = pynmea2.parse(msg)
    except:
        parsed_message = msg

    return parsed_message


def udp_server(host='0.0.0.0', port=8000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128*1024)
        yield parse_nema(data)


def main():
    for data in udp_server():
        logging.debug("%r" % (data,))


if __name__ == "__main__":
    main()
