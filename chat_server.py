import socket, select, sys, threading 

from packet_gen import is_client_hello, get_server_error_packet, get_nick 
from packet_decode import pop_dict, is_poppable

# sample command line: `python chat_server.py 3490`
def usage():
    print("usage: python3 chat_server.py port", file=sys.stderr)

try:
  PORT = int(sys.argv[1])
except:
  usage()
  sys.exit()

BYTES_PER_RECV = 4096

buffer_dict = {}
socket_nick = {}
unnamed_client_buffer_dict = {} # for clients connected but without finished hello packet; 
# purpose further explained later in file in `receive()` function 

listen = socket.socket()
listen.bind(('', PORT))
listen.listen()

listening_sockets     = {listen} 
clients_with_names    = set()
print("waiting for connections")

def broadcast(packet, clients):
  for curr in clients:
    curr.send(packet)

def get_server_leave_packet_by_socket(s):
  return get_server_leave_packet(socket_nick[s])

def receive():
  global buffer_dict, socket_nick 
  global listening_sockets, clients_with_names, unnamed_client_buffer_dict 

  while True: 
    print(listening_sockets)
    readable, _, _ = select.select(listening_sockets, {}, {}) 
    for s in readable:
      new_conn, addr = s.accept()
      print(new_conn.getpeername(), "connected")
      unnamed_client_buffer_dict[new_conn] = b''

    print(set(unnamed_client_buffer_dict.keys()))
    readable, _, _ = select.select(set(unnamed_client_buffer_dict.keys()), {}, {})
    for s in readable:
      d = s.recv(BYTES_PER_RECV)
      print(s)
      unnamed_client_buffer_dict[s] += d
      # if client sent a whole packet 
      buf = unnamed_client_buffer_dict[s]
      if (is_poppable(buf)):
        # if the whole packet the client sent is a hello packet 
        if (is_client_hello(buf)):
          # get the nick 
          nick = get_nick(buf)
          # set the socket's nick 
          socket_nick[s] = nick
          # remove client from unnamed list of clients 
          del unnamed_client_buffer_dict[s]
          # add client to list of clients with names 
          clients_with_names.add(s)
          # initialize the client's buffer 
          buffer_dict[s] = b''
        # if the whole packet the client sent is something other than a hello packet 
        else:
          # send an error packet back 
          s.send(get_server_error_packet())
          # close the connection 
          s.close()
          # remove the client from the list of unnamed clients 
          unnamed_client_buffer_dict.pop(s)
    del buf

    readable, _, _ = select.select(clients_with_names, {}, {}) 
    for s in readable:
      # Originally left at 5 bytes here to 
        # 1) go breadth first; 
        # if one client sends an overwhelming amount of data, 
        # it is preferable that other clients get some of their 
        # data received too. 
        # 2) ensure that the program works, even on receiving 
        # uncommon lengths of data and potentially hidding 
        # edges of packet data 
      # All client data will be reached anyway, 
      # so there is no reason not too (aside from performance). 
      d = s.recv(BYTES_PER_RECV)
      # if the client sent nothing, remove the client
      if (len(d) == 0):
        # remove client 
        clients_with_names.remove(s)
        # broadcast client leaving 
        broadcast(get_server_leave_packet_by_socket(s)) 
        # close connection w/ client 
        print("Closing connection with", s.getpeername())
        s.close()
      # else, add the data to the client's buffer 
      else:
        buffer_dict[s] += d

    for s, buf in buffer_dict.items():
      if is_poppable(buf):
        dicted, buf = pop_dict(buf)
        print(dicted)
        msg = dicted['message']
        nick = socket_nick[s]
        
        packet = get_server_chat_packet(msg, nick)
        broadcast(packet)

    

receive()
listen.close()
sys.exit()