from django.db import models

class StoreStatus(models.Model):
    #store id value >21bill thus used BigInt field
    store_id = models.BigIntegerField()
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

class BusinessHours(models.Model):
    store_id = models.BigIntegerField()
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreTimezone(models.Model):
    store_id = models.BigIntegerField()
    timezone_str = models.CharField(max_length=50)

class StoreReport(models.Model):
    report_id = models.CharField(max_length=10, unique=True)
    file_path = models.FileField(upload_to='reports/', default='')
    