from flask import Flask, request
import socket
import pickle

app = Flask(__name__)
BUFFER_SIZE = 1024

@app.route('/')
def info():
    return "This is FS (Fibonacci Server)"

def fibonacci(num):
    if num < 0:
        raise ValueError(f"number should be greater than 0")
    elif num == 0:
        return 0
    elif num == 1 or num == 2:
        return 1
    else:
        return fibonacci(num - 1) + fib(num - 2)


@app.route('/fibonacci')
def fibonacciSeries():
    num = int(request.args.get('number'))
    return str(fibonacci(num))


def registerAS(as_ip, as_port, hostname, val, type, ttl):
    message   = ((hostname, val, type, ttl))
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.sendto(pickle.dumps(message), (as_ip, int(as_port)))


@app.route('/register', methods=['PUT'])
def register():
    requestData = request.json
    if not requestData:
        raise ValueError("body is Null")
    hostname = requestData["hostname"]
    registerAS( as_ip =requestData["as_ip"],as_port = requestData["as_port"],hostname= hostname, val = requestData["fs_ip"], type = "A",ttl = requestData["ttl"])
    return "Done!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
