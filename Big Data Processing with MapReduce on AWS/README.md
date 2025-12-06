# Big Data Processing with MapReduce on AWS (NYC Yellow Taxi — Payment Type Distribution)

This project analyzes large-scale **NYC Yellow Taxi trip records (March 2016)** using **Hadoop MapReduce on AWS** to compute the distribution of **payment types** at scale.

---

## Objective

Analyze NYC Yellow Taxi trip CSV data using **Java Hadoop MapReduce** on an **AWS-hosted Hadoop cluster** to efficiently aggregate **payment_type counts**.

---

## Motivation

- Demonstrate **distributed big-data processing** in a real cloud environment (AWS).
- Practice end-to-end Hadoop workflows: **HDFS, YARN, MapReduce**
- Improve job runtime with practical **Hadoop performance tuning**.

---

## Tech Stack

- **AWS EC2** (cluster nodes), AWS CLI, SSH
- **Hadoop 3.2.2**
  - **HDFS** for distributed storage
  - **YARN** for job scheduling/resource management
  - **MapReduce** for distributed compute
- **Java** (Mapper, Reducer, Driver)
- Linux shell tools (scp, ssh, hdfs dfs, yarn, javac, jar)

---

## Dataset

- **NYC Yellow Taxi Trip Records — March 2016** (CSV)
- Input is large and processed using HDFS + MapReduce
- Important column used:
  - `payment_type` (field index **11**, 0-based indexing)

---

## Methodology

### 1) AWS + Hadoop Setup
- Provisioned and managed a Hadoop environment on **AWS EC2**
- Used **AWS CLI / SSH** for access and administration
- Uploaded dataset to **HDFS** and executed MapReduce on **YARN**

### 2) MapReduce Implementation (Java)
A complete pipeline was built:

#### Mapper — `PaymentTypeMapper.java`
- Reads each CSV line
- Skips the header (lines starting with `VendorID`)
- Splits by commas; validates at least 12 fields
- Emits:
  - **Key:** `payment_type` (Text)
  - **Value:** `1` (IntWritable)

Output pairs:
(payment_type, 1)


#### Reducer — `PaymentTypeReducer.java`
- Aggregates values for each `payment_type`
- Sums all `1`s
- Emits:


(payment_type, totalCount)


#### Combiner
- Used a **Combiner (same logic as Reducer)** to reduce shuffle volume.

#### Driver — `YellowTripDriver.java`
- Sets mapper / combiner / reducer classes
- Sets input and output paths
- Submits job to YARN and waits for completion

### 3) Performance Tuning
- Tuned Hadoop settings to improve throughput:
  - Adjusted **split size** (e.g., 64MB)
  - Enabled **speculative execution** to reduce stragglers
- Observed that using a single reducer can create a shuffle bottleneck (especially in small clusters)

---

## Results

Processed March 2016 dataset and computed the payment type distribution:

| payment_type | Meaning       | Count     |
|-------------|---------------|-----------|
| 1           | Credit Card   | 8,127,391 |
| 2           | Cash          | 4,020,408 |
| 3           | No Charge     | 46,913    |
| 4           | Dispute       | 16,240    |

✅ Achieved **~15% throughput improvement** after tuning split size and enabling speculative execution.

---



---

## Compilation & Execution (Typical Commands)

> Commands may vary depending on your cluster paths and environment.

### Compile Java
```bash
mkdir -p build
javac -classpath `hadoop classpath` -d build src/*.java
jar -cvf yellowtrip.jar -C build/ .
Upload input to HDFS
hdfs dfs -mkdir -p /input/yellowtrip
hdfs dfs -put yellow_tripdata_2016-03.csv /input/yellowtrip/

Run MapReduce job
hadoop jar yellowtrip.jar YellowTripDriver /input/yellowtrip /output/payment_type_counts

View output
hdfs dfs -cat /output/payment_type_counts/part-r-00000 | head

Copy output locally (optional)
hdfs dfs -get /output/payment_type_counts ./results
