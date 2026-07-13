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

ruta = f"abfss://{container}@{storageName}.dfs.core.windows.net/cuentas.csv"

# COMMAND ----------

cuentas_schema = StructType(fields=[
    StructField("cuentaid", IntegerType(), False),
    StructField("clienteid", IntegerType(), True),
    StructField("tipocuenta", StringType(), True),
    StructField("fechaapertura", DateType(), True),
    StructField("saldo", DoubleType(), True)
])

# COMMAND ----------

df_clientes_final = spark.read\
.option('header', True)\
.schema(cuentas_schema)\
.csv(ruta)


# COMMAND ----------

cuentas_final_df = df_clientes_final.select(
    col("cuentaid").alias("cuenta_id"),
    col("clienteid").alias("cliente_id"),
    col("tipocuenta").alias("tipo_cuenta"),
    col("fechaapertura").alias("fec_apertura"),
    col("saldo")
)

# COMMAND ----------

cuentas_final_df.write \
    .mode("overwrite") \
    .insertInto(f"{catalogo}.{esquema}.cuentas")

# COMMAND ----------

#spark.table(f"{catalogo}.{esquema}.cuentas").display()
