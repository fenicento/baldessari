#-*- coding:Latin-1 -*
# Create your views here.
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from archivio.models import *
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.template import RequestContext
import json
from management.commands import update_from_json
import os.path
from os.path import exists
from string import split
import re
FILE_PATH = os.path.dirname(os.path.abspath(__file__))


#return the view of the index - for now, it corresponds to the opere view
def index(request):
    return render_to_response('archivio/index.html')

def redirect_to_opere(request):
    return HttpResponseRedirect("/opere/")

#returns the global view biografia
def biografia(request):
    return render_to_response('archivio/test_arguments.html', {'section_name': 'biografia'})

#returns the global view bibliografia
def bibliografia(request):
    liste  = Publication.objects.all()
    projets = Project.objects.all()
        
    return render_to_response('archivio/bibliografia.html', {'section_name': 'bibliografia','publications' : liste, 'projets' : projets})

def ricerca(request):
    return render_to_response('archivio/test_arguments.html', {'section_name': 'ricerca'})

def museo_virtuale(request):
    return render_to_response('archivio/test_arguments.html', {'section_name': 'museovirtuale'})

def contatti(request):
    return render_to_response('archivio/test_arguments.html', {'section_name': 'contatti'})

def login(request):
    return render_to_response('archivio/test_arguments.html', {'section_name': 'login'})


#returns the global view opere
def opere(request):  
    args = {
                'section_name': 'opere'
            }
    return render_to_response('archivio/opere.html', args)




#returns the metadata for one particular document
def viewdoc(request, docsigle):
    document = Drawing.objects.get(segnatura=docsigle)
    project = document.project
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
    
    static_img_path = os.path.join(FILE_PATH, '../static/img_documents/')
    
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

#returns the metadata for all projects
def getAllProjectsList(request, get):
    static_img_path = os.path.join(FILE_PATH, '../static/img_documents/')
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


#returns all the types of the projects in order to build the filter menu
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

#returns a representation of the number of documents per year in Baldessari's life
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



#dictionnary with all get fonctions
functions_dict = {
                  'getAllDocsList': getAllDocsList,
                  'getAllProjectsList': getAllProjectsList,
                  'getTipi' : getTipi,
                  'getDatesOverview' : getDatesOverview
                  }      





#-----FUNCTIONS OF IMPORT AND EXPORT -----------------------------

def saveDataBase(request):
    call_command('save_json')
    return HttpResponseRedirect("admin/")


def loadDataBase(request):
    call_command('load_json')
    #update_from_json.parseJson((os.path.join(FILE_PATH, 'management/commands/baldessari.json'), BaseCommand.handle(self)))
    return HttpResponseRedirect("admin/")

def loadInizziali(request):
    call_command('update_from_json')
    return HttpResponseRedirect("admin/")




