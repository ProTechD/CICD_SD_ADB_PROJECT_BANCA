# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

dbutils.widgets.text("container", "raw")
dbutils.widgets.text("catalogo", "catalog_au")
dbutils.widgets.text("esquema", "bronze")
dbutils.widgets.text("storageName", "adlsmartdata1207")

# COMMAND ----------

container = dbutils.widgets.get("container")
catalogo = dbutils.widgets.get("catalogo")
esquema = dbutils.widgets.get("esquema")
storageName = dbutils.widgets.get("storageName")

ruta = f"abfss://{container}@{storageName}.dfs.core.windows.net/transacciones.csv"

# COMMAND ----------

transacciones_schema = StructType(fields=[StructField("transaccionid", IntegerType(), False),
                                  StructField("cuentaid", IntegerType(), True),
                                  StructField("fecha", DateType(), True),
                                  StructField("tipo", StringType(), True),
                                  StructField("monto", DoubleType(), True)
])

# COMMAND ----------

transacciones_df = spark.read \
            .option("header", True) \
            .schema(transacciones_schema) \
            .csv(ruta)


# COMMAND ----------

transacciones_selected_df = transacciones_df.select(col('transaccionid').alias('transaccion_id'), 
                                                   col('cuentaid').alias('cuenta_id'), 
                                                   col('fecha'), col('tipo'),
                                                   col('monto'))

# COMMAND ----------

transacciones_selected_df.write \
    .mode("overwrite") \
    .insertInto(f"{catalogo}.{esquema}.transacciones")

# COMMAND ----------

#spark.table(f"{catalogo}.{esquema}.transacciones").display()
