import time
import socket
import os
import json
import pickle

HOST_IP = "0.0.0.0"
BUFFER_SIZE = 1024
SERVER_PORT = 53533
SERVER_FILE = "/tmp/auth_db.json"
TYPE = "A"

def main():
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketUDP.bind((HOST_IP, SERVER_PORT))

    while (True):
        msgBytes, client_addr = socketUDP.recvfrom(BUFFER_SIZE)
        message = pickle.loads(msgBytes)
        if len(message) == 4:
            name, value, type, ttl = pickle.loads(msgBytes)
            if not os.path.exists(SERVER_FILE):
                with open(SERVER_FILE, "w") as f:
                    json.dump({}, f, indent=4)
            with open(SERVER_FILE, "r") as f:
                oldRecords = json.load(f)
            ttl_ts = time.time() + int(ttl)
            oldRecords[name] = (value, ttl_ts, ttl)
            with open(SERVER_FILE, "w") as f:
                json.dump(oldRecords, f, indent=4)
        elif len(message) == 2:
            type, name = message
            with open(SERVER_FILE, "r") as f:
                oldRecords = json.load(f)
            if name not in oldRecords:
                dns_record = None
            value, ttl_ts, ttl = oldRecords[name]
            if time.time() > ttl_ts:
                dns_record = None
            dns_record =  (TYPE, name, value, ttl_ts, ttl)
            if dns_record:
                (_, name, value, _, ttl) = dns_record
                response = (type, name, value, ttl)
            else:
                response = ""
            response_bytes = pickle.dumps(response)
            socketUDP.sendto(response_bytes, client_addr)
        else:
            message = f"Expecting a message of len 4 or 2, got :{message!r}"
            socketUDP.sendto(message, client_addr)


if __name__ == '__main__':
    main()
