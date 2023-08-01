from django.http import JsonResponse
from django.shortcuts import render
from workalendar.america import Brazil
from datetime import datetime, timedelta, time
from workadays import workdays as wd

# Create your views here.
def page_dates(request):
    return render(request, 'testes/calculator_dates.html')

def get_days_corridos(data_final: datetime, data_incial: datetime):
    meia_noite = time(hour=0, minute=0)
    if data_incial.weekday() in [5, 6]:
        data_incial = data_incial.replace(day=(data_incial.day + 1), hour=0, minute=0)
    if data_final.weekday() in [5, 6]:
        data_final = data_final.replace(hour=0, minute=0)
    print(data_incial, data_final)
    return data_final - data_incial

def calculator_dates(request):
    data_inicial = datetime.strptime(f'{request.POST.get("data_inicial")} 14:00', '%Y-%m-%d %H:%M')
    data_final = datetime.strptime(f"{request.POST.get('data_final')} 17:00", '%Y-%m-%d %H:%M')
    calendario_brasil = Brazil()
    dias_uteis = calendario_brasil.get_working_days_delta(data_inicial.date(), data_final.date())
    # dias_uteis = wd.networkdays(data_inicial.date(), data_final.date())
    total_dias = (data_final - data_inicial).days + 1
    dias_nao_uteis = total_dias - dias_uteis
    # dias_corridos = data_final - data_inicial
    dias_corridos = get_days_corridos(data_final, data_inicial)
    dias_horas_uteis = timedelta(days=(dias_corridos.days - dias_nao_uteis), seconds=dias_corridos.seconds)

    return JsonResponse(data={
        'dias_uteis': dias_uteis,
        'total_dias': total_dias,
        'dias_nao_uteis': dias_nao_uteis,
        'dias_corridos': dias_corridos.days,
        'dias_horas_uteis': f'{dias_horas_uteis.days}d : {dias_horas_uteis.seconds/3600}h'
    })  