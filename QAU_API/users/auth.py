from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
# {
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MzIxNDY2LCJpYXQiOjE3NDYzMTk0MDcsImp0aSI6ImQyODgwYmM3NjJiODQyMGViY2Y0ODU5MmQzYWM3NWUxIiwidXNlcl9pZCI6ImJlMTFkNDZjLThiZWMtNDcyYS05ZTBmLTA5MTBjYWQxMjc0OSJ9.k-U2HOnOAWnsXezCiDlc4G1sDg2RJ2Gg0-buv2VMl9o",
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjkyNTM2NiwiaWF0IjoxNzQ2MzIwNTY2LCJqdGkiOiIzNjgyZGFkOTM3Mjk0Y2M2ODFlNTcwYWJhMjQ5ZDllZSIsInVzZXJfaWQiOiJiZTExZDQ2Yy04YmVjLTQ3MmEtOWUwZi0wOTEwY2FkMTI3NDkifQ.LBLwVikIaCArUu8APCith7gViJQVB5FcsGpLi-Pmpns"
# }
