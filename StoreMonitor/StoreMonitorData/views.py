from django.shortcuts import render

from django.http import JsonResponse,HttpResponse
from .models import StoreReport
from .ReportGenerator import generate_report
import os
import random, string
import threading


def trigger_report(request):
    # Trigger report generation
    report_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    StoreReport.objects.create(report_id=report_id)


    thread = threading.Thread(target=generate_report, args=(report_id,))
    thread.start()

    return JsonResponse({'report_id': report_id})


def get_report(request, report_id):
        
    try:
        report_instance=StoreReport.objects.get(report_id=report_id)
        
        # Get the CSV file path from the model instance
        csv_file_path = str(report_instance.file_path)
        if csv_file_path:
            return JsonResponse({'Status': f'{report_id} Complete','Report Download Link':f'http://127.0.0.1:8000/download_report/{report_id}/'})
        else:
            return JsonResponse({'Status': f'Report {report_id} Running'})
    except:
        return JsonResponse({'Error': f'Report {report_id} dosent exist'})
        

def download_report(request,report_id):
    
    try:
        report_instance=StoreReport.objects.get(report_id=report_id)
        csv_file_path = str(report_instance.file_path)

        with open(csv_file_path, 'r') as csv_file:
            response = HttpResponse(csv_file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(csv_file_path)
        
            return response
    except:
        return JsonResponse({'Error': f'Report {report_id} dosent exist'})