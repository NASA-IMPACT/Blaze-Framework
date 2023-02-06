from swiftclient.service import SwiftService, SwiftError
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
import requests
from datetime import datetime, timedelta

CONTAINER_NAME = ""
SWIFT_OPTS = {
    "auth_version": "3",
    "os_auth_url": "",
    "os_user_domain_name": "",
    "os_project_domain_name": "",
    "os_tenant_name": "",
    "os_tenant_id": "",
    "os_region_name": "",
    "os_username": "",
    "os_password": "",
}

CATALOGUE_URL = ""
maximum_processing_files = 20000

def resolve_unsealing_files(**context):
    response = requests.get( CATALOGUE_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_state=unsealing")
    unsealing_file_objects = response.json()

    if len(unsealing_file_objects) == 0:
        print("No files in unsealing state")
        return

    with SwiftService(SWIFT_OPTS) as swift:

        container = CONTAINER_NAME

        unsealing_files = []
        for seal_file in unsealing_file_objects:
            unsealing_files.append(seal_file["source_path"])

        header_data = {}
        stats_it = swift.stat(container=container, objects=unsealing_files)
        for stat_res in stats_it:
            if stat_res['success']:
                header_data[stat_res['object']] = stat_res['headers']
            else:
                print('Failed to retrieve stats for %s' % stat_res['object'])


        for seal_file in unsealing_file_objects:
            file_name = seal_file["source_path"]
            if file_name in header_data:
                if "x-ovh-retrieval-state" in header_data[file_name]:
                    sealed_state = header_data[file_name]["x-ovh-retrieval-state"]
                    # print("File ", file_name + " is ", sealed_state)

                    if sealed_state == "sealed":
                        requests.patch(CATALOGUE_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "SEALED"})

                    elif sealed_state == "unsealed":
                        requests.patch(CATALOGUE_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALED"})

                    elif sealed_state == "unsealing":
                        requests.patch(CATALOGUE_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALING"})


def list_sealed_files(**context):
    response = requests.get(CATALOGUE_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_state=SEALED")
    sealed_files = response.json()
    #print("Total sealed files:")
    #print(sealed_files)
    context['ti'].xcom_push(key="sealed_files", value = sealed_files)

def list_unsealing_files(**context):
    response = requests.get(CATALOGUE_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_state=UNSEALING")
    unsealing_files = response.json()
    #print("Total unsealing files:")
    #print(unsealing_files)
    context['ti'].xcom_push(key="unsealing_files", value = unsealing_files)

def get_total_processing_files(**context):
    response = requests.get(CATALOGUE_URL + "/catalogue/count/?transfer_status=NOT_STARTED&sealed_state=UNSEALED")
    total_processing_files = int(response.json()['count'])
    response = requests.get(CATALOGUE_URL + "/catalogue/count/?transfer_status=NOT_STARTED&sealed_state=UNSEALING")
    total_processing_files += int(response.json()['count'])
    response = requests.get(CATALOGUE_URL + "/catalogue/count/?transfer_status=IN_PROGRESS&sealed_state=UNSEALED")
    total_processing_files += int(response.json()['count'])
    context['ti'].xcom_push(key="total_processing_files", value = total_processing_files)

def process_sealed_files(**context):
    container = CONTAINER_NAME

    with SwiftService(SWIFT_OPTS) as swift:

        sealed_files_objects = context['ti'].xcom_pull(key="sealed_files")
        unsealing_files_objects = context['ti'].xcom_pull(key="unsealing_files")
        total_processing_files = int(context['ti'].xcom_pull(key="total_processing_files"))
        print("Total processing files " ,total_processing_files)

        remaining_processing_files = maximum_processing_files - total_processing_files

        if remaining_processing_files <= 0:
            print("There are still {} files to be processed.".format(remaining_processing_files))
            return

        unsealing_files_objects.extend(sealed_files_objects)
        sealed_files_objects = unsealing_files_objects[:remaining_processing_files]


        if len(sealed_files_objects) == 0:
            print("No files to process")
            return

        sealed_files = []
        for seal_file in sealed_files_objects:
            sealed_files.append(seal_file["source_path"])

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
            file_name = seal_file["source_path"]
            if file_name in header_data:
                if "x-ovh-retrieval-state" in header_data[file_name]:
                    sealed_state = header_data[file_name]["x-ovh-retrieval-state"]
                    #print("File ", file_name + " is ", sealed_state)

                    if sealed_state == "sealed":
                        #print("Unsealing the file %s" % file_name)
                        sealed_list.append(seal_file)
                        sealed_name_list.append(file_name)
                        sealed_list_map[file_name] = seal_file

                    elif sealed_state == "unsealed":
                        unsealed_list.append(seal_file)
                        requests.patch(CATALOGUE_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALED"})

                    elif sealed_state == "unsealing":
                        unsealing_list.append(seal_file)
                        requests.patch(CATALOGUE_URL + "/catalogue/" + seal_file["uuid"], json= {"sealed_state": "UNSEALING"})


        download_it = swift.download(
                    container=container,
                    objects=sealed_name_list)

        for down_res in download_it:
            if "response_dict" in down_res:
                if "headers" in down_res["response_dict"]:
                    if "retry-after" in down_res["response_dict"]["headers"]:
                        retry_seconds = down_res["response_dict"]["headers"]["retry-after"]
                        #print("For file " + down_res["path"] + ". Retry-After: %s" % retry_seconds)
                        unseal_time = datetime.now() + timedelta(seconds=int(retry_seconds))
                        requests.patch(CATALOGUE_URL + "/catalogue/" + sealed_list_map[down_res["path"]]["uuid"], json= {"sealed_state": "UNSEALING", "unseal_time": str(unseal_time)})
                    else:
                        print("Not Retry-After header %s" % down_res["path"])
                else:
                    print("Failed to fetch headers %s" % down_res["path"])
            else:
                print('Failed to fetch response dict %s' % down_res['path'])



with DAG(dag_id="hls-nasa-cold-to-hot-workflow", start_date=datetime(2023,1,1), schedule_interval="*/3 * * * *", catchup=False) as dag:

    task0 = PythonOperator(task_id="resolve_unsealing_files", python_callable=resolve_unsealing_files)

    task1 = PythonOperator(task_id="list_sealed_files", python_callable=list_sealed_files)
    task2 = PythonOperator(task_id="list_unsealing_files", python_callable=list_unsealing_files)
    task3 = PythonOperator(task_id="get_total_processing_files", python_callable=get_total_processing_files)
    task4 = PythonOperator(task_id="process_sealed_files", python_callable=process_sealed_files)

task0 >> task1 >> task2 >> task3 >> task4
