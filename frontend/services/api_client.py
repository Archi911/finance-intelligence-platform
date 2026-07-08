import requests
import os
BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000/api/v1"
)
 

def ask_question(question):

    response = requests.post(
        f"{BASE_URL}/analytics",
        json={
            "question": question
        }
    )

    return response.json()




def get_dashboard_metrics():

    response = requests.get(
        f"{BASE_URL}/dashboard-metrics"
    )

    return response.json()


def upload_invoice(file):

    response = requests.post(
        f"{BASE_URL}/ingest",
        files={
            "file": file
        }
    )

    return response.json()