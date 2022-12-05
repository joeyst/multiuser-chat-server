
def broadcast(clients, packet):
  for s in clients:
    s.send(packet)