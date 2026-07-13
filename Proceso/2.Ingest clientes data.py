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

ruta = f"abfss://{container}@{storageName}.dfs.core.windows.net/clientes.csv"

# COMMAND ----------

df_clientes = spark.read.option('header', True)\
                        .option('inferSchema', True)\
                        .csv(ruta)

# COMMAND ----------

clientes_schema = StructType(fields=[StructField("clienteid", IntegerType(), False),
                                     StructField("nombre", StringType(), True),
                                     StructField("apellido", StringType(), True),
                                     StructField("dni", StringType(), True),
                                     StructField("fechanacimiento", DateType(), True),
                                     StructField("ciudad", StringType(), True)
])

# COMMAND ----------

# DBTITLE 1,Use user specified schema to load df with correct types
df_clientes_final = spark.read\
.option('header', True)\
.schema(clientes_schema)\
.csv(ruta)

# COMMAND ----------

# DBTITLE 1,select only specific cols
clientes_selected_df = df_clientes_final.select(col("clienteid"), 
                                                col("nombre"), 
                                                col("apellido"), 
                                                col("dni"), 
                                                col("fechanacimiento"), 
                                                col("ciudad"))

# COMMAND ----------

clientes_renamed_df = clientes_selected_df.withColumnRenamed("clienteid", "cliente_id") \
                                            .withColumnRenamed("fechanacimiento", "fec_nacimiento")


# COMMAND ----------

clientes_renamed_df.write.mode("overwrite").insertInto(f"{catalogo}.{esquema}.clientes")

# COMMAND ----------

#spark.table(f"{catalogo}.{esquema}.clientes").display()
