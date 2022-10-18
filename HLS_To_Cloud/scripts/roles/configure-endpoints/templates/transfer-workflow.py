from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
from airavata_mft_sdk import mft_client
from airavata_mft_sdk import MFTTransferApi_pb2
from airavata_mft_sdk.s3 import S3Storage_pb2
from airavata_mft_sdk.resourcesecretmap import StorageSecretMap_pb2
from airavata_mft_sdk.resource import ResourceService_pb2
import time
from airflow.operators.dagrun_operator import TriggerDagRunOperator

def fetch_pending(**context):
    print("Fetching pending transfers")
    response = requests.get("http://172.17.0.1:5000/catalogue/?transfer_status=IN_PROGRESS&sealed_State=unsealed")
    in_progress_files = response.json()
    context['ti'].xcom_push(key="transfer_in_progress", value = in_progress_files)

def get_transfer_status_from_mft(**context):
    transfer_in_progress = context['ti'].xcom_pull(key="transfer_in_progress")

    client = mft_client.MFTClient(transfer_api_host = "172.17.0.1", resource_service_host = "172.17.0.1", secret_service_host="172.17.0.1")

    completed_ids = []
    in_progess_ids = []
    failed_ids = []
    for entry in transfer_in_progress:
        state_req = MFTTransferApi_pb2.TransferStateApiRequest(transferId=entry['transfer_id'])
        state_resp = client.transfer_api.getTransferState(state_req)
        print(state_resp)
        if state_resp.state == 'COMPLETED':
            completed_ids.append(entry['uuid'])
        elif state_resp.state == 'FAILED':
            failed_ids.append(entry['uuid'])
        else:
            in_progess_ids.append(entry['uuid'])

    context['ti'].xcom_push(key="completed_ids", value = completed_ids)
    context['ti'].xcom_push(key="in_progess_ids", value = in_progess_ids)
    context['ti'].xcom_push(key="failed_ids", value = failed_ids)

    print("Fetching transfer status from mft")

def update_completed_transfers(**context):

    print("Updating completed transfers")

    completed_ids = context['ti'].xcom_pull(key="completed_ids")
    in_progess_ids = context['ti'].xcom_pull(key="in_progess_ids")
    failed_ids = context['ti'].xcom_pull(key="failed_ids")

    for completed_id in completed_ids:
        response = requests.patch("http://172.17.0.1:5000/catalogue/" + completed_id, json= {"transfer_status": "COMPLETED"})

    for faileded_id in failed_ids:
        response = requests.patch("http://172.17.0.1:5000/catalogue/" + faileded_id, json= {"transfer_status": "FAILED"})

    file_count_for_next_iteration = 500 - len(in_progess_ids)
    context['ti'].xcom_push(key="file_count_for_next_iteration", value = file_count_for_next_iteration)
    print("File count for next iteration ", file_count_for_next_iteration)

def fetch_unprocessed(**context):

    file_count_for_next_iteration = context['ti'].xcom_pull(key="file_count_for_next_iteration")
    response = requests.get("http://172.17.0.1:5000/catalogue/?transfer_status=NOT_STARTED&sealed_State=unsealed")
    not_startd_files = response.json()
    if len(not_startd_files) > file_count_for_next_iteration:
        not_startd_files = not_startd_files[0:file_count_for_next_iteration]

    print(not_startd_files)
    context['ti'].xcom_push(key="to_transfer", value = not_startd_files)
    print("Fetching unprocessed data points")

def submit_transfer(client, file_name, source_id, source_token, dest_id, dest_token):

    source_file_name = file_name
    dest_file_name = file_name.split("/")[-1]

    transfer_request = MFTTransferApi_pb2.TransferApiRequest(sourcePath = source_file_name,
                                                             sourceToken = source_token,
                                                             sourceStorageId = source_id,
                                                             destinationStorageId = dest_id,
                                                             destinationPath = dest_file_name,
                                                             destinationToken = dest_token)
    transfer_resp = client.transfer_api.submitTransfer(transfer_request)
    transfer_id = transfer_resp.transferId
    return transfer_id

def submit_to_mft(**context):

    client = mft_client.MFTClient(transfer_api_host = "172.17.0.1", resource_service_host = "172.17.0.1", secret_service_host="172.17.0.1")

    source_id = "{{ source_storage_id }}"
    dest_id = "{{ destination_storage_id }}"

    source_search_req = StorageSecretMap_pb2.StorageSecretSearchRequest(storageId=source_id, type=StorageSecretMap_pb2.StorageSecret.StorageType.S3)
    source_search_resp = client.storage_secret_map_api.searchStorageSecret(source_search_req)
    #print(source_search_resp)
    source_token = source_search_resp.storageSecret.secretId

    dest_search_req = StorageSecretMap_pb2.StorageSecretSearchRequest(storageId=dest_id, type=StorageSecretMap_pb2.StorageSecret.StorageType.S3)
    dest_search_resp = client.storage_secret_map_api.searchStorageSecret(dest_search_req)
    dest_token = dest_search_resp.storageSecret.secretId

    file_list = context['ti'].xcom_pull(key="to_transfer")
    transfer_map = {}
    print("Pending amount to submit to MFT " + str(len(file_list)))
    for file_entry in file_list:
        file_name = file_entry['name']
        transfer_id = submit_transfer(client, file_name, source_id, source_token, dest_id, dest_token)
        #print("Submitted transfer ", transfer_id, " to file ", file_name)
        transfer_map[file_entry['uuid']] = transfer_id

    context['ti'].xcom_push(key="transfer_map", value = transfer_map)

    print("Submitting to MFT ", file_list)

def update_submitted_transfers(**context):
    transfer_map = context['ti'].xcom_pull(key="transfer_map")
    for uid in transfer_map:
        transfer_id = transfer_map[uid]
        response = requests.patch("http://172.17.0.1:5000/catalogue/" + uid, json= {"transfer_status": "IN_PROGRESS", "transfer_id": transfer_id})
        print(response.content)
    print("Updating the transfer status")


with DAG(dag_id="transfer-workflow", start_date=datetime(2021,1,1), schedule_interval=None, catchup=False) as dag:
    task1 = PythonOperator(task_id="fetch_pending", python_callable=fetch_pending)
    task2 = PythonOperator(task_id="get_transfer_status_from_mft", python_callable=get_transfer_status_from_mft)
    task3 = PythonOperator(task_id="update_completed_transfers", python_callable=update_completed_transfers)
    task4 = PythonOperator(task_id="fetch_unprocessed", python_callable=fetch_unprocessed)
    task5 = PythonOperator(task_id="submit_to_mft", python_callable=submit_to_mft)
    task6 = PythonOperator(task_id="update_submitted_transfers", python_callable=update_submitted_transfers)
    trigger_self = TriggerDagRunOperator(task_id='repeat',  trigger_dag_id=dag.dag_id, dag=dag)

task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> trigger_self

