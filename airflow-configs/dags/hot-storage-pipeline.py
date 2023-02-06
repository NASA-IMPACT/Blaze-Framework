from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

from airavata_mft_sdk import mft_client
from airavata_mft_sdk.common import StorageCommon_pb2
from airavata_mft_sdk import MFTTransferApi_pb2

import time 
from airflow.operators.dagrun_operator import TriggerDagRunOperator

TRANSFER_SUBMISSIONS_PER_ITERATION = 800
FILES_PER_TRANSFER = 50
CATALOGUE_URL = ""
MFT_HOST_IP = ""
SOURCE_STORAGE_ID = ""
DESTINATION_STORAGE_ID = ""

def fetch_pending(**context):
    print("Fetching pending transfers")
    response = requests.get(CATALOGUE_URL + "/catalogue/?transfer_status=IN_PROGRESS&sealed_state=UNSEALED")
    in_progress_files = response.json()

    transfer_ids = set()
    for entry in in_progress_files:
        transfer_ids.add(entry['transfer_id'])

    transfer_ids = list(transfer_ids)
    #print("Transfer Ids:")
    #print(transfer_ids)
    context['ti'].xcom_push(key="transfer_in_progress", value = transfer_ids)

def get_transfer_status_from_mft(**context):
    transfer_ids = context['ti'].xcom_pull(key="transfer_in_progress")

    client = mft_client.MFTClient(transfer_api_host =MFT_HOST_IP,
                                    transfer_api_port = 7003,
                                    transfer_api_secured = False, 
                                    resource_service_host = MFT_HOST_IP, 
                                    resource_service_port = 7003,
                                    resource_service_secured = False,
                                    secret_service_host=MFT_HOST_IP,
                                    secret_service_port = 7003)
    
    completed_ids = []
    in_progess_ids = []
    failed_ids = []

    for transfer_id in transfer_ids:
        state_req = MFTTransferApi_pb2.TransferStateApiRequest(transferId=transfer_id)
        state_summary_resp = client.transfer_api.getTransferStateSummary(state_req)
        print(state_summary_resp)

        completed_ids.extend(state_summary_resp.completed)
        in_progess_ids.extend(state_summary_resp.processing)
        failed_ids.extend(state_summary_resp.failed)


    context['ti'].xcom_push(key="completed_ids", value = completed_ids)
    context['ti'].xcom_push(key="in_progess_ids", value = in_progess_ids)
    context['ti'].xcom_push(key="failed_ids", value = failed_ids)

    print("Fetching transfer status from mft")

def update_completed_transfers(**context):

    print("Updating completed transfers")

    completed_ids = context['ti'].xcom_pull(key="completed_ids")
    in_progess_ids = context['ti'].xcom_pull(key="in_progess_ids")
    failed_ids = context['ti'].xcom_pull(key="failed_ids")

    #print("Completed Ids")
    #print(completed_ids)

    #print("In Progress Ids")
    #print(in_progess_ids)

    #print("Failed Ids")
    #print(failed_ids)


    for completed_id in completed_ids:
        response = requests.patch(CATALOGUE_URL + "/catalogue/" + completed_id, json= {"transfer_status": "COMPLETED"})

    for faileded_id in failed_ids:
        response = requests.patch(CATALOGUE_URL + "/catalogue/" + faileded_id, json= {"transfer_status": "FAILED"})

    file_count_for_next_iteration = TRANSFER_SUBMISSIONS_PER_ITERATION - len(in_progess_ids)
    context['ti'].xcom_push(key="file_count_for_next_iteration", value = file_count_for_next_iteration)
    print("File count for next iteration ", file_count_for_next_iteration)

def fetch_unprocessed(**context):

    file_count_for_next_iteration = context['ti'].xcom_pull(key="file_count_for_next_iteration")
    response = requests.get(CATALOGUE_URL + "/catalogue/?transfer_status=NOT_STARTED&sealed_state=UNSEALED")
    not_startd_files = response.json()
    if len(not_startd_files) > file_count_for_next_iteration:
        not_startd_files = not_startd_files[0:file_count_for_next_iteration]

    print(not_startd_files)
    context['ti'].xcom_push(key="to_transfer", value = not_startd_files)
    print("Fetching unprocessed data points")

def submit_to_mft(**context):

    file_list = context['ti'].xcom_pull(key="to_transfer")

    client = mft_client.MFTClient(transfer_api_host = MFT_HOST_IP,
                                    transfer_api_port = 7003,
                                    transfer_api_secured = False, 
                                    resource_service_host = MFT_HOST_IP, 
                                    resource_service_port = 7003,
                                    resource_service_secured = False,
                                    secret_service_host=MFT_HOST_IP,
                                    secret_service_port = 7003)

    source_id = SOURCE_STORAGE_ID
    dest_id = DESTINATION_STORAGE_ID

    sec_req = StorageCommon_pb2.SecretForStorageGetRequest(storageId = source_id)
    source_sec_resp = client.common_api.getSecretForStorage(sec_req)

    sec_req = StorageCommon_pb2.SecretForStorageGetRequest(storageId = dest_id)
    dest_sec_resp = client.common_api.getSecretForStorage(sec_req)

    endpoint_paths = []
    current_files = []
    transfer_map = {}
    for i in range(len(file_list)):

        file_entry = file_list[i]
        current_files.append(file_entry)
        endpoint_paths.append(MFTTransferApi_pb2.EndpointPaths(
                            sourcePath = file_entry['source_path'], 
                            destinationPath = file_entry['destination_path']))

        if (i > 0 and i % FILES_PER_TRANSFER == 0) or i == len(file_list) - 1:
            transfer_request = MFTTransferApi_pb2.TransferApiRequest(sourceStorageId = source_id,
                                                           sourceSecretId = source_sec_resp.secretId,
                                                           destinationStorageId = dest_id,
                                                           destinationSecretId = dest_sec_resp.secretId,
                                                           optimizeTransferPath = False)
            transfer_request.endpointPaths.extend(endpoint_paths)

            transfer_resp = client.transfer_api.submitTransfer(transfer_request)
            transfer_id = transfer_resp.transferId

            print("Transfer id : " + transfer_id)

            for current_file in current_files:
                transfer_map[current_file['uuid']] = transfer_id

            endpoint_paths = []
            current_files = []


    context['ti'].xcom_push(key="transfer_map", value = transfer_map)

    print("Submitting to MFT ", file_list)

def update_submitted_transfers(**context):
    transfer_map = context['ti'].xcom_pull(key="transfer_map")
    for uid in transfer_map:
        transfer_id = transfer_map[uid]
        response = requests.patch(CATALOGUE_URL + "/catalogue/" + uid, json= {"transfer_status": "IN_PROGRESS", "transfer_id": transfer_id})
        print(response.content)
    print("Updating the transfer status")


with DAG(dag_id="hls-nasa-hot-data-movement-workflow", start_date=datetime(2022,1,1), schedule_interval=None, catchup=False) as dag:
    task1 = PythonOperator(task_id="fetch_pending", python_callable=fetch_pending)
    task2 = PythonOperator(task_id="get_transfer_status_from_mft", python_callable=get_transfer_status_from_mft)
    task3 = PythonOperator(task_id="update_completed_transfers", python_callable=update_completed_transfers)
    task4 = PythonOperator(task_id="fetch_unprocessed", python_callable=fetch_unprocessed)
    task5 = PythonOperator(task_id="submit_to_mft", python_callable=submit_to_mft)
    task6 = PythonOperator(task_id="update_submitted_transfers", python_callable=update_submitted_transfers)
    trigger_self = TriggerDagRunOperator(task_id='repeat',  trigger_dag_id=dag.dag_id, dag=dag)
    
task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> trigger_self

