from swiftclient.service import SwiftService, SwiftError
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
import requests
from datetime import datetime, timedelta

CATALOG_URL="http://example.com:5000"

def list_sealed_files(**context):
    response = requests.get(CATALOG_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_State=sealed")
    sealed_files = response.json()
    print(sealed_files)
    context['ti'].xcom_push(key="sealed_files", value = sealed_files)

def list_unsealing_files(**context):
    response = requests.get(CATALOG_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_State=unsealing")
    unsealing_files = response.json()
    print(unsealing_files)
    context['ti'].xcom_push(key="unsealing_files", value = unsealing_files)

def process_sealed_files(**context):
    container = ""
    minimum_size = 10*1024**2

    opts = {
        "auth_version": "3",
        "os_auth_url": "",
        "os_project_name": "",
        "os_project_id": "",
        "os_user_domain_name": "",
        "os_region_name": "",
        "os_username": "",
        "os_password": "",
    }

    with SwiftService(opts) as swift:

        sealed_files_objects = context['ti'].xcom_pull(key="sealed_files")
        unsealing_files_objects = context['ti'].xcom_pull(key="unsealing_files")
        sealed_files_objects.extend(unsealing_files_objects)

        if len(sealed_files_objects) == 0:
            print("No files to process")
            return
            
            
        sealed_files = []
        for seal_file in sealed_files_objects:
            sealed_files.append(seal_file["name"])

        header_data = {}
        stats_it = swift.stat(container=container, objects=sealed_files)
        for stat_res in stats_it:
            if stat_res['success']:
                header_data[stat_res['object']] = stat_res['headers']
            else:
                print('Failed to retrieve stats for %s' % stat_res['object'])

        sealed_list = []
        sealed_name_list = []
        sealed_list_map = {}
        unsealing_list = [] 
        unsealed_list = []

        for seal_file in sealed_files_objects:
            file_name = seal_file["name"]
            if file_name in header_data:
                if "x-ovh-retrieval-state" in header_data[file_name]:
                    sealed_state = header_data[file_name]["x-ovh-retrieval-state"]
                    print("File ", file_name + " is ", sealed_state)
                    
                    if sealed_state == "sealed":
                        print("Unsealing the file %s" % file_name)
                        sealed_list.append(seal_file)
                        sealed_name_list.append(file_name)
                        sealed_list_map[file_name] = seal_file
                        
                    elif sealed_state == "unsealed":
                        unsealed_list.append(seal_file)
                        requests.patch(CATALOG_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALED"})

                    elif sealed_state == "unsealing":
                        unsealing_list.append(seal_file)
                        requests.patch(CATALOG_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALING"})


        download_it = swift.download(
                    container=container,
                    objects=sealed_name_list)

        for down_res in download_it:
            if "response_dict" in down_res:
                if "headers" in down_res["response_dict"]:
                    if "retry-after" in down_res["response_dict"]["headers"]:
                        retry_seconds = down_res["response_dict"]["headers"]["retry-after"]
                        print("For file " + down_res["path"] + ". Retry-After: %s" % retry_seconds)
                        unseal_time = datetime.now() + timedelta(seconds=int(retry_seconds))
                        requests.patch(CATALOG_URL + "/catalogue/" + sealed_list_map[down_res["path"]]["uuid"], json= {"sealed_state": "UNSEALING", "unseal_time": str(unseal_time)})
                    else:
                        print("Not Retry-After header %s" % down_res["path"])
                else:
                    print("Failed to fetch headers %s" % down_res["path"])
            else:
                print('Failed to fetch response dict %s' % down_res['path'])



with DAG(dag_id="hls-nasa-cold-storage", start_date=datetime(2021,1,1), schedule_interval=None, catchup=False) as dag:
    task1 = PythonOperator(task_id="list_sealed_files", python_callable=list_sealed_files)
    task2 = PythonOperator(task_id="list_unsealing_files", python_callable=list_unsealing_files)
    task3 = PythonOperator(task_id="process_sealed_files", python_callable=process_sealed_files)

task1 >> task2 >> task3