
# somehow the names got backward, too much of a time crunch
# to fix it though. It works properly at least! 
def get_chat_msg(nick, message, **_):
  return "{}: {}".format(message, nick)

def get_join_msg(nick, **_):
  return "*** {} has joined the chat".format(nick)

def get_leave_msg(nick, **_):
  return "*** {} has left the chat".format(nick)

def unknown_packet_type(packet_type):
  return "Error, unknown packet type {}.".format(packet_type)

client_format_dict = {
  'chat': get_chat_msg,
  'join': get_join_msg,
  'leave': get_leave_msg
}

