# Example usage:
#
# python select_server.py 3490

# create, bind, listen, use loop is select 
# explorations for how the rest is glued together 

import sys
import socket
import select

buf_dict = {}

def run_server(port):
    listening_socket = socket.socket()
    listening_socket.bind(('', port))
    listening_socket.listen()

    ready_set = {listening_socket}
    print("waiting for connections")

    while True:
      ready_to_read, _, _ = select.select(ready_set, {}, {})

      for s in ready_to_read:
        # if socket is listener socket 
        if s == listening_socket:
          new_conn, src = s.accept()
          ready_set.add(new_conn)
          print("{}:".format(new_conn.getpeername()), "connected")

        # if socket is client socket 
        else:
          name, port = s.getpeername()
          data = s.recv(4096)

          if (len(data) == 0):
            ready_set.remove(s)
            print("{}:".format(s.getpeername()), "disconnected")
          else:
            len_bytes = data[0:2]
            length = len(data)
            print((name, port), "{} bytes:".format(length), data)
          


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
