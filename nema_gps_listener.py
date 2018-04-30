import logging
import socket
import pynmea2

logging.basicConfig(filename='nema_gps_listener.log', level=logging.DEBUG)


def parse_nema(msg):
    """ parse a nema coded message if we can """
    try:
        parsed_message = pynmea2.parse(msg)
    except:
        parsed_message = None

    return parsed_message


def update_coordinates_file(payload):
    """ write a file with lat/lon pairs """
    try:
        file = open("location.txt", "w")
        file.write(payload)
        file.close()
    except:
        print "unable to write location file"
    return True


def udp_server(host='0.0.0.0', port=8000):
    """ a udb server """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128*1024)
        yield parse_nema(data)


def main():
    for data in udp_server():
        if data:

            try:
                thedate = "{} {}".format(data.datestamp.strftime("%Y-%m-%d"), data.timestamp.strftime("%H:%M:%S"))
                output = "{} nema payload: {}".format(thedate, data)
                logging.debug(output)

                location = "{}, {}".format(data.latitude, data.longitude)
                update_coordinates_file(location)

            except Exception as e:
                logging.debug(e)


if __name__ == "__main__":
    main()
