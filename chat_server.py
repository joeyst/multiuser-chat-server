import socket, select, sys, threading 

from packet_gen import is_client_hello, get_server_error_packet, get_nick 

# sample command line: `python chat_server.py 3490`
def usage():
    print("usage: python3 chat_server.py port", file=sys.stderr)

try:
  PORT = int(sys.argv[1])
except:
  usage()
  sys.exit()

buffer_dict = {}
socket_nick = {}

listen = socket.socket()
listen.bind(('', PORT))
listen.listen()
all_sockets = {listen}
print("waiting for connections")

def broadcast(msg):
  global all_sockets, listen 

  for curr in all_sockets:
    if (curr != listen):
      curr.send(msg)

def receive_all(s):
  d = b'Temp'
  packet = b''

  while (len(d) != 0):
    d = s.recv(5)
    packet += d
  
  return packet 

def get_server_leave_packet_by_socket(s):
  return get_server_leave_packet(socket_nick[s])

def receive():
  global buffer_dict, socket_nick, listen, all_sockets

  while True: 
    readable, _, _ = select.select(all_sockets, {}, {}) 

    for s in readable:
      # if socket is listener socket 
      if s == listen:
        new_conn, src = s.accept()
        # it's possible that we'd want to "sanitize" hello packet here; 
        # it could have overwhelming amount of data or 
        # have invalid `utf-8` characters 
        # or the nick could already be taken. 
        # I believe it wasn't specified in the assignment, 
        # so I'm going with the least restrictive approach 
        # which risks overwhelming data. This also supports 
        # any length of names, which I don't believe was 
        # specified. This also runs the risk of getting stuck in 
        # an infinite loop and not allowing other clients 
        # send or receive data. 
        hello_packet = receive_all(new_conn)
        if is_client_hello(hello_packet):
          try:
            socket_nick[new_conn] = get_nick(hello_packet)
            # Adding client iff can get nick 
            all_sockets.add(new_conn)
          except:
            new_conn.send(get_server_error_packet())



      # if socket is client socket 
      else:
        # Only receiving 5 bytes here to 
          # 1) go breadth first; 
          # if one client sends an overwhelming amount of data, 
          # it is preferable that other clients get some of their 
          # data received too. 
          # 2) ensure that the program works, even on receiving 
          # uncommon lengths of data and potentially hidding 
          # edges of packet data 
        # All client data will be reached anyway, 
        # so there is no reason not too (aside from performance). 
        d = s.recv(5)
        if (len(d) == 0):
          all_sockets.remove(s)
          broadcast(get_server_leave_packet_by_socket(s)) # requires client name 
        else:
          buffer_dict[s] += d

def send():
  global all_sockets, listen 

  while True:
    for s, buf in buffer_dict.items():
      if is_poppable(buf):
        dicted, buf = pop_dict(buf)
        msg = dicted['message']
        nick = socket_nick[s]
        
        packet = get_server_chat_packet(msg, nick)
        broadcast(packet)

send_thread = threading.Thread(target=send, args=())
recv_thread = threading.Thread(target=receive, args=())

send_thread.start()
recv_thread.start()

recv_thread.join()

listen.close()
sys.exit()