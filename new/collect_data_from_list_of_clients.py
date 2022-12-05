
def collect_data_from_single_client(s):
  tcp_packet = b''
  while True:
    d = s.recv(5)
    print("In collect_data_from_single_client, received:", d)
    print("Should see print statement about returning immediately after this.")
    if (len(d) == 0):
      print("Returning immediately.")
      return tcp_packet
    tcp_packet += d

def collect_data_from_list_of_clients(clients, buf_dict, verbose=True):
  print("This assumes all of the provided clients are ready to receive from.")
  for s in clients:
    buf_dict[s] += collect_data_from_single_client(s)
  return buf_dict
