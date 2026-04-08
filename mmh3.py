def murmur3_32(data_key, seed=0):
    #Convert text/url to bytes
    if isinstance(data_key, str):
        data_key = data_key.encode('utf-8')
    
    total_length = len(data_key) #length of bit encoding
    hash_value = seed  

    #constants for bit scrambling (both prime numbers)
    MIXER_1 = 0xcc9e2d51
    MIXER_2 = 0x1b873593
    
    #helper for bit shifting
    def rotate_left(value, bits_to_shift):
        return ((value << bits_to_shift) & 0xFFFFFFFF) | (value >> (32 - bits_to_shift))

    #process bits into 4 bit chunks
    num_full_blocks = total_length // 4
    for i in range(0, num_full_blocks * 4, 4):
        #combine chunk into 32 bit integer
        chunk = (data_key[i] | 
                 (data_key[i+1] << 8) | 
                 (data_key[i+2] << 16) | 
                 (data_key[i+3] << 24))

        #scramble the chunks with mixer values, and ensure there is no integer overflow
        chunk = (chunk * MIXER_1) & 0xFFFFFFFF
        chunk = rotate_left(chunk, 15)
        chunk = (chunk * MIXER_2) & 0xFFFFFFFF

        #merge scrambled chunk into hash value
        hash_value ^= chunk
        hash_value = rotate_left(hash_value, 13)
        
        # randomize the state with a linear transformation
        hash_value = ((hash_value * 5) + 0xe6546b64) & 0xFFFFFFFF

    #hash any remaining bytes not included in the 4 bit chunks
    tail_start = num_full_blocks * 4
    leftover_bytes = total_length % 4
    tail_chunk = 0

    if leftover_bytes >= 3:
        tail_chunk ^= data_key[tail_start + 2] << 16
    if leftover_bytes >= 2:
        tail_chunk ^= data_key[tail_start + 1] << 8
    if leftover_bytes >= 1:
        tail_chunk ^= data_key[tail_start]
        
        #scramble tail chunk
        tail_chunk = (tail_chunk * MIXER_1) & 0xFFFFFFFF
        tail_chunk = rotate_left(tail_chunk, 15)
        tail_chunk = (tail_chunk * MIXER_2) & 0xFFFFFFFF
        hash_value ^= tail_chunk

    
    #Xor top half of bits and bottom half to ensure every bit in unput affects each bit in output
    hash_value ^= total_length 
    
 
    hash_value ^= (hash_value >> 16)
    hash_value = (hash_value * 0x85ebca6b) & 0xFFFFFFFF
    hash_value ^= (hash_value >> 13)
    hash_value = (hash_value * 0xc2b2ae35) & 0xFFFFFFFF
    hash_value ^= (hash_value >> 16)

    return hash_value 