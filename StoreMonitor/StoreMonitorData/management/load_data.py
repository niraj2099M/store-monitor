from django.core.management.base import BaseCommand
from StoreMonitorData.models import StoreStatus, BusinessHours, StoreTimezone
import dateutil.parser
import csv


class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **kwargs):

        storestatus_path="StoreMonitor/data/store status.csv"
        
        chunk_size = 1000
        with open(storestatus_path, 'r') as file:
            reader = csv.DictReader(file)
            chunk=[]
            
            for row in reader:
                store_status_instance = StoreStatus(
                        store_id=row['store_id'],
                        timestamp_utc=dateutil.parser.parse(row['timestamp_utc']),
                        status=row['status']
                    )
                chunk.append(store_status_instance)
                if len(chunk) == chunk_size:
                    StoreStatus.objects.bulk_create(chunk)
                    chunk = []
            if chunk:
                StoreStatus.objects.bulk_create(chunk)

        self.stdout.write(self.style.SUCCESS('Store status Data imported successfully'))
        



        #Loading store's business hours
        Menuhours_path = "StoreMonitor/data/Menu_hours.csv"
        with open(Menuhours_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                BusinessHours.objects.create(
                    store_id=row['store_id'],
                    day=row['day'],
                    start_time_local=row['start_time_local'],
                    end_time_local=row['end_time_local']
                )
        self.stdout.write(self.style.SUCCESS('Business hours Data imported successfully'))



        #Loading store's Timezone
        timezone_path = "StoreMonitor/data/bq-results-20230125-202210-1674678181880.csv"
        with open(timezone_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StoreTimezone.objects.create(
                    store_id=row['store_id'],
                    timezone_str=row['timezone_str']
                )
        self.stdout.write(self.style.SUCCESS('Timezone Data imported successfully'))