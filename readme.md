# Projeto de Engenharia de Dados: Pipeline de ETL de Big Data com PySpark e Databricks

![Databricks](https://img.shields.io/badge/Databricks-Community-FF5722?logo=databricks)
![PySpark](https://img.shields.io/badge/Apache%20Spark-3.4-E25A1C?logo=apache-spark)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)

Este projeto demonstra a construção de um pipeline de ETL (Extração, Transformação e Carga) de ponta a ponta em um ambiente de **Big Data**, utilizando **PySpark** na plataforma **Databricks Community Edition**. O objetivo é processar um grande volume de dados de corridas de táxi de Nova York, desde a ingestão até a análise e o armazenamento em um formato otimizado.

Este projeto destaca habilidades em **Engenharia de Dados**, processamento distribuído, otimização de performance e resolução de problemas em ambientes de nuvem.

---

## 🚀 Arquitetura e Fluxo do Pipeline

O projeto foi desenvolvido inteiramente dentro de um Notebook no Databricks, seguindo estas etapas:

1.  **Extração (E):** Ingestão de dois datasets públicos: um arquivo Parquet com milhões de registros de corridas (`yellow_tripdata`) e um arquivo CSV com o mapeamento das zonas de táxi (`taxi_zone_lookup`).
2.  **Transformação (T):** Utilização de **PySpark** para realizar uma série de transformações no DataFrame:
    *   Limpeza e renomeação de colunas para padronização.
    *   **JOINs** para enriquecer os dados das corridas com os nomes legíveis das zonas de embarque e desembarque.
    *   **Engenharia de Features:** Criação de novas colunas de valor para o negócio, como `duracao_corrida_min`, `dia_da_semana` e `hora_do_dia`.
    *   Filtragem de dados inconsistentes para garantir a qualidade da análise.
3.  **Análise (A):** Uso de **Spark SQL** para realizar consultas agregadas diretamente no DataFrame transformado, respondendo a perguntas de negócio como "Quais as rotas mais populares?" e "Qual o valor médio das corridas por bairro?".
4.  **Carga (L):** O DataFrame final, limpo e enriquecido, é salvo como uma **tabela gerenciada** no Databricks (`corridas_nyc_enriquecidas`), pronta para ser consumida por analistas de dados, cientistas de dados ou ferramentas de BI.

---

## 🛠️ Tecnologias Utilizadas

*   **Plataforma Cloud:** Databricks Community Edition
*   **Processamento de Big Data:** Apache Spark (via PySpark)
*   **Linguagem:** Python e Spark SQL
*   **Formatos de Dados:** Parquet, CSV

---

## 📈 Principais Desafios e Aprendizados

*   **Configuração de Ambiente:** Navegar pelas particularidades e limitações da Databricks Community Edition, especialmente em relação ao Unity Catalog vs. Hive Metastore e as permissões de escrita em diferentes sistemas de arquivos (DBFS vs. Volumes).
*   **Sintaxe do PySpark:** Adaptação da lógica de manipulação de dados do Pandas para a sintaxe funcional e distribuída do PySpark.
*   **Otimização:** Entendimento prático de como o Spark executa as transformações de forma "preguiçosa" (lazy evaluation) e a importância de salvar os resultados em formatos colunares como Parquet.

---

## ⚙️ Como Reproduzir (Visão Geral)

O código completo está disponível no arquivo `pipeline_nyc_taxi.py`. Para reproduzir, os passos gerais são:
1.  Criar uma conta na Databricks Community Edition.
2.  Fazer o upload dos datasets para o ambiente Databricks.
3.  Criar um cluster e um notebook.
4.  Adaptar os caminhos dos arquivos no código e executar as células em ordem.

*Este projeto focou na lógica de ETL e análise, e não na reprodutibilidade via clone, devido às particularidades do ambiente Databricks.*
