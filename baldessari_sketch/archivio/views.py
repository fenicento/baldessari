#-*- coding:Latin-1 -*
# Create your views here.
from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.management import call_command
from django.utils.safestring import SafeString
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from management.commands import update_from_json
from os.path import exists
from string import split
import json, os.path, re

# import models
from archivio.models import *

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_PATH = settings.MEDIA_ROOT


#return the view of the index - for now, it corresponds to the opere view
def index(request):
    return render_to_response('archivio/index.html')

def redirect_to_opere(request):
    return HttpResponseRedirect("/opere/progetti/elenco")
    # return HttpResponseRedirect("/opere/")

def redirect_to_elenco_progetti(request):
    return HttpResponseRedirect("/opere/progetti/elenco/")

#returns the global view biografia
def biografia(request):
    # dettagli = BioDetail.objects.all();
    args = {
           'section_name': 'biografia',
           # 'dettagli': dettagli ,
           }
    return render_to_response('archivio/biografia.html', args)

#returns the global view bibliografia
def bibliografia(request):
    liste  = Publication.objects.all()
    projets = Project.objects.all()
    args = {'section_name': 'bibliografia', 
			'publications' : liste, 
			'projets' : projets}
    return render_to_response('archivio/bibliografia.html', args)

def ricerca(request):
    arg = {'section_name': 'ricerca'}
    return render_to_response('archivio/test_arguments.html', arg)

def museo_virtuale(request):
    arg = {'section_name': 'museovirtuale'}
    return render_to_response('archivio/test_arguments.html', arg)

def contatti(request):
    arg = {'section_name': 'contatti'}
    return render_to_response('archivio/test_arguments.html', arg)

def login(request):
    arg = {'section_name': 'login'}
    return render_to_response('archivio/test_arguments.html', arg)


#returns the global view opere
def opere(request):  
    return HttpResponseRedirect("/opere/progetti/elenco")

    # projects = Project.objects.all()
    #     draws = Drawing.objects.all()
    #     drawings = []
    #     for p in projects:
    #         ds = draws.filter(project__sigla = p.sigla)
    #         if len(ds) > 0:	# at least one document
    #             d = ds[0]
    #             drawings.append(d)
    # 
    # 
    #     args = {
    #            'section_name': 'opere',
    #            'projects': projects,
    #            'drawings': drawings,
    #            }
    #     return render_to_response('archivio/opere.html', args)

    # arg = {'section_name': 'opere'}
    # return render_to_response('archivio/opere.html', arg)


#returns the global view opere
def elenco_progetti(request):
    # projects = Project.objects.all()
    # draws = Drawing.objects.all()
    # drawings = []
    # for p in projects:
        # ds = draws.filter(project__sigla = p.sigla)
        # if len(ds) > 0:	# at least one document
            # d = ds[0]
            # drawings.append(d)
# 
# 
    # args = {
           # 'section_name': 'opere',
           # 'projects': projects,
           # 'drawings': drawings,
           # }
    type = request.GET.get('type')
    bdate = request.GET.get('bdate')
    edate = request.GET.get('edate')
    desc = request.GET.get('desc')
    
    filterValues=dict();
    minDate=2000
    maxDate=0
    types=[]
    
    #define filters from query string
    if type is not None:
        types=type.split(",")
        variables = {'tipo__in':types,'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
        
    else:
        variables = {'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
        
    projects = Project.objects.all()
    
    #filter the project list
    for key, value in variables.items():
        if value is not None:
            projects = projects.filter(**{key: value})
        
    #projects=projects.order_by('timeinterval__beginningYear')
    projects=projects.distinct()
    jsonProjs=[]
    
    for p in projects:
        currProj=dict()
        currProj['sigla']=p.sigla
        currProj['nome']=p.denominazione
        currProj['lat']=p.latitude
        currProj['long']=p.longitude
        currProj['tipo']=p.tipo
        currProj['start']=TimeInterval.objects.filter(target=p)[0].beginningYear
        currProj['end']=TimeInterval.objects.filter(target=p).reverse()[0].endYear
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        
        if currProj['start']<minDate:
            minDate=currProj['start']
        
        if currProj['end']>maxDate:
            maxDate=currProj['end']
        
        if currProj['tipo'] is not None and {'des':currProj['tipo'],'checked':False} not in types:
            types.append({'des':currProj['tipo'],'checked':False})
        
        
    filterValues['minDate']=minDate;
    filterValues['maxDate']=maxDate;
    filterValues['types']=types;
    
                       
    jsonProj=json.dumps(jsonProjs)
    jFilterValues=json.dumps(filterValues)
        
    args = {
            'section_name': 'opere',
            #'projects': projects,
            'jsonProj': jsonProj,
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/opere.html', args)

    # arg = {'section_name': 'opere'}
    # return render_to_response('archivio/opere.html', arg)

# Show documents
def documenti(request):
    drawings = Drawing.objects.all()[1:10]	# TODO eliminare limite di 10 elementi
    args = {
            'section_name': 'opere',
            'drawings': drawings,
            }
    return render_to_response('archivio/documenti.html', args)


# Show progetti
def progetti(request):
    projects = Project.objects.all()[1:10]
    args = {
            'section_name': 'opere',
            'drawings': projects,
            }
    return render_to_response('archivio/progetti.html', args)

# Show progetti as a gallery - STARTING FILTER DEVELOPMENT HERE
def galleria_progetti(request):
    type = request.GET.get('type')
    bdate = request.GET.get('bdate')
    edate = request.GET.get('edate')
    desc = request.GET.get('desc')
    
    filterValues=dict();
    minDate=2000
    maxDate=0
    types=[]
    
    #define filters from query string
    if type is not None:
        types=type.split(",")
        variables = {'tipo__in':types,'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
        
    else:
        variables = {'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
        
    projects = Project.objects.all()
    
    #filter the project list
    for key, value in variables.items():
        if value is not None:
            projects = projects.filter(**{key: value})
        
    #projects=projects.order_by('timeinterval__beginningYear')
    projects=projects.distinct()
    jsonProjs=[]
    
    for p in projects:
        currProj=dict()
        currProj['sigla']=p.sigla
        currProj['nome']=p.denominazione
        currProj['lat']=p.latitude
        currProj['long']=p.longitude
        currProj['tipo']=p.tipo
        currProj['start']=TimeInterval.objects.filter(target=p)[0].beginningYear
        currProj['end']=TimeInterval.objects.filter(target=p).reverse()[0].endYear
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        
        if currProj['start']<minDate:
            minDate=currProj['start']
        
        if currProj['end']>maxDate:
            maxDate=currProj['end']
        
        if currProj['tipo'] is not None and {'des':currProj['tipo'],'checked':False} not in types:
            types.append({'des':currProj['tipo'],'checked':False})
        
        
    filterValues['minDate']=minDate;
    filterValues['maxDate']=maxDate;
    filterValues['types']=types;
    
                       
    jsonProj=json.dumps(jsonProjs)
    jFilterValues=json.dumps(filterValues)
        
    args = {
            'section_name': 'opere',
            #'projects': projects,
            'jsonProj': jsonProj,
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/galleria_progetti.html', args)



#####################
### JSON SERVICES ###
#####################

def filtraProgettiJson(request):
    type = request.GET.get('type')
    bdate = request.GET.get('bdate')
    edate = request.GET.get('edate')
    desc = request.GET.get('desc')
    
    if type is not None and type!="null":
        types=type.split(",")
        variables = {'tipo__in':types,'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
        
    else:
        variables = {'timeinterval__beginningYear__gte':bdate,'timeinterval__endYear__lte':edate,'denominazione__icontains':desc}
    #define filters from query string
    
    projects = Project.objects.all()
    
    #filter the project list
    for key, value in variables.items():
        if value is not None:
            projects = projects.filter(**{key: value})
    
    projects=projects.distinct()
    
    jsonProjs=[]
    
    for p in projects:
        currProj=dict()
        currProj['sigla']=p.sigla
        currProj['nome']=p.denominazione
        currProj['lat']=p.latitude
        currProj['long']=p.longitude
        currProj['tipo']=p.tipo
        currProj['start']=TimeInterval.objects.filter(target=p)[0].beginningYear
        currProj['end']=TimeInterval.objects.filter(target=p).reverse()[0].endYear
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        print p.sigla
        
        
                       
    jsonProj=json.dumps(jsonProjs)
    
    return HttpResponse(jsonProj, mimetype='application/json')





# Show progetti as a map
def mappa_progetti(request):
    projects = Project.objects.all()
    filterValues=dict();
    minDate=2000
    maxDate=0
    types=[]
    
    geoProj={"type": "FeatureCollection", 
             "features":[]}
    
    
    for p in projects:
        if p.latitude is None:
            continue
        currProj=dict()
        currProj["type"]="Feature"
        currProj["id"]=p.id
        
        props=dict()
        props["tipo"]=p.tipo
        props["start"]=TimeInterval.objects.filter(target=p)[0].beginningYear
        props["end"]=TimeInterval.objects.filter(target=p).reverse()[0].endYear        
        props["sigla"]=p.sigla
        props["nome"]=p.denominazione
        
        geom=dict()
        geom["type"]="Point"
        geom["coordinates"]=[p.longitude,p.latitude]
        
        currProj["properties"]=props
        currProj["geometry"]=geom
        
        geoProj["features"].append(currProj);
        
        if props['start']<minDate:
            minDate=props['start']
        
        if props['end']>maxDate:
            maxDate=props['end']
        
        if props['tipo'] is not None and {'des':props['tipo'],'checked':False} not in types:
            types.append({'des':props['tipo'],'checked':False})
        
        
    filterValues['minDate']=minDate;
    filterValues['maxDate']=maxDate;
    filterValues['types']=types;
    jFilterValues=json.dumps(filterValues)
    
    args = {
            'section_name': 'opere',
            'projects': json.dumps(geoProj),
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/mappa_progetti.html', args)



def timeline_progetti(self):
    
    projects = Project.objects.all()
    filterValues=dict();
    minDate=2000
    maxDate=0
    types=[]
    
    timeline={
    "timeline":
    {
        "headline":"Progetti di Baldessari",
        "type":"default",
        "text":"Visualizzazione grafica della cronologia dei progetti",
        "startDate":"1927,0,0",
        'date':[]}
    }
    
    for p in projects:
        
        date=dict()
        date['startDate']=str(TimeInterval.objects.filter(target=p)[0].beginningYear)+",0,0"
        date['endDate']=str(TimeInterval.objects.filter(target=p)[0].endYear)+",0,0"
        date['headline']='<a href="/opere/project/'+p.sigla+'">'+p.denominazione+"</a>"
        date['type']=p.tipo
        if p.related_drawing() is not None:
            date['asset']={"media":'/media/'+p.related_drawing().thumbAdress}
        timeline['timeline']['date'].append(date)
        
        
        if TimeInterval.objects.filter(target=p)[0].beginningYear<minDate:
            minDate=TimeInterval.objects.filter(target=p)[0].beginningYear
        
        if TimeInterval.objects.filter(target=p)[0].endYear>maxDate:
            maxDate=TimeInterval.objects.filter(target=p)[0].endYear
        
        if p.tipo is not None and {'des':p.tipo,'checked':False} not in types:
            types.append({'des':p.tipo,'checked':False})
        
        
    filterValues['minDate']=minDate;
    filterValues['maxDate']=maxDate;
    filterValues['types']=types;
    jFilterValues=json.dumps(filterValues)
    
    print json.dumps(timeline)
    
    args = {
            'section_name': 'opere',
            'projects': json.dumps(timeline),
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/timeline_progetti.html', args)
    

#returns the metadata for one particular document
def viewdoc(request, docsigle):
    document = Drawing.objects.get(segnatura=docsigle)
    project = document.project
    # a project may have more than one TimeInterval - get the first
    date = TimeInterval.objects.filter(target=project)[0]

    related_documents = Drawing.objects.filter(project=project)    
    
    biblio = project.bibliografia.all()
    
    try:
        committente = project.participation_set.filter(role="COM")
    except :
        committente = 'null'
    if(committente.count() == 0): committente = 'null'
    
    try:
        coproj = project.participation_set.filter(role="COP")
    except : 
        coproj = 'null'
    if(coproj.count() == 0): coproj = 'null'
        
    try:
        collab = project.participation_set.filter(role="COL")
    except:
        collab = 'null'
    if(collab.count() == 0): collab = 'null'
    
    params = {
            'section_name': 'opere',
            'project' : project,
            'date' : date,
            'related_documents' : related_documents,
            'biblio' : biblio,

            'committente' : committente,
            'coproj' : coproj,
            'collab' : collab,
            
            'document' : document,
            'segnatura':document.segnatura,
            'cornicce':document.formato_cornice,
            'supporto': document.supporto,
            'collocazione': document.collocazione,
            'tipologia': document.tipo,
            'largezza':document.largezza,
            'altezza':document.altezza,
            'note': document.annotazioni,
            'contenuto': document.cartigli,
            'imageadress' : document.imageAdress
            }
    
    c = RequestContext(request, params)
    
    return render_to_response('archivio/viewdocument.html', c)


#return the metadata for the display of one particular project
def viewproj(requestion, projsigle):
    project = Project.objects.get(sigla=projsigle)
    # a project may have more than one TimeInterval - get the first
    date = TimeInterval.objects.filter(target=project)[0]
    related_documents = Drawing.objects.filter(project=project)
    
    biblio = project.bibliografia.all()
    
    try:
        committente = project.participation_set.filter(role="COM")
    except :
        committente = 'null'
    if(committente.count() == 0): committente = 'null'
    
    try:
        coproj = project.participation_set.filter(role="COP")
    except : 
        coproj = 'null'
    if(coproj.count() == 0): coproj = 'null'
        
    try:
        collab = project.participation_set.filter(role="COL")
    except:
        collab = 'null'
    if(collab.count() == 0): collab = 'null'
    
    
    params = {
            'section_name': 'opere',
            'project' : project,
            'date' : date,
            'related_documents' : related_documents,
            'biblio' : biblio,

            'committente' : committente,
            'coproj' : coproj,
            'collab' : collab
            }
    
    return render_to_response('archivio/viewproject.html', params)




def getInfo(request):
    if request.method == "GET":
        get = request.GET.copy()
        if get.has_key(u'action'):
            action = get[u'action']
            return HttpResponse(functions_dict[action](request, get), mimetype='application/json')
        
 #returns the metadata for all documents       
def getAllDocsList(request, get):
    
    # static_img_path = MEDIA_PATH + 'img_documents/'
    # static_img_path = os.path.join(FILE_PATH, '../static/img_documents/')	#TODO da static a media
    
    info = {}
    info['list'] = []
    listOfDocs = Drawing.objects.all()
    for doc in listOfDocs:
        document = {}
        document['segnatura'] = doc.segnatura
        document['project'] = doc.project.denominazione
        document['tipo'] = doc.project.tipo
        document['projectid'] = doc.project.sigla
        document['address'] = doc.project.address
        
        document['cornicce']=doc.formato_cornice,
        document['supporto']= doc.supporto,
        document['collocazione']= doc.collocazione,
        document['tipologia']= doc.tipo,
        document['largezza']=doc.largezza,
        document['altezza']=doc.altezza,
        document['note']= doc.annotazioni,
        document['contenuto']= doc.cartigli
        
        document['adressthumb'] = doc.thumbAdress
        document['adressimage'] = doc.imageAdress
        
        if doc.data is not None:
            document['data'] =  doc.data.year
        else :
            proj = doc.project
            dateList = TimeInterval.objects.filter(target=proj)
            dates = []
            for dateD in dateList:
                date = {}
                if dateD.begining is not None : date['begining'] = dateD.begining.year
                if dateD.begining is not None : date['end'] = dateD.end.year
                dates.append(date)
            document['data'] = dates
        
        
        
        info['list'].append(document)
    return json.dumps(info)

# returns the metadata for all projects
def getAllProjectsList(request, get):
    # static_img_path = os.path.join(FILE_PATH, '../media/img_documents/')
    # static_img_path = os.path.join(FILE_PATH, '../static/img_documents/')
    info = {}
    info['list'] = []
    listOfProjs = Project.objects.all()

    for proj in listOfProjs:
        project = {}
        project['denominazione'] = proj.denominazione
        project['tipo'] = proj.tipo
        project['sigla'] = proj.sigla
        project['address'] = proj.address
        project['x'] = proj.latitude
        project['y']  = proj.longitude
        relateddocuments = Drawing.objects.filter(project = proj)
        if len(relateddocuments) > 0:
            firstdocument = relateddocuments[0]
            project['segnatura'] = firstdocument.segnatura
            
            #image
            imgFound = False
            adresseT = ''
            adresseI = ''
            for doc in relateddocuments:
                if doc.thumbAdress != 'img_thumbs/noimage.jpg':
                    adresseT = doc.thumbAdress
                    imgFound = True
            if imgFound is False:
                adresseT = 'img_thumbs/noimage.jpg'
                adresseI = 'img_documents/noimage.jpg'
            project['adressthumb'] = adresseT
            project['adressimage'] = adresseI
            
        else:
            project['adressthumb'] = 'img_thumbs/noimage.jpg'
            project['adressimage'] = 'img_documents/noimage.jpg'
            
        dateList = TimeInterval.objects.filter(target=proj)
        dates = []
        for dateD in dateList:
            date = {}
            if dateD.begining is not None : date['begining'] = dateD.begining.year
            if dateD.end is not None : date['end'] = dateD.end.year
            dates.append(date)
        project['data'] = dates
        info['list'].append(project)
        
    return json.dumps(info)


# returns all the types of the projects in order to build the filter menu
def getTipi(request, get):
    info = {}
    info['tipi'] = []
    listOfProjs = Project.objects.all()
    for proj in listOfProjs:
        if len(info['tipi']) == 0:
                info['tipi'].append(proj.tipo)
        else:
            exists = False
            for tipo in info['tipi']:
                if tipo == proj.tipo:
                    exists = True
            if exists is False:
                    info['tipi'].append(proj.tipo)
    return json.dumps(info)

# returns a representation of the number of documents per year in Baldessari's life
def getDatesOverview(request, get):
    info = {}
    info['dates'] = []
    i = 0
    while i < 100:
        info['dates'].append(0)
        i = i + 1
    
    listOfDocs = Drawing.objects.all()
    for doc in listOfDocs:
        if doc.data is not None:
            date = doc.data.year - 1900
            info['dates'][date-1] += 1
        else:
            project = doc.project
            intervals = TimeInterval.objects.filter(target = project)
            for interval in intervals:
                begining = interval.begining.year - 1900
                end = interval.end.year -1900
                j = begining
                while j <= end:
                    info['dates'][j-1] += 1
                    j += 1
    return json.dumps(info)




# dictionary with all get fonctions
functions_dict = {
                  'getAllDocsList': getAllDocsList,
                  'getAllProjectsList': getAllProjectsList,
                  'getTipi' : getTipi,
                  'getDatesOverview' : getDatesOverview
                  }      





#-----FUNCTIONS FOR IMPORT AND EXPORT -----------------------------

def saveDataBase(request):
    call_command('save_json')
    return HttpResponseRedirect("admin/")


def loadDataBase(request):
    call_command('load_json')
    #update_from_json.parseJson((os.path.join(FILE_PATH, 'management/commands/baldessari.json'), BaseCommand.handle(self)))
    return HttpResponseRedirect("admin/")

def saveProjects(request):
    call_command('saveProjects')
    #update_from_json.parseJson((os.path.join(FILE_PATH, 'management/commands/baldessari.json'), BaseCommand.handle(self)))
    return HttpResponseRedirect("admin/")

def loadInizziali(request):
    call_command('update_from_json')
    return HttpResponseRedirect("admin/")




