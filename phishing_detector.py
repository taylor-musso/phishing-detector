from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from datetime import datetime
import json
import mmh3

sc = SparkContext()
ssc = StreamingContext(sc, 10)

m = 50000
k = 7   
bit_array = [0] * m

seen_urls = set()

def hash_funcs(url):
    return [mmh3.hash(url, seed=i) % m for i in range(k)]

def process_rdd(rdd):
    global bit_array, seen_urls

    if rdd.isEmpty():
        return
    
    lines = list(set(rdd.collect()))
    urls = []
    for line in lines:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if url:
            urls.append(url)
    
    false_pos = 0
    true_neg = 0

    for url in urls:
        indices = hash_funcs(url)
        in_filter = all(bit_array[i] == 1 for i in indices)
        seen = url in seen_urls

        if in_filter:
            if not seen:
                false_pos += 1
        else:
            if not seen:
                true_neg += 1

        for i in indices:
            bit_array[i] = 1

        seen_urls.add(url)

    denominator = false_pos + true_neg
    false_pos_rate = false_pos / denominator if denominator > 0 else 0.0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _ in range(40):
        print("-------------------")

    with open("output.csv", "a") as f:
        f.write(f"{timestamp},{false_pos_rate}\n")
    with open("bit_filter.csv", "a") as file:
        file.write(f"{timestamp},{sum(bit_array)}\n")


if __name__ == "__main__":
    with open("output.csv", "w") as f:
        f.write("Time,FPR\n")
    
    with open("bit_filter.csv", "w") as file:
        file.write("Time, Bit Filter\n")
 
    lines = ssc.socketTextStream("localhost", 9999)
    lines.foreachRDD(process_rdd)

    ssc.start()
    ssc.awaitTermination()