# Databricks notebook source
# Lendo os dados diretamente da tabela SQL que você criou
# O Spark SQL pode ler tabelas do catálogo diretamente
df_corridas = spark.table("workspace.default.yellow_tripdata_2023_01")

# Visualizando os dados
display(df_corridas)

# COMMAND ----------

# Lendo os dados da tabela de zonas
df_zonas = spark.table("workspace.default.taxi_zone_lookup")

# Visualizando os dados
display(df_zonas)

# COMMAND ----------

# Importando as funções que vamos usar
from pyspark.sql.functions import col, unix_timestamp, date_format, round

# Renomeando as colunas mais importantes para facilitar a manipulação
df_corridas = df_corridas.withColumnRenamed("tpep_pickup_datetime", "horario_embarque") \
                         .withColumnRenamed("tpep_dropoff_datetime", "horario_desembarque") \
                         .withColumnRenamed("passenger_count", "num_passageiros") \
                         .withColumnRenamed("trip_distance", "distancia_corrida") \
                         .withColumnRenamed("PULocationID", "id_local_embarque") \
                         .withColumnRenamed("DOLocationID", "id_local_desembarque") \
                         .withColumnRenamed("total_amount", "valor_total")

print("Colunas renomeadas com sucesso!")

# COMMAND ----------

# Precisamos dar "apelidos" (alias) para o df_zonas para o Spark não confundir as colunas
zonas_embarque = df_zonas.alias("zonas_embarque")
zonas_desembarque = df_zonas.alias("zonas_desembarque")

# Juntando df_corridas com zonas_embarque para pegar o nome do local de embarque
df_final = df_corridas.join(
    zonas_embarque,
    df_corridas.id_local_embarque == zonas_embarque.LocationID,
    "left"
).withColumnRenamed("Borough", "bairro_embarque") \
 .withColumnRenamed("Zone", "zona_embarque") \
 .drop("LocationID", "service_zone") # Remove colunas duplicadas ou desnecessárias

# Juntando o resultado com zonas_desembarque para pegar o nome do local de desembarque
df_final = df_final.join(
    zonas_desembarque,
    df_final.id_local_desembarque == zonas_desembarque.LocationID,
    "left"
).withColumnRenamed("Borough", "bairro_desembarque") \
 .withColumnRenamed("Zone", "zona_desembarque") \
 .drop("LocationID", "service_zone")

print("DataFrames juntados com sucesso!")
display(df_final.select("horario_embarque", "bairro_embarque", "zona_embarque", "bairro_desembarque", "zona_desembarque"))

# COMMAND ----------

# Calculando a duração da corrida em minutos
df_final = df_final.withColumn(
    "duracao_corrida_min",
    round((unix_timestamp(col("horario_desembarque")) - unix_timestamp(col("horario_embarque"))) / 60, 2)
)

# Extraindo o dia da semana e a hora do embarque
df_final = df_final.withColumn("dia_da_semana", date_format(col("horario_embarque"), "E")) # 'E' retorna a abreviação do dia (ex: 'Mon')
df_final = df_final.withColumn("hora_do_dia", date_format(col("horario_embarque"), "H"))

# Limpando dados inconsistentes (ex: corridas com duração negativa ou distância zero)
df_final = df_final.filter("duracao_corrida_min > 0 AND distancia_corrida > 0")


print("Novas features criadas e dados limpos!")
display(df_final.select("duracao_corrida_min", "dia_da_semana", "hora_do_dia"))

# COMMAND ----------

# Registrando o DataFrame final como uma tabela temporária para usar SQL
df_final.createOrReplaceTempView("vw_corridas_nyc")

print("View temporária 'vw_corridas_nyc' criada. Agora podemos usar Spark SQL!")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC   zona_embarque,
# MAGIC   zona_desembarque,
# MAGIC   COUNT(*) AS total_corridas
# MAGIC FROM
# MAGIC   vw_corridas_nyc
# MAGIC GROUP BY
# MAGIC   zona_embarque,
# MAGIC   zona_desembarque
# MAGIC ORDER BY
# MAGIC   total_corridas DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   bairro_embarque,
# MAGIC   ROUND(AVG(valor_total), 2) AS media_valor_total
# MAGIC FROM
# MAGIC   vw_corridas_nyc
# MAGIC WHERE
# MAGIC   bairro_embarque != 'Unknown'
# MAGIC GROUP BY
# MAGIC   bairro_embarque
# MAGIC ORDER BY
# MAGIC   media_valor_total DESC

# COMMAND ----------

# Vamos dar apenas o nome da tabela, sem especificar o catálogo ou o schema.
# O Databricks vai usar o padrão da sua sessão atual.
nome_da_tabela = "corridas_nyc_enriquecidas"

# Salvando o DataFrame como uma tabela gerenciada.
# O modo "overwrite" vai apagar e recriar a tabela a cada execução.
df_final.write.mode("overwrite").saveAsTable(nome_da_tabela)

print(f"DataFrame salvo com sucesso como a tabela: `{nome_da_tabela}`")
print("\nVocê agora pode consultar esta tabela usando SQL!")