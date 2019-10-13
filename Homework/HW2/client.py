#!/usr/bin/env python3

# Import socket module
import socket
import argparse

parser = argparse.ArgumentParser(description='client side')
required = parser.add_argument_group('required arguments')
required.add_argument('-s', help='host IP Address', required=True)
required.add_argument('-p', type=int, help = "Host Port", required=True)
parser.add_argument('-i', dest='countHardware', action='store_true',
                    help='finding hardware information')
parser.add_argument('-m', dest='countMemory', action='store_true',
                    help='finding physical memory')
parser.add_argument('-w', dest='countSwap', action='store_true',
                    help='finding swap capacity')
parser.add_argument('-g', dest='countStorage', action='store_true',
                    help='finding storage capacity')
parser.add_argument('-c', dest='checkConnection', action='store_true',
                    help='check connection status')
parser.add_argument('-a', dest='access', action='store_true',
                    help='finding log access')
parser.add_argument('args', nargs=argparse.REMAINDER)
args, unknown = parser.parse_known_args()
args = vars(args)
print(args, unknown)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server on local computer
s.connect((args['s'], args['p']))
# message you send to server
# message sent to server
if args["countHardware"]:
    message = "i"
elif args["countMemory"]:
    message = "m"
elif args["countSwap"]:
    message = "w"
elif args['countStorage']:
    message = "g"
elif args['checkConnection']:
    message = "c"
elif args['access']:
    message = "a"
else:
    message = "x"


while True:
    
    print(message)
    s.send(message.encode('utf-8'))

    # messaga received from server
    data = s.recv(1024)

    # print the received message
    # here it would be a reverse of sent message
    print('Received from the server :', str(data.decode('utf-8')))
    break

# close the connection
s.close()
