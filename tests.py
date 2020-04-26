from django.test import TestCase

import requests
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_esapi.settings'
django.setup()

from jogos.models import Athlete, Modality, Stage, Results


class Base:
    url_base = 'http://localhost:8000/api/v1/'
    headers = {}
    athlete = Athlete.objects.first()
    modality = Modality.objects.first()
    stage = Stage.objects.first()
    result = Results.objects.first()

class TestModality(Base):
    """
    Class for tests in modality endpoint
    """
        
    url_name = 'modality/'

    def test_get_modality(self):

        modality = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert modality.status_code == 200


    def test_get_specific_modality(self):
        modality = requests.get(url=f'{self.url_base}{self.url_name}{self.modality.id}/', headers=self.headers)
        assert modality.status_code == 200


    def test_post_modality(self):
        new_modality = {
            "name": "Ginástica Artística"
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_modality)
        response.status_code == 201


    def test_put_modality(self):
        update_modality = {
            "name": "100m rasos"
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{self.modality.id}/', 
                                headers=self.headers, 
                                data=update_modality)
        assert response.status_code == 200


    def test_delete_modality(self):
        response = requests.delete(url=f'{self.url_base}{self.url_name}{self.modality.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0


class TestStage(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'stage/'
    
    def test_get_stage(self):
        stage = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert stage.status_code == 200

    def test_get_specific_stage(self):
        stage = requests.get(url=f'{self.url_base}{self.url_name}{self.stage.id}/', headers=self.headers)
        assert stage.status_code == 200

    def test_post_stage(self):
        new_stage = {
            "modality": 3,
            "name": "Classificatória 1",
            "status": False
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_stage)
        response.status_code == 201

    def test_put_stage(self):
        update_stage = {
            "modality": 3,
            "name": "Classificatória 1",
            "status": True
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{self.stage.id}/', 
                                headers=self.headers, 
                                data=update_stage)
        assert response.status_code == 200

    def test_delete_stage(self):
        response = requests.delete(url=f'{self.url_base}{self.url_name}{self.stage.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0


class TestAthlete(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'athletes/'

    def test_get_athlete(self):
        athlete = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert athlete.status_code == 200

    def test_get_specific_athlete(self):
        athlete = requests.get(url=f'{self.url_base}{self.url_name}{self.athlete.id}/', headers=self.headers)
        assert athlete.status_code == 200

    def test_post_athlete(self):
        new_athlete = {
            "modality": 3,
            "first_name": "João",
            "last_name": "Carlos",
            "age": 40
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_athlete)
        response.status_code == 201

    def test_put_athlete(self):
        update_athlete = {
            "modality": 3,
            "first_name": "João",
            "last_name": "Flávio",
            "age": 40
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{self.athlete.id}/', 
                                        headers=self.headers, 
                                        data=update_athlete)
        assert response.status_code == 200

    def test_delete_athlete(self):
        response = requests.delete(url=f'{self.url_base}{self.url_name}{self.athlete.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0


class TestResults(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'results/'
    
    def test_get_results(self):
        results = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert results.status_code == 200

    def test_get_specific_result(self):
        results = requests.get(url=f'{self.url_base}{self.url_name}{self.result.id}/', headers=self.headers)
        assert results.status_code == 200

    def test_post_result(self):
        new_result = {
            "modality": 3,
            "athlete": 1,
            "stage": 1,
            "value": "10.123",
            "unity": "m"
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_result)
        response.status_code == 201

    def test_put_result(self):
        update_result = {
            "modality": 3,
            "athlete": 1,
            "stage": 1,
            "value": "16.123",
            "unity": "m"
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{self.result.id}/',
                                        headers=self.headers, 
                                        data=update_result)
        assert response.status_code == 200

    def test_delete_result(self):
        response = requests.delete(url=f'{self.url_base}{self.url_name}{self.result.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0    


class TestRanking(Base):
    """
    Class for tests in ranking endpoint
    """

    def test_list_ranking(self):

        ranking = requests.get(url=f'{self.url_base}stage/{self.stage.id}/ranking/', headers=self.headers)
        assert ranking.status_code == 200
