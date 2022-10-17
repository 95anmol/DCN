from flask import Flask, request
import pickle
import socket
import requests

app = Flask(__name__)

BUFFER_SIZE = 2048

@app.route('/')
def US():
    return 'This is US (User Server)'


@app.route('/fibonacci', methods=["GET"])
def fibonacciSeries():
    openSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = request.args.get('hostname').replace('"','')
    fs_port  = int(request.args.get('fs_port'))
    openSocket.sendto(pickle.dumps(("A", hostname)), (request.args.get('as_ip').replace('"',''), int(request.args.get('as_port'))))
    response, _ = openSocket.recvfrom(BUFFER_SIZE)
    response = pickle.loads(response)
    type, hostname, fs_ip, ttl = response
    if not fs_ip:
        return "Couldn't retrieve fs_ip"
    return requests.get(f"http://{fs_ip}:{fs_port}/fibonacci",
                        params={"number": int(request.args.get('number'))}).content


app.run(host='0.0.0.0',
        port=8080,
        debug=True)