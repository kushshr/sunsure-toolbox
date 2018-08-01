from webserver.models import *
import datetime
from django.shortcuts import render,HttpResponse


def value_from_req(request,key,default):
    value = getattr(request, 'GET').get(key)
    if not value:
        value = getattr(request, 'POST').get(key)
    if not value:
        return default
    return value

def default_response(status=True,data={},msg='',login=True):
    if status:
        return {'status':status,'response':data,'login':login}
    else:
        return {'status':status,'msg':msg,'login':login}

# Create your views here.
def index(request):
    return render(request,'index.html', locals())

def create_project(request):
    name = value_from_req(request,'name','')
    manager = value_from_req(request,'manager','')
    size = value_from_req(request,'size','')
    location = value_from_req(request,'location','')
    in_charge = value_from_req(request,'in_charge','')

    manager = ProjectManagers.objects.filter(name = manager).first()
    if not manager:
        manager = ProjectManagers(name=manager)
        manager.save()

    project = Projects.objects.filter(name=name).first()
    if not project:
        project = Projects(name=name, manager=manager,size=size, location=location, site_in_charge=in_charge)
        project.save()

    ##Front end should set these fields as mandatory
    return HttpResponse(json.dumps(default_response(status=False, msg=" Project Created", data = project.embed())))

def create_contractor_for_project(request):
    project_id  = value_from_req(request, 'project_id', '')
    name = value_from_req(request, 'name', '')
    size = value_from_req(request, 'size', '')
    location = value_from_req(request, 'location', '')