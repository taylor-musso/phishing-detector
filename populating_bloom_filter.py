from bloom_filter import BloomFilter
import json

bf = BloomFilter()

false_pos = 0
true_neg = 0

with open("data/filtered_malicious_webpages.json", "r") as f:
    for line in f:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if not url:
            continue

        bf.add(url)
        
print(f"Fill Ratio: {bf.get_fill_ratio()}, Bits Set: {bf.get_num_bits_set()}")
bf.save_bit_array("bit_array.bin")
print("Saved bit array")