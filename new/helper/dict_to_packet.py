
import json

def _dict_to_packet(**kwargs):
  jsoned = json.dumps(kwargs).encode('utf-8')
  length = int.to_bytes(len(jsoned), 2, 'big')
  return length + jsoned

