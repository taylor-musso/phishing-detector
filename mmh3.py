def murmur3_32(key, seed=0):
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    length = len(key)
    hash_val = seed

    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    r1 = 15
    r2 = 13
    m = 5
    n = 0xe6546b64

    
    def rotate_left(n, r):
        return ((n << r) & 0xFFFFFFFF) | (n >> (32 - r))

    
    n_blocks = length // 4
    for i in range(0, n_blocks * 4, 4):
       
        k = (key[i] | 
             (key[i+1] << 8) | 
             (key[i+2] << 16) | 
             (key[i+3] << 24))

        k = (k * c1) & 0xFFFFFFFF
        k = rotate_left(k, r1)
        k = (k * c2) & 0xFFFFFFFF

        hash_val ^= k
        hash_val = rotate_left(hash_val, r2)
        hash_val = ((hash_val * m) + n) & 0xFFFFFFFF

 
    tail_index = n_blocks * 4
    remaining = length % 4
    k1 = 0

    if remaining >= 3:
        k1 ^= key[tail_index + 2] << 16
    if remaining >= 2:
        k1 ^= key[tail_index + 1] << 8
    if remaining >= 1:
        k1 ^= key[tail_index]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = rotate_left(k1, r1)
        k1 = (k1 * c2) & 0xFFFFFFFF
        hash_val ^= k1


    hash_val ^= length
    hash_val ^= (hash_val >> 16)
    hash_val = (hash_val * 0x85ebca6b) & 0xFFFFFFFF
    hash_val ^= (hash_val >> 13)
    hash_val = (hash_val * 0xc2b2ae35) & 0xFFFFFFFF
    hash_val ^= (hash_val >> 16)

    return hash_val

