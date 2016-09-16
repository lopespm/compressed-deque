import os
from unittest import TestCase

from compdeque import CompressedDeque
from tempdir import TempDir


class TestCompressedDeque(TestCase):

    def test_len_object_mix(self):
        collection = CompressedDeque()
        collection.append(ComplexObject("string value 1", 5, [2, 3 ,5 ,6]))
        collection.append("sample string 2")
        collection.append(455.0)
        self.assertEqual(len(collection), 3)

    def test_numbers(self):
        collection = CompressedDeque()
        collection.append(333.5)
        collection.append(42.42)
        collection.append(11)
        self.assertEqual(list(collection), [333.5, 42.42, 11])

    def test_strings(self):
        collection = CompressedDeque()
        collection.append("sample string 1")
        collection.append("sample string 2")
        self.assertEqual(list(collection), ["sample string 1", "sample string 2"])

    def test_complex_objects(self):
        collection = CompressedDeque()
        item1 = ComplexObject("string value 1", 5, [2, 3 ,5 ,6])
        item2 = ComplexObject("string value 2", 44.0, [0, "another value", 5, False])

        collection.append(item1)
        collection.append(item2)

        self.assertEqual(list(collection), [item1, item2])

    def test_initial_data(self):
        collection = CompressedDeque([1, 2, 3])
        self.assertEqual(collection[0], 1)

    def test_persistance_simple_objects(self):
        with TempDir() as temp_directory:
            file_path = os.path.join(temp_directory, 'compressed_deque.dat')
            collection = CompressedDeque()
            collection.append(333.5)
            collection.append(11)
            collection.append("sample string 1")
            collection.append(True)

            CompressedDeque.save_to_file(compressed_deque=collection, file_path=file_path)
            retrieved_collection = CompressedDeque.load_from_file(file_path)

            expected_collection = [333.5, 11, "sample string 1", True]
            self.assertSequenceEqual(list(retrieved_collection), expected_collection)

    def test_persistance_complex_objects(self):
        with TempDir() as temp_directory:
            file_path = os.path.join(temp_directory, 'compressed_deque.dat')
            collection = CompressedDeque()
            item1 = ComplexObject("string value 1", 5, [2, 3, 5, 6])
            item2 = ComplexObject("string value 2", 44.0, [0, "another value", 5, False])
            collection.append(item1)
            collection.append(item2)

            CompressedDeque.save_to_file(compressed_deque=collection, file_path=file_path)
            retrieved_collection = CompressedDeque.load_from_file(file_path)

            expected_collection = [item1, item2]
            self.assertSequenceEqual(list(retrieved_collection), expected_collection)

    def test_valid_compression_level_lower_bound(self):
        collection = CompressedDeque(compression_level=0)
        collection.append(455.0)
        self.assertEqual(list(collection), [455.0])

    def test_valid_compression_level_upper_bound(self):
        collection = CompressedDeque(compression_level=9)
        collection.append(455.0)
        self.assertEqual(list(collection), [455.0])

    def test_invalid_compression_levels_lower_bound(self):
        self.assertRaises(ValueError, CompressedDeque, compression_level=-1)

    def test_invalid_compression_levels_upper_bound(self):
        self.assertRaises(ValueError, CompressedDeque, compression_level=10)


class ComplexObject(object):
    def __init__(self, string_value, number_value, list_of_values):
        self.string_value = string_value
        self.number_value = number_value
        self.list_of_values = list_of_values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.string_value == other.string_value \
               and self.number_value == other.number_value \
               and self.list_of_values == other.list_of_values