from enum import Enum
import json

MessageType = Enum('MessageType', ['CHAT', 'EXIT', 'UNKNOWN_COMMAND'])

class Message:
  def __init__(self, raw_message):
    self.m = raw_message

  def get_m(self):
    return self.m

  def _len_bytes(self):
    return int.to_bytes(self._len_int(), 2, 'big')

  def _len_int(self):
    return len(self.get_m())

  def packet(self):
    return self._packet().encode("UTF-8")

  @classmethod
  def hello_packet(cls, nick):
    return cls._hello_packet(nick).encode("UTF-8")

  def _packet(self):
    temp_packet = {
      "type": "chat",
      "message": self.get_m()
    }

    jsoned = json.dumps(temp_packet)
    length = int.to_bytes(len(jsoned), 2, 'big')
    return str(len(jsoned)) + json.dumps(temp_packet)

  @classmethod  
  def _hello_packet(cls, nick):
    temp_packet = {
      "type": "hello",
      "nick": nick
    }

    jsoned = json.dumps(temp_packet)
    length = int.to_bytes(len(jsoned), 2, 'big')
    return str(len(jsoned)) + json.dumps(temp_packet)

  def _type(self):
    if self._len_int() > 0 and self.get_m()[0] == "/":
      if self._len_int() > 1 and self.get_m()[1] == "q":
        return MessageType.EXIT
      else:
        return MessageType.UNKNOWN_COMMAND
    else:
      return MessageType.CHAT

# msg = Message(input("Enter msg: "))
# print(msg._len_bytes())
# print(msg._len_int())
# print(msg._type())
