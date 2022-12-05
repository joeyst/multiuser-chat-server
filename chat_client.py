
import socket, threading, sys 
from packet_gen import get_client_hello_packet 
from client_input import input_fn 
from client_recv import recv_fn
from chatui import init_windows, end_windows 

# example usage: `python chat_client.py chris localhost 3490` 
def usage():
  print("usage: python3 chat_client.py jorgefulson localhost 3490")

try: 
  NICK   = sys.argv[1]
  SERVER = sys.argv[2]
  PORT   = int(sys.argv[3])
except:
  usage()
  sys.exit()

# Initializing connection 
s = socket.socket()
s.connect((SERVER, PORT))

# Initializing chat display window 
init_windows()

# Sending hello packet to server with nickname 
hello = get_client_hello_packet(NICK) 
s.send(hello)
print("Sent hello!")

# Creating input and receiving threads 
input_thread = threading.Thread(target=input_fn, args=(NICK, s))
recv_thread = threading.Thread(target=recv_fn, args=(s,), daemon=True)

# Running threads 
input_thread.start()
recv_thread.start()

# Joining threads on return of input thread 
input_thread.join()

# Closing the connection 
s.close()

# Closing the window 
end_windows()

# Exiting the program 
sys.exit()