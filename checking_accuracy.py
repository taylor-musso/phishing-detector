from bloom_filter import BloomFilter
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time


start_time = time.time()

bf = BloomFilter(hash_algorithm="murmur")
bf.load_bit_array("bit_array.bin")

false_pos = 0
true_neg = 0
true_pos = 0

with open("data/webpages_classification.json", "r") as f:
    for line in f:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if not url:
            continue

        is_in_filter = bf.check(url)
        is_malicious = obj.get("label", "").strip() == "bad"

        if is_in_filter:
            if is_malicious:
                true_pos += 1
            else:
                false_pos += 1
        else:
            if not is_malicious:
                true_neg += 1

end_time = time.time()

        
print(f"True Neg: {true_neg}, True Pos: {true_pos}, False Pos: {false_pos}")
print(f"Execution Time: {end_time - start_time:.4f} seconds")

conf_matrix = np.array([[true_pos, false_pos],
                        [0, true_neg]])

labels = conf_matrix

plt.figure(figsize=(6,5))
sns.heatmap(conf_matrix, annot=labels, fmt='', cmap='Blues', cbar=False,
            xticklabels=['Predicted Bad', 'Predicted Good'],
            yticklabels=['Actual Bad', 'Actual Good'])
plt.title("Confusion Matrix")
plt.show()