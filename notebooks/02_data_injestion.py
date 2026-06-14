# Databricks notebook source
sales_df = spark.table(
    "retail_catalog.bronze.sales_raw"
)

store_df = spark.table(
    "retail_catalog.bronze.store_raw"
)

# COMMAND ----------

sales_df.count()

sales_df.printSchema()

display(sales_df)

# COMMAND ----------

# Read Bronze Tables

sales_df = spark.table(
    "retail_catalog.bronze.sales_raw"
)

store_df = spark.table(
    "retail_catalog.bronze.store_raw"
)

print("Sales Rows:", sales_df.count())
print("Store Rows:", store_df.count())

sales_df.printSchema()
store_df.printSchema()

display(sales_df.limit(10))
display(store_df.limit(10))

# COMMAND ----------

from pyspark.sql.functions import *
display(sales_df.select([count(when(col(c).isNull(), c)).alias(c) for c in sales_df.columns]))



# COMMAND ----------

display(store_df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in store_df.columns
]))

# COMMAND ----------

sales_df.groupBy(
    "Store",
    "Date"
).count().filter(
    col("count") > 1
).count()

# COMMAND ----------

store_df.groupBy(
    "Store"
).count().filter(
    col("count") > 1
).count()

# COMMAND ----------

sales_df.select(
    countDistinct("Store")
).show()

# COMMAND ----------

sales_df.select(
    min("Date"),
    max("Date")
).show()

# COMMAND ----------

sales_df.groupBy(
    "Open"
).count().display()

# COMMAND ----------

sales_df.describe(
    ["Sales"]
).display()

# COMMAND ----------

sales_df.filter(
    (col("Open") == 1) &
    (col("Sales") == 0)
).count()

# COMMAND ----------

store_df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in [
        "CompetitionDistance",
        "CompetitionOpenSinceMonth",
        "CompetitionOpenSinceYear"
    ]
]).display()

# COMMAND ----------

store_df.groupBy(
    "Promo2"
).count().display()

# COMMAND ----------

joined_df = sales_df.join(
    store_df,
    "Store",
    "left"
)

# COMMAND ----------

joined_df.filter(
    col("StoreType").isNull()
).count()

# COMMAND ----------


from pyspark.sql.functions import *

store_df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in store_df.columns
]).display()

# COMMAND ----------

store_df.groupBy("Promo2").count().display()