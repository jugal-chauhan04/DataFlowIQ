import pandas as pd
import logging 
import time 
from google.cloud import bigquery


# Init client
client = bigquery.Client()

def load_to_biquery(df, table_name, project_id = "saas-pipeline", dataset = "raw_src"):
    """
    Appends a pandas DataFrame to bigquery table.
    """
    table_id = f"{project_id}.{dataset}.{table_name}"
    table = client.get_table(table_id)
    schema = table.schema

    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition = "WRITE_TRUNCATE"
    )
    
    
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

