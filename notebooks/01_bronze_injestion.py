# Databricks notebook source
sales_df = spark.read.csv(
    "/Volumes/retail_catalog/bronze/raw_files/train.csv",
    header=True,
    inferSchema=True
)

display(sales_df)

# COMMAND ----------

sales_df.printSchema()

# COMMAND ----------

store_df = spark.read.csv(
    "/Volumes/retail_catalog/bronze/raw_files/store.csv",
    header=True,
    inferSchema=True
)

display(store_df)

# COMMAND ----------

print(sales_df.count())

print(store_df.count())

# COMMAND ----------

sales_df.write.mode("overwrite").format("delta").saveAsTable("retail_catalog.bronze.sales_raw")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_catalog.bronze.sales_raw
# MAGIC LIMIT 10;

# COMMAND ----------

store_df.write.mode("overwrite").format("delta").saveAsTable("retail_catalog.bronze.store_raw")