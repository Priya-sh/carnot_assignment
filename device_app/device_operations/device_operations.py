import os
import pandas as pd
import json
from datetime import datetime
from django.core.cache import cache


class RedisOperation:
	"""class that handles redis communication"""

	def __init__(self, request_data = {}):
		self.request_data = request_data

	def storeData(self, device_id):
		fo = FileOperations()
		df = fo.readCsv()
		db_obj = DBSimulate({'device_id': device_id})
		latest_db_data = db_obj.getLatestData(df)
		latest_record = {
			'latitude': float(latest_db_data['latitude']),
			'longitude': float(latest_db_data['longitude']),
			'time_stamp': str(latest_db_data['time_stamp']),
			'device_id': int(latest_db_data['device_fk_id']),
			'sts': str(latest_db_data['sts']),
			'speed': int(latest_db_data['speed'])
		}
		json_data = json.dumps(latest_record)
		cache.set(device_id, json_data)
		return latest_record
		

	def getData(self):
		device_id = 25029
		if 'device_id' in self.request_data:
			device_id = self.request_data['device_id']
		
		cache_key = str(device_id)
		data = cache.get(key=cache_key)
		print("cache: ", data)
		if not data:
			data = self.storeData(device_id)
		else:
			data = json.loads(data)
		return data


class FileOperations:

	def __init__(self):
		self.raw_data_path = os.path.join('', 'raw_data.csv')

	def readCsv(self):
		df = pd.read_csv(self.raw_data_path)
		df['sts'] = pd.to_datetime(df['sts'])
		return df
		

class DBSimulate:

	def __init__(self, request_data = {}):
		self.request_data = request_data

	def getLatestData(self, df):
		device_id = 25029
		if 'device_id' in self.request_data:
			device_id = self.request_data['device_id']
		df = df[df['device_fk_id'] == device_id].sort_values(by="sts", ascending=False)
		return df.iloc[0]


	def getFilterData(self, df):
		# device_id = 25029
		# start_time = pd.Timestamp("2021-10-22 20:30:00", tz="UTC").replace(microsecond=0)
		# end_time = pd.Timestamp("2021-10-23 16:00:00", tz="UTC").replace(microsecond=0)
		
		if 'start_time' in self.request_data:
			start_time = pd.Timestamp(self.request_data['start_time'], tz="UTC").replace(microsecond=0)
		if 'end_time' in self.request_data:
			end_time = pd.Timestamp(self.request_data['end_time'], tz="UTC").replace(microsecond=0)
		
		print("start: ", start_time, "end: ", end_time)
		
		if 'device_id' in self.request_data:
			device_id = self.request_data['device_id']
		df = df[(df['device_fk_id'] == device_id) & (df['sts'] >= start_time) & (df['sts'] <= end_time)]
		record_list = df.to_dict('records')
		result = []
		for d in record_list:
			result.append((d['latitude'], d['longitude'], d['time_stamp']))
		return result