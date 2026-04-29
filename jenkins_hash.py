def jenkins_hash(key, seed=0):
    """
    Generate a 32-bit Jenkins hash for a string.

    Args:
        key (str): Input value, for example a URL.
        seed (int): Seed value used to create multiple hash outputs.

    Returns:
        int: Unsigned 32-bit hash value.
    """
    hash_value = seed & 0xFFFFFFFF

    for char in key:
        hash_value += ord(char)
        hash_value &= 0xFFFFFFFF

        hash_value += (hash_value << 10)
        hash_value &= 0xFFFFFFFF

        hash_value ^= (hash_value >> 6)
        hash_value &= 0xFFFFFFFF

    hash_value += (hash_value << 3)
    hash_value &= 0xFFFFFFFF

    hash_value ^= (hash_value >> 11)
    hash_value &= 0xFFFFFFFF

    hash_value += (hash_value << 15)
    hash_value &= 0xFFFFFFFF

    return hash_value
