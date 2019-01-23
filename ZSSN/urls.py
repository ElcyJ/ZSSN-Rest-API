from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from core.views import *
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'survivors', SurvivorView, base_name = 'survivor')
router.register(r'inventory', InventoryView, base_name ='inventory')
router.register(r'flag_survivor', FlagSurvivorView, base_name = 'flag_survivor')
router.register(r'survivor_last_location', LastLocationView, base_name = 'survivor_last_location')
router.register(r'trade', TradeView, base_name ='trade')
router.register(r'reports',ReportView, base_name = 'report')

urlpatterns = [
    path(r'admin/', admin.site.urls),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

urlpatterns = router.urls + urlpatterns
