from django.http import FileResponse

def favicon(request):
    return FileResponse(open('./static/odaa.png', 'rb'))

