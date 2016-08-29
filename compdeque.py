from collections import deque
import zlib
import pickle
import struct


class CompressedDeque(deque):
    INT_NUMBER_OF_BYTES = 4

    def __init__(self, iterable=(), maxlen=None, compression_level=4):
        if compression_level < 0 or compression_level > 9:
            raise ValueError("Compression level must range from 0 to 9")
        super(CompressedDeque, self).__init__([self._compress(item) for item in iterable], maxlen)
        self.compression_level = compression_level

    def __iter__(self):
        return (self._decompress(compressed_value) for compressed_value in super(CompressedDeque, self).__iter__())

    def __getitem__(self, key):
        return self._decompress(super(CompressedDeque, self).__getitem__(key))

    def append(self, value):
        super(CompressedDeque, self).append(self._compress(value))

    def _compress(self, value):
        return zlib.compress(pickle.dumps(value, protocol=0), self.compression_level)

    def _decompress(self, compressed_value):
        return pickle.loads(zlib.decompress(compressed_value))

    @staticmethod
    def save_to_file(compressed_deque, file_path):
        with open(file_path, 'wb') as handle:
            header_number_of_items = struct.pack("i", len(compressed_deque))
            handle.write(header_number_of_items)
            for item in super(CompressedDeque, compressed_deque).__iter__():
                header_item_size = struct.pack("i", len(item))
                handle.write(header_item_size)
                handle.write(item)

    @staticmethod
    def load_from_file(file_path):
        compressed_deque = CompressedDeque([])
        with open(file_path, 'rb') as handle:
            header_number_of_items = handle.read(CompressedDeque.INT_NUMBER_OF_BYTES)
            number_of_items = struct.unpack("i", header_number_of_items)[0]
            for i in range(number_of_items):
                header_item_size = handle.read(CompressedDeque.INT_NUMBER_OF_BYTES)
                item_size = struct.unpack("i", header_item_size)[0]
                super(CompressedDeque, compressed_deque).append(handle.read(item_size))

        return compressed_deque