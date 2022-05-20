import json
import os
from typing import Dict

import pandas as pd
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views import View

from ods.models import OdsSpecModel


class LoadView(View):

    def post(self, request: WSGIRequest):
        data: Dict = json.loads(request.body)
        filename = data.get('filename', None)
        bm_type = data.get('bm_type', None)
        if filename is not None and os.path.isfile(filename) and filename.split('.')[-1] == 'csv':
            is_ok = self._load(bm_type, filename)
            if is_ok:
                return HttpResponse(f"Load {bm_type} - {filename} Successfully")
            else:
                return HttpResponse(f"Error! Check {bm_type} or {filename}")
        return HttpResponse(f"Error! Check {bm_type} or {filename}")

    def _load(self, bm_type, filename):
        df = pd.read_csv(filename)
        if 'cpu' in bm_type:
            df.apply(lambda item: self._insert_cpu(item), axis=1)
            return True
        elif 'jbb' in bm_type:
            df.apply(lambda item: self._insert_jbb2015(item), axis=1)
            return True
        elif 'jvm' in bm_type:
            df.apply(lambda item: self._insert_jvm2008(item), axis=1)
            return True
        elif 'ssj' in bm_type:
            df.apply(lambda item: self._insert_ssj2008(item), axis=1)
            return True
        else:
            return False

    @classmethod
    def _get_model(cls, row):
        spec_model = OdsSpecModel(
            suite=row['Suite'],
            hw_vendor=row['HW Vendor'],
            system_series=row['System Series'],
            result=row['Result'],
            cpu_vendor=row['CPU Vendor'],
            cpu_name=row['CPU Name'],
            cpu_ghz=row['CPU GHz'],
            max_ghz=row['Max GHz'],
            threads_per_core=row['Threads Per Core'],
            cores_per_chip=row['Cores Per Chip'],
            chips=row['Chips'],
            total_cores=row['Total Cores'],
            l1_cache=row['L1 Cache'],
            l2_cache=row['L2 Cache'],
            memory=row['Memory'],
            memory_amount=row['Memory Amount'],
            memory_number=row['Memory Number'],
            os=row['OS'],
            file_system=row['File System'],
            url_suffix=row['URL Suffix'],
            test_date=row['Test Date'],
            hw_avail=row['HW Avail'],
            submit_quarter=row['Submit Quarter'],
            submit_year=row['Submit Year'],
            full_url=row['Full URL'],
        )
        return spec_model

    def _insert_cpu(self, row):
        spec_model = self._get_model(row)
        spec_model.l3_cache = row['L3 Cache']
        spec_model.storage_type = row['Storage Type']
        spec_model.storage = row['Storage']
        spec_model.save()

    def _insert_jbb2015(self, row):
        spec_model = self._get_model(row)
        spec_model.nodes = row['Nodes']
        spec_model.l3_cache = row['L3 Cache']
        spec_model.storage_type = row['Storage Type']
        spec_model.storage = row['Storage']
        spec_model.jvm = row['JVM']
        spec_model.save()

    def _insert_jvm2008(self, row):
        spec_model = self._get_model(row)
        spec_model.jvm = row['JVM']
        spec_model.save()

    def _insert_ssj2008(self, row):
        spec_model = self._get_model(row)
        spec_model.l3_cache = row['L3 Cache']
        spec_model.storage_type = row['Storage Type']
        spec_model.storage = row['Storage']
        spec_model.jvm = row['JVM']
        spec_model.save()
