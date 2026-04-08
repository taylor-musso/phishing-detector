from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
from bloom_filter import BloomFilter 
import json 

sc = SparkContext() 
sc.setLogLevel("ERROR") 
ssc = StreamingContext(sc, 10) 

bf = BloomFilter() 
bf.load_bit_array("bit_filter.csv") 

false_pos = 0 
true_neg = 0 
true_pos = 0

def process_rdd(rdd): 
    global bf, false_pos, true_neg, true_pos
    
    if rdd.isEmpty(): 
        return 
    
    lines = list(set(rdd.collect())) 
    
    
    for line in lines: 
        obj = json.loads(line) 
        url = obj.get("url", "").strip() 
        if not url: 
            continue 
        
        is_malicious = bf.check(url)
        link_type = obj.get("label", "").strip()
        if is_malicious:
            if link_type == "good":
                false_pos += 1
            else:
                true_pos += 1
        else:
            if link_type == "good":
                true_neg += 1
            
        
    print(f"False Positives: {false_pos}, True Negatives: {true_neg}, True Positives: {true_pos}")
    with open("output.csv", "a") as f: 
        f.write(f"{false_pos},{true_neg}\n") 
            
if __name__ == "__main__": 
    with open("output.csv", "w") as f:
        f.write("FP,TN\n") 
        lines = ssc.socketTextStream("localhost", 9999) 
        lines.foreachRDD(process_rdd) 
        ssc.start() 
        ssc.awaitTermination()