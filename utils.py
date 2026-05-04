import argparse
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
from bloom_filter import BloomFilter


def parse_args():
    ''' 
    Parse command-line arguments to determine which hash function is used
    '''
    parser = argparse.ArgumentParser(description="Bloom Filter Email Simulator")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--murmur", action="store_true", help="Use MurmurHash3")
    group.add_argument("--jenkins", action="store_true", help="Use Jenkins hash")

    parser.add_argument("port", nargs="?", type=int, default=9999,
                        help="Streaming socket port (default: 9999)")

    return parser.parse_args()

def bloom_filter_args():
    '''
    Gets command-line args, then gets arguments for 
    Bloom Filter initialization
    '''
    args = parse_args()

    hash_algo = "murmur"
    bit_array_path = "bit_array/bit_array.bin"

    if args.murmur:
        hash_algo = "murmur"
        bit_array_path = "bit_array/bit_array.bin"
        print("Using MurmurHash3\n\n")
    elif args.jenkins:
        hash_algo = "jenkins"
        bit_array_path = "bit_array/bit_array_jenkins.bin"
        print("Using Jenkins Hash\n\n")
    return hash_algo, bit_array_path

def csv_to_json():
    '''
    Converts a CSV file to a JSON file. 

    Input and Output paths are specified and should not change
    as they will be used by other files.
    '''
    csv_file = "data/Webpages_Classification_test_data.csv"
    json_file = "data/webpages_classification.json"

    with open(csv_file, mode="r", encoding="utf-8") as infile, \
        open(json_file, mode="w", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)

        for row in reader:
            json_line = json.dumps(row)
            outfile.write(json_line + "\n")

    print("Done! NDJSON file created.")

def filter_malicious_webpages():
    '''
    Filters a JSON file to only include URL and LABEL 
    for malicious webpages.

    Input and Output paths are specified and should not change
    as they will be used by other files.
    '''
    input_file = "data/webpages_classification.json"
    output_file = "data/filtered_malicious_webpages.json"

    with open(input_file, "r", encoding="utf-8") as infile, \
        open(output_file, "w", encoding="utf-8") as outfile:

        for line in infile:
            data = json.loads(line)

            if data.get("label") == "bad":
                filtered = {
                "url": data.get("url"),
                "label": data.get("label")
                }
                outfile.write(json.dumps(filtered) + "\n")

    print("Filtered bad links saved.")

def populate_bloom_filter():
    '''
    Populates Bloom Filter
    '''
    hash_algo, bit_array_path = bloom_filter_args()

    bf = BloomFilter(hash_algorithm=hash_algo)

    with open("data/filtered_malicious_webpages.json", "r") as f:
        for line in f:
            obj = json.loads(line)
            url = obj.get("url", "").strip()
            if not url:
                continue

            bf.add(url)
        
    print(f"Fill Ratio: {bf.get_fill_ratio()}, Bits Set: {bf.get_num_bits_set()}")
    bf.save_bit_array(bit_array_path)
    print("Saved bit array")

def check_accuracy():
    '''
    Checks accuracy of specified hash algorithm
    '''
    start_time = time.time()

    hash_algo, bit_array_path = bloom_filter_args()
    bf = BloomFilter(hash_algorithm=hash_algo)
    bf.load_bit_array(bit_array_path)

    false_pos = 0
    false_neg = 0
    true_neg = 0
    true_pos = 0

    # Go through each line in JSON file to get classification, update accuracy counts
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
                else:
                    false_neg += 1

    end_time = time.time()

            
    print(f"True Neg: {true_neg}, False Neg: {false_neg}, True Pos: {true_pos}, False Pos: {false_pos}")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")

    # Plot confusion matrix
    conf_matrix = np.array([[true_pos, false_pos],
                            [false_neg, true_neg]])

    labels = conf_matrix

    plt.figure(figsize=(6,5))
    sns.heatmap(conf_matrix, annot=labels, fmt='', cmap='Blues', cbar=False,
                xticklabels=['Predicted Bad', 'Predicted Good'],
                yticklabels=['Actual Bad', 'Actual Good'])
    plt.title("Confusion Matrix")
    plt.show()