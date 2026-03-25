from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from datetime import datetime
import binascii
import json

sc = SparkContext()
ssc = StreamingContext(sc, 10)

def process_rdd(rdd):
    if rdd.isEmpty():
        return
    
    lines = list(set(rdd.collect()))
    urls = []
    for line in lines:
        obj = json.loads(line)
        url = obj.get("url", "").strip()
        if url:
            urls.append(url)
 
 
    false_pos_rate = "not implemented"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("output.csv", "a") as f:
        f.write(f"{timestamp},{false_pos_rate}\n")


if __name__ == "__main__":
    with open("output.csv", "w") as f:
        f.write("Time,FPR\n")
    lines = ssc.socketTextStream("localhost", 9999)
    lines.foreachRDD(process_rdd)
    ssc.start()
    ssc.awaitTermination()




