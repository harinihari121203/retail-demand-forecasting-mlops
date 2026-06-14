# Databricks notebook source
from pyspark.sql.functions import *

sales_df=spark.table("retail_catalog.silver.sales_clean")

weather_df=(sales_df
            .select("Date").distinct())

# COMMAND ----------

print(weather_df.count())

# COMMAND ----------

weather_df=(
    weather_df
    .withColumn("year",year("Date"))
    .withColumn("month",month("Date"))
    .withColumn("quarter",quarter("Date"))
)

# COMMAND ----------

weather_df = (
    weather_df
    .withColumn(
        "temperature",
        when(col("month").isin(12,1,2),
             round(rand()*8 + 1,2))
        .when(col("month").isin(3,4,5),
             round(rand()*10 + 8,2))
        .when(col("month").isin(6,7,8),
             round(rand()*12 + 18,2))
        .otherwise(
             round(rand()*10 + 10,2))
    )
)

# COMMAND ----------

weather_df = (
    weather_df
    .withColumn(
        "humidity",
        when(
            col("month").isin(11,12,1,2),
            round(rand()*20 + 70,2)
        )
        .otherwise(
            round(rand()*30 + 40,2)
        )
    )
)

# COMMAND ----------

weather_df = (
    weather_df
    .withColumn(
        "rainfall",
        when(
            col("month").isin(10,11,12),
            round(rand()*25,2)
        )
        .otherwise(
            round(rand()*10,2)
        )
    )
)

# COMMAND ----------

weather_df = (
    weather_df
    .withColumn(
        "weather_condition",
        when(col("rainfall") > 15, "Rainy")
        .when(col("temperature") > 25, "Hot")
        .when(col("temperature") < 5, "Cold")
        .otherwise("Normal")
    )
)

# COMMAND ----------

weather_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(
        "retail_catalog.silver.weather_clean"
    )

# COMMAND ----------

weather_df.printSchema()

# COMMAND ----------

display(weather_df)

# COMMAND ----------

weather_df.groupBy(
    "weather_condition"
).count().display()

# COMMAND ----------

weather_df.count()

# COMMAND ----------


weather_df.printSchema()

weather_df.groupBy(
    "weather_condition"
).count().display()