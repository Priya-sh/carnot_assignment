from django.urls import path
from device_app import views

urlpatterns = [
	path('getDeviceData', views.LatestDeviceData.as_view(), name='get-device-data'),
	path('getLocationData', views.LocationAPIView.as_view(), name='get-location-data'),
	path('getRangeData', views.RangeAPIView.as_view(), name='get-range-data'),
]