import requests
import json
import threading
import time

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        r = requests.get(
            f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(r.text)
        return data

    def get_total_cases(self):
        data = self.data['total']
        for n in data:
            if n['name'] == 'Coronavirus Cases:':
                return n['value']
        return -1

    def get_total_death(self):
        data = self.data['total']
        for n in data:
            if n['name'] == 'Deaths:':
                return n['value']
        return -1

    def get_country_data(self, country):
        data = self.data['country']
        for n in data:
            if n['name'].lower() == country.lower():
                return n
        return -1

    def get_country_list(self):
        list = [country['name'].lower() for country in self.data['country']]
        return list

    def update_data(self):
        r = requests.post(
            f"https://www.parsehub.com/api/v2/projects/{self.project_token}/run", params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('Data updated')
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()
