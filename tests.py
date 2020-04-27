from django.test import TestCase

import requests
import os
import django

import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_esapi.settings'
django.setup()

from jogos.models import Athlete, Modality, Stage, Results


class Base:
    """
    Base Class for run tests in API
    """
    url_base = 'http://localhost:8000/api/v1/'
    headers = {'Authorization': 'Token a584711ab6d173e831f6927ad5d0baef297745b2'}


class TestModality(Base):
    """
    Class for tests in modality endpoint
    """ 
    url_name = 'modality/'

    def test_post_modality(self):
        new_modality = {
            "name": "Natação"
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_modality)
        assert response.status_code == 201

    def test_get_modality(self):
        modality = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert modality.status_code == 200
        time.sleep(2)

    def test_get_specific_modality(self):
        modality = Modality.objects.last()
        get_modality = requests.get(url=f'{self.url_base}{self.url_name}{modality.id}/', headers=self.headers)
        assert get_modality.status_code == 200
        time.sleep(2)

    def test_put_modality(self):
        modality = Modality.objects.last()
        update_modality = {
            "name": "Natação 2"
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{modality.id}/', 
                                headers=self.headers, 
                                data=update_modality)
        assert response.status_code == 200
        time.sleep(2)


class TestAthlete(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'athletes/'

    def test_post_athlete(self):
        modality = Modality.objects.last()
        new_athlete = {
            "modality": modality.id,
            "first_name": "João",
            "last_name": "Carlos",
            "age": 40,
            "active": True
        }
        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_athlete)
        assert response.status_code == 201
        time.sleep(2)

    def test_get_athlete(self):
        athlete = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert athlete.status_code == 200
        time.sleep(2)

    def test_get_specific_athlete(self):
        athlete = Athlete.objects.last()
        new_athlete = requests.get(url=f'{self.url_base}{self.url_name}{athlete.id}/', headers=self.headers)
        assert new_athlete.status_code == 200
        time.sleep(2)

    def test_put_athlete(self):
        modality = Modality.objects.last()
        athlete = Athlete.objects.last()
        update_athlete = {
            "modality": modality.id,
            "first_name": "João",
            "last_name": "Flávio",
            "age": 40
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{athlete.id}/', 
                                        headers=self.headers, 
                                        data=update_athlete)
        assert response.status_code == 200
        time.sleep(2)


class TestStage(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'stage/'

    def test_post_stage(self):
        modality = Modality.objects.last()
        new_stage = {
            "modality": modality.id,
            "name": "Classificatória 90",
            "status": True
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_stage)
        assert response.status_code == 201
        time.sleep(2)
    
    def test_get_stage(self):
        stage = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert stage.status_code == 200
        time.sleep(2)

    def test_get_specific_stage(self):
        stage = Stage.objects.last()
        stage = requests.get(url=f'{self.url_base}{self.url_name}{stage.id}/', headers=self.headers)
        assert stage.status_code == 200
        time.sleep(2)

    def test_put_stage(self):
        stage = Stage.objects.last()
        update_stage = {
            "modality": stage.modality_id,
            "name": "Classificatória 99",
            "status": True
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{stage.id}/', 
                                headers=self.headers, 
                                data=update_stage)
        assert response.status_code == 200
        time.sleep(2)


class TestResults(Base):
    """
    Class for tests in stage endpoint
    """
    url_name = 'results/'

    def test_post_result(self):
        athlete = Athlete.objects.last()
        stage = Stage.objects.last()
        new_result = {
            "modality": athlete.modality_id,
            "athlete": athlete.id,
            "stage": stage.id,
            "value": "10.123",
            "unity": "m"
        }

        response = requests.post(url=f'{self.url_base}{self.url_name}', headers=self.headers, data=new_result)
        assert response.status_code == 201
        time.sleep(2)
    
    def test_get_results(self):
        results = requests.get(url=f'{self.url_base}{self.url_name}', headers=self.headers)
        assert results.status_code == 200
        time.sleep(2)

    def test_get_specific_result(self):
        result = Results.objects.last()
        results = requests.get(url=f'{self.url_base}{self.url_name}{result.id}/', headers=self.headers)
        assert results.status_code == 200
        time.sleep(2)

    def test_put_result(self):
        result = Results.objects.last()
        update_result = {
            "modality": result.modality_id,
            "athlete": result.athlete_id,
            "stage": result.stage_id,
            "value": "16.123",
            "unity": "m"
        }

        response = requests.put(url=f'{self.url_base}{self.url_name}{result.id}/',
                                        headers=self.headers, 
                                        data=update_result)
        assert response.status_code == 200
        time.sleep(2)


class TestRanking(Base):
    """
    Class for tests in ranking endpoint
    """
    def test_list_ranking(self):
        stage = Stage.objects.last()
        ranking = requests.get(url=f'{self.url_base}stage/{stage.id}/ranking/', headers=self.headers)
        assert ranking.status_code == 200
        time.sleep(2)


class TestDeleteInstancesAfterUse(Base):
    """
    Class for delete the instances created to tests
    """
    def test_delete_result(self):
        result = Results.objects.last()
        response = requests.delete(url=f'{self.url_base}results/{result.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0    
        time.sleep(2)

    def test_delete_athlete(self):
        athlete = Athlete.objects.last()
        response = requests.delete(url=f'{self.url_base}athletes/{athlete.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0
        time.sleep(2)

    def test_delete_stage(self):
        stage = Stage.objects.last()
        response = requests.delete(url=f'{self.url_base}stage/{stage.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0
        time.sleep(2)

    def test_delete_modality(self):
        modality = Modality.objects.last()
        response = requests.delete(url=f'{self.url_base}modality/{modality.id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0
        time.sleep(2)