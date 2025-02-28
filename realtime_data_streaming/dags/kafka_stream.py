from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Thomas',
    'start_date': datetime(2024, 7, 19, 12, 00)
}


def get_data():
    import json
    import requests
    
    res = requests.get('https://randomuser.me/api/').json()
    res = res['results'][0]
    
    return res

def format_data(res):
    data = {}
    
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']

    data['gender'] = res['gender']
    data['age'] = res['dob']['age']
    data['birthday'] = res['dob']['date']

    data['email'] = res['email']
    data['phone'] = res['phone']
    data['cell'] = res['cell']
    data['timezone_utc'] = res['location']['timezone']['offset']
        
    data['street'] = str(res['location']['street']['number']) + ' ' + res['location']['street']['name']
    data['postcode'] = str(res['location']['postcode'])
    data['city'] = res['location']['city']
    data['state'] = res['location']['state']
    data['country'] = res['location']['country']
    data['full_address'] = data['street'] + ' ' + data['postcode'] + ' ' + data['city'] + ', ' + data['state'] + ', ' + data['country']
    
    data['registration_date'] = res['registered']['date']
    data['picture'] = res['picture']['medium']
    
    return data

def stream_data():
    import json 
    
    res = get_data()
    res = format_data(res)
    print(json.dumps(res, indent=3))

with DAG('user_automation'
         , default_args=default_args
         , schedule='@daily'
         , catchup=False) as dag:
    
    streaming_task = PythonOperator(
        task_id='stream_data_from_user_api'
        , python_callable=stream_data
    )
    
stream_data()