import pandas as pd
import logging 
import time
from extract import config
from google.cloud import bigquery


# Init client
client = bigquery.Client()

def get_max_id(client, table_name, project_id = "saas-pipeline", dataset = "raw_src"):
    """
    Fetch max unique id from the bigquery table
    """
    id_col = config.UNIQUE_KEYS[table_name]
    table_id = f"{project_id}.{dataset}.{table_name}"

    query = f"SELECT COALESCE(MAX({id_col}), 0) AS max_id FROM `{table_id}`"
    result = list(client.query(query).result())[0]
    return result.max_id

def load_to_biquery(df, table_name, project_id = "saas-pipeline", dataset = "raw_src"):
    """
    Appends a pandas DataFrame to bigquery table.
    """
    table_id = f"{project_id}.{dataset}.{table_name}"
    table = client.get_table(table_id)
    schema = table.schema

    job_config = bigquery.LoadJobConfig(
        schema = schema,
        create_disposition = "CREATE_NEVER"
    )

    # deciding if to load static tables (products, plans, and discounts) or no 
    if table_name in config.STATIC_TABLES:
        # compare row counts
        query = f"SELECT COUNT(*) AS cnt FROM `{table_id}`"
        result = list(client.query(query).result())[0]
        bq_count = result.cnt
        local_count = len(df)
        
        # Checking if a new product / plan / discount has been added, if yes append to existing table
        if bq_count != local_count:
            job_config.write_disposition = "WRITE_APPEND"
            print(f"Updating static table {table_name} from {bq_count} rows to {local_count} rows")

        # If no change then do not load any data
        else:
            print(f"No changes in {table_name}, skipping load")
            return 0
    else:
        job_config.write_disposition = 'WRITE_APPEND'
    
    start_time = time.perf_counter()
    try:
        logging.info(f"Starting load for {table_id} | {len(df)} rows ")
        job = client.load_table_from_dataframe(df, table_id, job_config = job_config)
        result = job.result()
        print("BigQuery inserted rows:", result.output_rows)
        print(f"Loaded {result.output_rows} rows into {table_id}")
        print("Errors:", job.errors)

        duration = time.perf_counter() - start_time
        logging.info(
            f"Loaded {len(df)} rows into {table_id} |"
            f"Duration: {duration: .2f} sec"
            )
        return len(df)
        
    except Exception as e:
        duration = time.perf_counter() - start_time
        logging.error(f"Failed to load {table_name} after {duration: .2f} sec: {e}", exc_info = True)
        raise

