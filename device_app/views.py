from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from device_app.device_operations.device_operations import RedisOperation, DBSimulate, FileOperations



class LatestDeviceData(APIView):

	def post(self, request):

		request_data = request.data
		rd = RedisOperation(request_data)
		result = rd.getData()
		
		return JsonResponse({"data": result})
	

class LocationAPIView(APIView):
	
	def post(self, request):

		request_data = request.data
		rd = RedisOperation(request_data)
		result = rd.getData()
		data = (result['latitude'], result['longitude'])
		
		return JsonResponse({"data": data})
	

class RangeAPIView(APIView):

	def post(self, request):
		fo = FileOperations()
		df = fo.readCsv()

		request_data = request.data
		dbs = DBSimulate(request_data)
		result = dbs.getFilterData(df)
		return JsonResponse({"data": result})
