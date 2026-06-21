import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"
 

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