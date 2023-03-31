import msgpack

import random
import os
import test_pb2

byteToGenerate = 1024*1024
msgpackWroteSize = 0
protobufWroteSize = 0
with open("random.msgpack", "wb") as outfile:
    for x in range(1024):
        print("Msgpack Write index {}".format(x), end="\r")
        useful_dict = {
            "counter": x,
            "channel_name": "string data",
            "buffer": bytearray(os.urandom(byteToGenerate)),
        }
        packed = msgpack.packb(useful_dict, use_bin_type=True)
        msgpackWroteSize += len(packed)
        outfile.write(packed)
print()
with open("random.protobuf", "wb") as outfile:
    for x in range(1024):
        print("Protobuf Write index {}".format(x), end="\r")
        event_data = test_pb2.EventData()
        event_data.counter = x
        event_data.channel_name = "string data"
        event_data.buffer.extend(bytearray(os.urandom(byteToGenerate)))
        to_write = event_data.SerializeToString();
        print(to_write)
        protobufWroteSize += len(to_write)
        outfile.write(to_write)
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
  
msgpack_file_size = os.path.getsize('random.msgpack')
protobuf_file_size = os.path.getsize('random.protobuf')
print("msgpack byte written are :", sizeof_fmt(msgpackWroteSize))
print("msgpack file size is :", sizeof_fmt(msgpack_file_size))
print("protobuf byte written are :", sizeof_fmt(protobufWroteSize))
print("protobuf file size is :", sizeof_fmt(protobuf_file_size))