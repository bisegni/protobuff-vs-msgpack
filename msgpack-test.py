import msgpack
import time
import os
import test_pb2
import argparse
from datasize import DataSize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bytes", help="Number of rando byte to generate",
                        type=int, default=1024*1024)
    parser.add_argument("-i", "--iterations", help="NUmber of iteration for every test",
                        type=int, default=1024)
    args = parser.parse_args()
    print("{} iteration for each test".format(args.iterations))
    print("Generate {} bytes each iteration".format(args.bytes))

    print("Test msgpack")
    byteToGenerate = args.bytes
    msgpackWroteSize = 0
    protobufWroteSize = 0
    msgpackExecutionTime = 0
    protobufExecutionTime = 0
    start = time.time()
    with open("random.msgpack", "wb") as outfile:
        for x in range(args.iterations):
            print("Msgpack Write index {}".format(x), end="\r")
            useful_dict = {
                "counter": x,
                "channel_name": "string data",
                "buffer": bytearray(os.urandom(byteToGenerate)),
            }
            packed = msgpack.packb(useful_dict, use_bin_type=True)
            msgpackWroteSize += len(packed)
            outfile.write(packed)
    msgpackExecutionTime = time.time() - start;
    print("\nTest protobuf")
    start = time.time()
    with open("random.protobuf", "wb") as outfile:
        for x in range(args.iterations):
            print("Protobuf Write index {}".format(x), end="\r")
            event_data = test_pb2.EventData()
            event_data.counter = x
            event_data.channel_name = "string data"
            event_data.buffer.append(bytes(os.urandom(byteToGenerate)))
            to_write = event_data.SerializeToString();
            protobufWroteSize += len(to_write)
            outfile.write(to_write)
    protobufExecutionTime = time.time() - start;     

    msgpack_file_size = os.path.getsize('random.msgpack')
    protobuf_file_size = os.path.getsize('random.protobuf')
    print("msgpack execution time {}".format(msgpackExecutionTime))
    print("msgpack byte written are {:MB}".format(DataSize(msgpackWroteSize)))
    print("msgpack file size is {:MB}".format(DataSize(msgpack_file_size)))
    print("protobuf execution time {}".format(protobufExecutionTime))
    print("protobuf byte written are {:MB}".format(DataSize(protobufWroteSize)))
    print("protobuf file size is {:MB}".format(DataSize(protobuf_file_size)))

if __name__ == "__main__":
   main()
