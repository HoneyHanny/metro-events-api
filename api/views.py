from django.http import JsonResponse

def getData(request):
    person = {'name':'MetroEvents API Deploy Test', 'age':20}
    return JsonResponse(person)