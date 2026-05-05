# Phishing Detector
*Taylor Musso, Jeron Alford, Tattimbet Zakaryia*

## Setup Instructions
### Data
The data files were too large to be pushed to GitHub, so they can be downloaded from this [box link](https://lmu.box.com/s/449gqqjbu15knftsbm6e5k7ljqb6sb99). When unzipped, it should create a folder named **data** that should be placed into the directory. 

### Data Processing
All of the data proccessing is already done and currently in the repository where it needs to be. If you want to recreate all of this, you can delete all files in **bit_array/** as well as the two CSV files in **data/**

Then run setup.py as specified:

`python setup.py --murmur  # To use the MurmurHash3 function`

or

`python setup.py --jenkins  # To use the Jenkins Hash function`

Default if no tag is used will be MurmurHash3.

You cannot change the hash function used while inside of this program, so press 4 to exit and run the command again with the other tag. Option 1 (Process Dataset) is not dependent on hash function, and only needs to be run once. Options 2 (Populate Bloom Filter) and 3 (Check Accuracy) will have to be run for both Bloom Filters.

### Streaming
This should be run on two separate terminal windows, one which runs

`java -cp stream.jar StreamSimulation data/webpages_classification.json 9999 100 `

and another that runs either:

`spark-submit phishing_detector.py 9999 --murmur`

or 

`spark-submit phishing_detector.py 9999 --jenkins`

Default if no tag is used will be MurmurHash3.

### Reports
All reports have been submitted to Brightspace but are also uploaded here in **reports/**.
