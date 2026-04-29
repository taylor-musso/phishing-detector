from mmh3 import murmur3_32
from bitarray import bitarray 

class BloomFilter: 
    def __init__(self, m=100000, k=7): 
        self.m = m 
        self.k = k 
        self.bit_array = bitarray(m) 
        self.bit_array.setall(0) 
    
    def _hashes(self, item): 
        ''' 
        Generates hashes 
        ''' 
        return [murmur3_32(data_key = item, seed=i) % self.m for i in range(self.k)] 
    
    def add(self, item): 
        ''' 
        Inserts item into filter 

        Will only be called by populating_bloom_filter.py, which
        contains a set of entirely malicious links, therefore it is assumed the
        link is malicious
        ''' 
        indices = self._hashes(item) 
        for i in indices: 
            self.bit_array[i] = 1 
        
    def check(self, item): 
        ''' 
        Checks if item is in set 
        
        Returns: 
            bool 
        ''' 
        indices = self._hashes(item) 
        return all(self.bit_array[i] == 1 for i in indices) 
        
    def get_fill_ratio(self): 
        ''' 
        Return how full the bit array is (float) 
        ''' 
        return sum(self.bit_array) / self.m 
    
    def get_num_bits_set(self): 
        return sum(self.bit_array) 
    
    def save_bit_array(self, path): 
        ''' 
        Save bit array to file specified 
        ''' 
        with open(path, "wb") as f: 
            self.bit_array.tofile(f) 
            
    def load_bit_array(self, path): 
        ''' 
        Load bit array from binary file 
        ''' 
        self.bit_array = bitarray() 
        with open(path, "rb") as f: 
            self.bit_array.fromfile(f) 
        
        if len(self.bit_array) > self.m: 
            self.bit_array = self.bit_array[:self.m] 
        elif len(self.bit_array) < self.m: 
            self.bit_array.extend([0] * (self.m - len(self.bit_array)))