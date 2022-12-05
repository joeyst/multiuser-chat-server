
import socket, select, sys, threading 

from handle_accept import handle_accept
from handle_pop import handle_pop 
from handle_recv_from_clients import handle_recv_from_clients 

# sample command line: `python chat_server.py 3490`
def usage():
    print("usage: python3 chat_server.py port", file=sys.stderr)

try:
  PORT = int(sys.argv[1])
except:
  usage()
  sys.exit()

BYTES_PER_RECV = 4096

listen = socket.socket()
listen.bind(('', PORT))
listen.listen()

# listening_sockets, client_sockets, buffer_dict, nick_dict 
buffer_dict = {}
listening_sockets = {listen}
client_sockets = set()
nick_dict = {}

print("waiting for connections")
while True:
  print("\n\n\n\n")
  print("listening_sockets:", listening_sockets)
  print("client_sockets:", client_sockets)
  print("buffer_dict:", buffer_dict)
  print("nick_dict:", nick_dict)
  print("\n\n\n\n")

  listening_sockets, client_sockets, buffer_dict, nick_dict = \
    handle_accept(listening_sockets, client_sockets, buffer_dict, nick_dict) 
  print("Finished handle_accept")

  client_sockets, buffer_dict, nick_dict = \
    handle_recv_from_clients(client_sockets, buffer_dict, nick_dict) 
  print("Finished handle_recv_from_clients")
