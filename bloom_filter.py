from mmh3 import murmur3_32
from bitarray import bitarray
from jenkins_hash import jenkins_hash


class BloomFilter:

    HASH_FUNCTIONS = {
        "murmur": lambda item, seed: murmur3_32(data_key=item, seed=seed),
        "jenkins": lambda item, seed: jenkins_hash(item, seed=seed),
    }

    def __init__(self, m=100000, k=7, hash_algorithm="murmur"):
        self.m = m
        self.k = k
        self.hash_algorithm = hash_algorithm
        self.bit_array = bitarray(m)
        self.bit_array.setall(0)

    @classmethod
    def get_available_hash_functions(cls):
        """
        Returns all hash algorithms currently supported by the Bloom Filter.
        """
        return list(cls.HASH_FUNCTIONS.keys())

    def _get_hash_indexes(self, item, hash_algorithm=None):
        """
        Returns the k Bloom Filter indexes for one selected hash algorithm.
        """
        algorithm = hash_algorithm or self.hash_algorithm

        if algorithm not in self.HASH_FUNCTIONS:
            raise ValueError(
                f"Unsupported hash algorithm: {algorithm}. "
                f"Supported algorithms: {self.get_available_hash_functions()}"
            )

        hash_function = self.HASH_FUNCTIONS[algorithm]
        return [hash_function(item, seed=i) % self.m for i in range(self.k)]

    def get_hashes(self, item, hash_algorithm=None):
        """
        Returns hash indexes for whatever hash function is requested.
        """
        algorithm = hash_algorithm or self.hash_algorithm

        if algorithm == "all":
            return {
                name: self._get_hash_indexes(item, name)
                for name in self.get_available_hash_functions()
            }

        return self._get_hash_indexes(item, algorithm)

    def _hashes(self, item):
        """
        Backward-compatible helper used by add() and check().
        """
        return self.get_hashes(item)

    def add(self, item):
        """
        Inserts item into filter.

        Will only be called by populating_bloom_filter.py, which
        contains a set of entirely malicious links, therefore it is assumed the
        link is malicious.
        """
        indices = self._hashes(item)
        for i in indices:
            self.bit_array[i] = 1

    def check(self, item):
        """
        Checks if item is in set.
        """
        indices = self._hashes(item)
        return all(self.bit_array[i] == 1 for i in indices)

    def get_fill_ratio(self):
        """
        Return how full the bit array is (float).
        """
        return sum(self.bit_array) / self.m

    def get_num_bits_set(self):
        return sum(self.bit_array)

    def save_bit_array(self, path):
        """
        Save bit array to file specified.
        """
        with open(path, "wb") as f:
            self.bit_array.tofile(f)

    def load_bit_array(self, path):
        """
        Load bit array from binary file.
        """
        self.bit_array = bitarray()
        with open(path, "rb") as f:
            self.bit_array.fromfile(f)

        if len(self.bit_array) > self.m:
            self.bit_array = self.bit_array[:self.m]
        elif len(self.bit_array) < self.m:
            self.bit_array.extend([0] * (self.m - len(self.bit_array)))
