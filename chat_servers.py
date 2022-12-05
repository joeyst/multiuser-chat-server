

# (socket object, buffer)
buffer_dict = {}

# (socket object, nick)
socket_nick = {}
# if client name is in socket nick and sending chat packet, good. 
# if client name not in socket nick and sending chat packet, disconnect. 
# if client name not in socket nick and sending hello packet, good. 
# if client name is in socket nick and sending hello packet, disconnect. 

class ClientTracker:
  """
  A data class that allows methods to mutate the same dictionaries: 
  - buffer_dict 
  - socket_nick 
  """
  def __init__(self, listening_set, buffer_dict={}, socket_nick={}):
    self.listening_set = listening_set
    self.buffer_dict   = buffer_dict
    self.socket_nick   = socket_nick

  def get_name(self, s):
    return self.socket_nick[s]

  def is_named(self, s):
    return s in self.socket_nick

  def is_not_named(self, s):
    return not self.is_named(s)

  def broadcast(self, packet):
    for s in self.socket_nick.keys():
      s.send(packet)