# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

sales_df = spark.table(
    "retail_catalog.bronze.sales_raw"
)

store_df = spark.table(
    "retail_catalog.bronze.store_raw"
)

# COMMAND ----------

sales_df=spark.table("retail_catalog.bronze.sales_raw")

# COMMAND ----------

store_df=spark.table("retail_catalog.bronze.store_raw")

# COMMAND ----------

sales_df.count()
store_df.count()


# COMMAND ----------

from pyspark.sql.functions import col
sales_df.filter(

    col("Store").isNull()
).count()

# COMMAND ----------

sales_clean=(
    sales_df

    .withColumn("year",year(col("Date")))
    .withColumn("month",month(col("Date")))
    .withColumn("week",weekofyear(col("Date")))
    .withColumn("quater",quarter(col("Date")))
    .withColumn("day",dayofmonth(col("Date")))
    .withColumn("is_open", col("Open").cast(BooleanType()))
    .withColumn("is_promo", col("Promo").cast(BooleanType()))
    .withColumn("is_school_holiday",when(col("SchoolHoliday") != "0" , True).otherwise(False))
    .withColumn(
        "is_state_holiday",
        when(
            col("StateHoliday").isin("a","b","c"),
            True
        ).otherwise(False))
)



# COMMAND ----------

sales_clean.printSchema()
display(sales_clean.limit(10))

# COMMAND ----------

median_distance=store_df.approxQuantile(
    "CompetitionDistance",
    [0.5],0.01
)[0]

# COMMAND ----------

store_clean=(
    store_df

    .fillna({
        "CompetitionDistance": median_distance
    })

    .withColumn("competition_info_available",
                when(col("CompetitionOpenSinceYear").isNull(),False).otherwise(True))
    .withColumn(
        "has_promo2",
        col("Promo2").cast(BooleanType())
    )

    .withColumn(
        "store_type",
        upper(col("StoreType"))
    )

        .withColumn(
        "assortment_type",
        upper(col("Assortment"))
    )

)



# COMMAND ----------

store_clean.printSchema()

# COMMAND ----------

display(store_clean.limit(10))

# COMMAND ----------

sales_clean.select("StateHoliday").distinct().show(20, False)

# COMMAND ----------

sales_clean.filter(
    col("StateHoliday").isNotNull()
).select("StateHoliday").distinct().show()

# COMMAND ----------

sales_df.groupBy("StateHoliday").count().show(20, False)

# COMMAND ----------

sales_clean = (
    sales_clean
    .drop("quater")
    .withColumn(
        "quarter",
        quarter(col("Date"))
    )
)

# COMMAND ----------

spark.table(
    "retail_catalog.silver.sales_clean"
).printSchema()

# COMMAND ----------

spark.sql("""
DROP TABLE IF EXISTS retail_catalog.silver.sales_clean
""")

# COMMAND ----------

sales_clean.write\
    .format("delta")\
    .mode("overwrite")\
    .saveAsTable("retail_catalog.silver.sales_clean")

# COMMAND ----------

store_clean.write\
    .format("delta")\
        .mode("overwrite")\
            .saveAsTable("retail_catalog.silver.store_clean")

# COMMAND ----------

sales_silver = spark.table(
    "retail_catalog.silver.sales_clean"
)

store_silver = spark.table(
    "retail_catalog.silver.store_clean"
)

# COMMAND ----------

print(
    sales_silver.count()
)

print(
    store_silver.count()
)

# COMMAND ----------

sales_silver.printSchema()

store_silver.printSchema()

# COMMAND ----------

store_silver.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in store_silver.columns
]).display()

# COMMAND ----------

sales_silver.printSchema()

store_silver.printSchema()