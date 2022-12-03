
class Client:
  """
    A class for handling sending and receiving packets by a client. 
    Initialized with a port for the client, a port of the server, a buffer, 
    and the state of whether the client is connected or not. 

    Calling `.run()` runs a while loop until the port disconnects. The client 
    must be spawned in a daemon thread so more clients can be generated, and that
    each client's thread will be killed if the system exits. 
  """

  def __init__(self, own_port, server_port, name, state):
    self.own_port = own_port
    self.server_port = server_port
    self.name = name
    self.state = state 

  def run(self):
    while self.state: 
      pass