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
from itertools import chain
import json, os.path, re
from django.http import Http404

# import models
from archivio.models import *

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_PATH = settings.MEDIA_ROOT


#return the view of the index - for now, it corresponds to the opere view
def index(request):
    return render_to_response('archivio/index.html')

def working(request, docsigle):
    return render_to_response('archivio/working.html')

def working2(request):
    return render_to_response('archivio/working.html')

def redirect_to_opere(request):
    return HttpResponseRedirect("/opere/progetti/elenco")
    # return HttpResponseRedirect("/opere/")

def redirect_to_elenco_progetti(request):
    return HttpResponseRedirect("/opere/progetti/elenco/")




#returns the global view bibliografia
def bibliografia(request):
    liste  = Publication.objects.all()
    projets = Project.objects.all()
    args = {'section_name': 'bibliografia', 
			'publications' : liste, 
			'projets' : projets}
    return render_to_response('archivio/bibliografia.html', args)

def bibliografia2(request):
    liste  = Publication.objects.all()
    projets = Project.objects.all()
    
    siz=list()
    
    for p in projets:
        a=0
        n=0
        b=dict()
        b['proj']=p.sigla
        b['bib']=list(p.bibliografia.all().order_by("sup_infos").values('name','sup_infos'))
        while n<p.bibliografia.count() :
            a=a+1
            n=(a*a*2)-2
        b['size']=a
        siz.append(b)
        
    proj=list(projets.values('denominazione','sigla'))
    proj=zip(proj,siz)
    print proj
    liste.order_by('date','author')
    
    args = {'section_name': 'bibliografia', 
            'publications' : liste, 
            'projects' : json.dumps(proj)}
    return render_to_response('archivio/bibliografia2.html', args)

def ricerca(request):
    arg = {'section_name': 'ricerca'}
    return render_to_response('archivio/working.html', arg)

def museo_virtuale(request):
    arg = {'section_name': 'museovirtuale'}
    return render_to_response('archivio/working.html', arg)

def contatti(request):
    arg = {'section_name': 'contatti'}
    return render_to_response('archivio/working.html', arg)

def login(request):
    arg = {'section_name': 'login'}
    return render_to_response('archivio/working.html', arg)


#returns the global view opere
def opere(request):  
    return HttpResponseRedirect("/opere/progetti/elenco")

#returns the global view opere
def elenco_progetti(request):

    type = request.GET.get('type')
    bdate = request.GET.get('bdate')
    edate = request.GET.get('edate')
    desc = request.GET.get('desc')
    
    
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
        if p.descrizione_prog is not None:
            currProj['descrizione_prog']=p.descrizione_prog if len(p.descrizione_prog) < 480 else p.descrizione_prog[:480]+"..."
        currProj['start']=TimeInterval.objects.filter(target=p)[0].beginningYear
        currProj['end']=TimeInterval.objects.filter(target=p).reverse()[0].endYear
        currProj['polimi']=Drawing.objects.filter(project=p, archivio="ALB").count()
        currProj['casva']=Drawing.objects.filter(project=p, archivio="CASVA").count()
        currProj['mart']=Drawing.objects.filter(project=p, archivio="MART").count()
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        
       
    
                       
    jsonProj=json.dumps(jsonProjs)
    jFilterValues=json.dumps(getProjectFilterValues())
        
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
    
    proj = request.GET.get('p')
    type = request.GET.get('t')
    tecn = request.GET.get('te')
    scale = request.GET.get('sc')
    instr = request.GET.get('i')
    att = request.GET.get('a')
    supp = request.GET.get('su')
    
    variables=dict()
    drawings=Drawing.objects.all();
    
    if proj is not None:
        variables['project__denominazione__icontains']=proj
    if type is not None:    
        variables['tipo__icontains']=type
    if tecn is not None:    
        variables['tecnica__icontains']=tecn
    if scale is not None:
        variables['scala__icontains']=scale
    if att is not None:
        variables['attivita__icontains']=att
    if instr is not None:
        variables['strumento__icontains']=instr
    if supp is not None:
        variables['supporto__icontains']=supp
        
    for key, value in variables.items():
        
        drawings = drawings.filter(**{key: value})
    
    count=drawings.count()
        
    drawings=drawings[0:29]
    
    drawList=list(drawings.values('archivio','attivita','dataYear','dataMonth','dataDay','largezza','altezza','scala','strumento','tipo','tecnica','supporto','segnatura','thumbAdress','cartigli','project__denominazione'))
    
    if len(drawList) >= count:
        last=drawList[-1]
        last['final']="true"
        print last
    
    atts=getDocsActivities()
    print atts
    
    args = {
            'section_name': 'opere',
            'drawings': json.dumps(drawList),
            'atts' : json.dumps(atts)
            }
    return render_to_response('archivio/documenti.html', args)



def galleria_doc(request):
    
    proj = request.GET.get('p')
    type = request.GET.get('t')
    tecn = request.GET.get('te')
    att = request.GET.get('a')
    scale = request.GET.get('sc')
    instr = request.GET.get('i')
    supp = request.GET.get('su')
    
    variables=dict()
    drawings=Drawing.objects.all();
    
    if proj is not None:
        variables['project__denominazione__icontains']=proj
    if type is not None:    
        variables['tipo__icontains']=type
    if att is not None:
        variables['attivita__icontains']=att
    if tecn is not None:    
        variables['tecnica__icontains']=tecn
    if scale is not None:
        variables['scala__icontains']=scale
    if instr is not None:
        variables['strumento__icontains']=instr
    if supp is not None:
        variables['supporto__icontains']=supp
        
    for key, value in variables.items():
        
        drawings = drawings.filter(**{key: value})
    
    count=drawings.count()
        
    drawings=drawings[0:29]
    
    drawList=list(drawings.values('archivio','attivita','dataYear','dataMonth','dataDay','largezza','altezza','scala','strumento','tipo','tecnica','supporto','segnatura','thumbAdress','cartigli','project__denominazione'))
    
    if len(drawList) >= count:
        last=drawList[-1]
        last['final']="true"
        print last
    
    atts=getDocsActivities()
    
    
    args = {
            'section_name': 'opere',
            'drawings': json.dumps(drawList),
            'atts' : json.dumps(atts)
            }
    return render_to_response('archivio/galleria_doc.html', args)


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
        currProj['polimi']=Drawing.objects.filter(project=p, archivio="ALB").count()
        currProj['casva']=Drawing.objects.filter(project=p, archivio="CASVA").count()
        currProj['mart']=Drawing.objects.filter(project=p, archivio="MART").count()
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        
       
    
                       
    jsonProj=json.dumps(jsonProjs)
    jFilterValues=json.dumps(getProjectFilterValues())
        
    args = {
            'section_name': 'opere',
            #'projects': projects,
            'jsonProj': jsonProj,
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/galleria_progetti.html', args)



def elencoTemi(self):
    themes=Tematica.objects.all();
    themesList=[]
    
    for t in themes:
        td = ThemeDetail.objects.filter(tema = t)[0]
        tl = model_to_dict(t)
        try:
            img = td.imgUrl.replace(".jpg","").replace(".jpeg","").replace(".png","")
            d = Drawing.objects.get(segnatura = img)
            tl['immagine']=(d.imageAdress)
            
        except:
            tl['immagine']="img_documents/noImage.jpg"
        
        themesList.append(tl)

    args= {
           'themes': themesList
           }
    
    return render_to_response('archivio/elencoTemi.html',args)

def viewTheme(request,themeid):
    
    theme = Tematica.objects.get(id=themeid)
    jsonTimeline=dict()
    jsonTheme=dict()
    jsonDetails=list()
    
    jsonTheme['headline']=theme.name
    jsonTheme['type']="default"
    jsonTheme['text']=""
    jsonTheme['date']=list()
    
    
    tdetail= ThemeDetail.objects.filter(tema=theme)
    
    for t in tdetail:
        
        tdict=dict()
        asset=dict()
        details=dict()
        res=parseTheme(t.testo)
        
        tdict['startDate'] = str(t.startDate)+",0,0"
        tdict['endDate'] = str(t.endDate)+",0,0"
        tdict['headline'] = t.titolo
        
        # d=Drawing.objects.filter(imageAdress__icontains=t.imgUrl)
        # if d:
            # asset['media'] = '/media/'+d[0].imageAdress
            # asset['caption'] = d[0].tipo
        # else:
            # d=Letter.objects.filter(imageAdress__icontains=t.imgUrl)
#              
            # if d:
                # asset['media'] = '/media/'+d[0].imageAdress
                # asset['caption'] = t.didascalia
            # else:
                # asset['media']="img_documents/noImage.jpg"
                # asset['caption'] = t.didascalia
        
        asset['media'] = t.immagine.url
        asset['caption'] = t.didascalia    
        tdict['asset']=asset
        tdict['testo'] = res['text']
        #tdict['testo'] = t.testo
        
        details['projects']=res['projects']
        details['themes']=res['themes']
        details['images']=res['images']
        details['actors']=res['actors']
        
        jsonDetails.append(details)
        jsonTheme['date'].append(tdict)
        
   
     
    jsonTimeline['timeline'] = jsonTheme
        
    args={
          "jsonTheme":json.dumps(jsonTimeline),
          "jsonDetails":json.dumps(jsonDetails)
          }
    
    
    
    return render_to_response('archivio/viewTheme.html',args)


def biografia(request):
    
    
    tdetail= BioDetail.objects.all()
    jsonTimeline=dict()
    jsonTheme=dict()
    jsonDetails=list()
    
    jsonTheme['headline']='Biografia di Luciano Baldessari'
    jsonTheme['type']="default"
    jsonTheme['text']=""
    jsonTheme['date']=list()
    
    for t in tdetail:
        
        tdict=dict()
        asset=dict()
        details=dict()
        res=parseTheme(t.testo)
        
        splitext=res['text'].split("OPERE")
        if len(splitext)>1:
            splitext[1]=splitext[1].replace("<br /><br />","<br />")
            res['text']=splitext[0]+"OPERE"+splitext[1]
        
            
        
        
        tdict['startDate'] = str(t.startDate)+",0,0"
        tdict['endDate'] = str(t.endDate)+",0,0"
        tdict['headline'] = t.titolo
        
        result = re.sub(r'\[\[([^\]|]*)\|?([^\]|]*)\]\]', r'<a href="\2">\1</a>', t.didascalia)
        #result=re.sub(r'(class=)"http.+?"',r'\1"ext-link"',result)
        
        
        asset['media'] = t.immagine.url
        asset['caption'] = result
       
            
        tdict['asset']=asset
        tdict['testo'] = res['text']
        #tdict['testo'] = t.testo
        
        details['projects']=res['projects']
        details['themes']=res['themes']
        details['images']=res['images']
        details['actors']=res['actors']
        
        jsonDetails.append(details)
        jsonTheme['date'].append(tdict)
        
   
     
    jsonTimeline['timeline'] = jsonTheme
        
    args={
          "jsonTheme":json.dumps(jsonTimeline),
          'section_name': 'biografia',
          "jsonDetails":json.dumps(jsonDetails)
          }
    
    
    
    return render_to_response('archivio/viewTheme.html',args)
    
#####################
### JSON SERVICES ###
#####################



def acProjName(request):
    
    term = request.GET.get('query')
    projects = Project.objects.filter(denominazione__icontains=term)[:8].values_list('denominazione', flat=True)
    
    resp=dict()
    
    resp['suggestions']=list(projects)
    resp['query']=term
    
    
    jsonProj=json.dumps(resp)
    
    return HttpResponse(jsonProj, mimetype='application/json')


def acActorName(request):
    
    term = request.GET.get('query')
    actors = Actor.objects.filter(name__icontains=term)[:8].values_list('name', flat=True)
    
    resp=dict()
    
    resp['suggestions']=list(actors)
    resp['query']=term
    
    
    jsonProj=json.dumps(resp)
    
    return HttpResponse(jsonProj, mimetype='application/json')





def acDoc(request):
    
    term = request.GET.get('query')
    attr = request.GET.get('attr')
    variables = {attr+'__icontains':term}
    drawings=Drawing.objects.all()
    for key, value in variables.items():
        if value is not None:
            drawings = drawings.filter(**{key: value}).distinct()[:8].values_list(attr, flat=True)
    
    resp=dict()
    
    resp['suggestions']=list(drawings)
    resp['query']=term
    
    
    jsonProj=json.dumps(resp)
    
    return HttpResponse(jsonProj, mimetype='application/json')




##### JSON SERVICE FOR LISTS AND GALLERIES #####

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
        if p.descrizione_prog is not None:
            currProj['descrizione_prog']=p.descrizione_prog if len(p.descrizione_prog) < 480 else p.descrizione_prog[:480]+"..."
        currProj['start']=TimeInterval.objects.filter(target=p)[0].beginningYear
        currProj['end']=TimeInterval.objects.filter(target=p).reverse()[0].endYear
        currProj['polimi']=Drawing.objects.filter(project=p, archivio="ALB").count()
        currProj['casva']=Drawing.objects.filter(project=p, archivio="CASVA").count()
        currProj['mart']=Drawing.objects.filter(project=p, archivio="MART").count()
        try:
            currProj['thumb']=p.related_drawing().thumbAdress
        except:
            currProj['thumb']='img_documents/nothumb.jpg'
        jsonProjs.append(currProj)
        print p.sigla
        
        
                       
    jsonProj=json.dumps(jsonProjs)
    
    return HttpResponse(jsonProj, mimetype='application/json')




##### JSON SERVICE FOR FORCE DIRECTED GRAPH #####

def filtraReteJson(request):
    
    actors= Actor.objects.all()
    desc = request.GET.get('desc')

    
    variables = {'name__icontains':desc}
        

    
    #filter the project list
    for key, value in variables.items():
        if value is not None:
            actors= actors.filter(**{key: value})

    actors=actors.distinct()

    nodes=[]
    links=[]
    existing=[]
    
    pos=0;
    
    for a in actors:
        
        node=dict()
        
        #node['id']=p.id
        node['group']=0;
        #node['name']=p.denominazione
        #node['sigla']=p.sigla
        node['name']=a.name
        node['id']=a.id
        
        
        nodes.append(node)
        
        apos=0;
        projects=Project.objects.filter(persone=a)
        node['size']=4+len(projects)*1.5
        for p in projects:
            
            link=dict()
            
            ex=next((x for x in existing if x['sigla'] == p.sigla), None)
            
            if ex is None:
                
                
                apos=apos+1;
                
                anode=dict()
                anode['id']=a.id
                anode['group']=1;
                anode['name']=p.denominazione
                anode['size']=5;
                anode['sigla']=p.sigla
                nodes.append(anode)
                existing.append(anode)
                
                link['source']=pos
                link['target']=pos+apos
                link['value']=1
            
            else:
               
                
                ind=nodes.index(ex)
                ex['size']=ex['size']+0.2
                
                
                link['source']=pos
                link['target']=ind
                link['value']=1
                    
            
            links.append(link)
        
        pos=pos+apos+1;
        
        
       
        
    netdata=dict()
    netdata['nodes']=nodes
    netdata['links']=links
    
    
    return HttpResponse(json.dumps(netdata), mimetype='application/json')
    
    

### JSON SERVICE FOR DOCUMENTS - FILTER AND INFINITE SCROLLING ###

def documentiJson(request):
    
    #type = request.GET.get('type')
    #bdate = request.GET.get('bdate')
    #edate = request.GET.get('edate')
    ind = float(request.GET.get('ind'))
    proj = request.GET.get('p')
    type = request.GET.get('t')
    att = request.GET.get('a')
    tecn = request.GET.get('te')
    scale = request.GET.get('sc')
    instr = request.GET.get('i')
    supp = request.GET.get('su')
    
    variables=dict()
    drawings=Drawing.objects.all();
     
    if proj is not None:
        variables['project__denominazione__icontains']=proj
    if type is not None:    
        variables['tipo__icontains']=type
    if att is not None:    
        variables['attivita__icontains']=att
    if tecn is not None:    
        variables['tecnica__icontains']=tecn
    if scale is not None:
        variables['scala__icontains']=scale
    if instr is not None:
        variables['strumento__icontains']=instr
    if supp is not None:
        variables['supporto__icontains']=supp
        
    for key, value in variables.items():
        
        drawings = drawings.filter(**{key: value})
        
    count= drawings.count()
    
    num=30
    
    sind=ind*30
    eind=sind+30
    drawings = drawings[sind:eind]    # TODO eliminare limite di 10 elementi
    
            
    jdrawings= list(drawings.values('archivio','attivita','dataYear','dataMonth','dataDay','scala','largezza','altezza','tipo','strumento','tecnica','supporto','segnatura','thumbAdress','project__denominazione','cartigli'))
    length=len(jdrawings)
    print length
   
    
    if int(length+sind) >= count:
        
       
        try:
            last=jdrawings[-1]
            last['final']="true"
        except Exception as e:
            print e.message
           
    
        
       
    
    return HttpResponse(json.dumps(jdrawings), mimetype='application/json')

### JSON SERVICE FOR CARTEGGI - GALLERIA ###

def carteggiJson(request):
    ind=float(request.GET.get('ind'))
    proj=request.GET.get('proj')
    
    num=30
    sind=ind*num+1
    eind=ind*num+num
    
    
    thisProj=Project.objects.get(sigla=proj)
    cart=Letter.objects.filter(project=thisProj)[sind:eind]
    
    jcart=json.dumps(list(cart.values('imageAdress')))
    return HttpResponse(jcart, mimetype='application/json')


# Show progetti as a map
def mappa_progetti(request):
    projects = Project.objects.all()
    
    
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
        
      
    jFilterValues=json.dumps(getProjectFilterValues())
    
    args = {
            'section_name': 'opere',
            'projects': json.dumps(geoProj),
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/mappa_progetti.html', args)



def timeline_progetti(self):
    
    projects = Project.objects.all()
    
    
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
        date['endDate']=str(TimeInterval.objects.filter(target=p).reverse()[0].endYear)+",0,0"
        date['headline']='<a href="/opere/project/'+p.sigla+'">'+p.denominazione+"</a>"
        date['type']=p.tipo
        if p.related_drawing() is not None:
            date['asset']={"media":'/media/'+p.related_drawing().thumbAdress}
        timeline['timeline']['date'].append(date)
        
        
       
    jFilterValues=json.dumps(getProjectFilterValues())
    
    print json.dumps(timeline)
    
    args = {
            'section_name': 'opere',
            'projects': json.dumps(timeline),
            'filterValues' : jFilterValues
            }
    return render_to_response('archivio/timeline_progetti.html', args)


def rete_progetti(request):
    
    actors= Actor.objects.all()
    desc = request.GET.get('desc')

    
    variables = {'name__icontains':desc}
        

    
    #filter the project list
    for key, value in variables.items():
        if value is not None:
            actors= actors.filter(**{key: value})

    actors=actors.distinct()

    nodes=[]
    links=[]
    existing=[]
    
    pos=0;
    
    for a in actors:
        
        node=dict()
        
        #node['id']=p.id
        node['group']=0;
        #node['name']=p.denominazione
        #node['sigla']=p.sigla
        node['name']=a.name
        node['id']=a.id
        
        
        nodes.append(node)
        
        apos=0;
        projects=Project.objects.filter(persone=a)
        node['size']=4+len(projects)*1.5;
        for p in projects:
            
            link=dict()
            
            ex=next((x for x in existing if x['sigla'] == p.sigla), None)
            
            if ex is None:
                
                
                apos=apos+1;
                
                anode=dict()
                anode['id']=a.id
                anode['group']=1;
                anode['name']=p.denominazione
                anode['size']=5;
                anode['sigla']=p.sigla
                nodes.append(anode)
                existing.append(anode)
                
                link['source']=pos
                link['target']=pos+apos
                link['value']=1
            
            else:
               
                
                ind=nodes.index(ex)
                ex['size']=ex['size']+0.2
                
                
                link['source']=pos
                link['target']=ind
                link['value']=1
                    
            
            links.append(link)
        
        pos=pos+apos+1;
        
        
       
        
    netdata=dict()
    netdata['nodes']=nodes
    netdata['links']=links
    
    
   
    jFilterValues=json.dumps(getProjectFilterValues())
    
    args = {
            'section_name': 'opere',
            'projects': json.dumps(netdata),
            'filterValues' : jFilterValues
            }
    
    return render_to_response('archivio/rete_progetti.html', args)
    
    

#returns the metadata for one particular document
def viewdoc(request, docsigle):
    document=None
    project=None
    date=None
    try:
        document = Drawing.objects.filter(segnatura__icontains=docsigle)[0]
        print document.tecnica
    except:
        try:
            document = Letter.objects.filter(segnatura__icontains=docsigle)[0]
        except:
            raise Http404
    if document is not None:
        if document.project is not None:
            project = document.project
            # a project may have more than one TimeInterval - get the first
            date = TimeInterval.objects.filter(target=project)[0]

   
    
    params = {
            'section_name': 'opere',
            'project' : project,
            'date' : date,
           
            
            'document' : document,
            }
    
    c = RequestContext(request, params)
    
    return render_to_response('archivio/viewdoc.html', c)


#return the metadata for the display of one particular project
def viewproj(requestion, projsigle):
    project = Project.objects.get(sigla=projsigle)
    # a project may have more than one TimeInterval - get the first
    date = TimeInterval.objects.filter(target=project)
    related_documents = Drawing.objects.filter(project=project)
    polimi = related_documents.filter(archivio="ALB").count()
    casva = related_documents.filter(archivio="CASVA").count()
    mart = related_documents.filter(archivio="MART").count()
    carteggi = Letter.objects.filter(project=project)
    
    
    biblio = project.bibliografia.all().order_by("-sup_infos")
    
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
    
    try:
        corr = project.participation_set.filter(role="COR")
    except:
        corr = 'null'
    if(corr.count() == 0): corr = 'null'
    
    try:
        costr = project.participation_set.filter(role="COS")
    except:
        costr = 'null'
    if(costr.count() == 0): costr = 'null'
    
    try:
        artist = project.participation_set.filter(role="A")
    except:
        artist = 'null'
    if(artist.count() == 0): artist = 'null'
    
    if project.descrizione_prog is not None:
        project.descrizione_prog=project.descrizione_prog.replace("\n","<br />")
    
    
    params = {
            'section_name': 'opere',
            'project' : project,
            'date' : date,
            'related_documents' : related_documents,
            'polimi' : polimi,
            'casva' : casva,
            'mart' : mart,
            'carteggi_count' : carteggi.count(),
            'carteggi':carteggi[:30],
            'biblio' : biblio,

            'committente' : committente,
            'coproj' : coproj,
            'collab' : collab,
            'corr' : corr,
            'costr' : costr,
            'artist' : artist
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

#filter values for projects
def getProjectFilterValues():
    
    projects = Project.objects.all()
    filterValues=dict();
    minDate=2000
    maxDate=0
    types=[]
    
    for p in projects:
        if TimeInterval.objects.filter(target=p)[0].beginningYear<minDate:
            minDate=TimeInterval.objects.filter(target=p)[0].beginningYear
        
        if TimeInterval.objects.filter(target=p).reverse()[0].endYear>maxDate:
            maxDate=TimeInterval.objects.filter(target=p)[0].endYear
        
        if p.tipo is not None and {'des':p.tipo,'checked':False} not in types:
            types.append({'des':p.tipo,'checked':False})
        
        
    filterValues['minDate']=minDate;
    filterValues['maxDate']=maxDate;
    filterValues['types']=types;
    
    return filterValues

def getDocsActivities():
    
    docs = Drawing.objects.all()
    atts=[];

    for p in docs:
        
        
        if p.attivita is not None and p.attivita not in atts:
            atts.append(p.attivita)
        
    
    return atts

def parseTheme(text):
    
    res=dict()
    result = re.sub(r'\[\[([^\]|]*)\|?([^\]|]*)\]\]', r'<a class="\2" href="\2">\1</a>', text)
    
    #find actors
    actors=re.findall(r'[!class="]person:(\d+)"',result)
    print "actors"
    print actors
    #find projects
    projects=re.findall(r'[!class="]proj:(.+?)"',result)
    print "projects"
    print projects
    #find images
    imgs=set(re.findall(r'[!class="]img:(.+?)"',result))
    print "images"
    print imgs
    #find themes
    themes=re.findall(r'[!class="]theme:(.+?)"',result)
    print "themes"
    print themes
    

    
    result=re.sub(r'(class=)"proj:.+?"',r'\1"proj-link"',result)
    result=re.sub(r'(class=)"img:.+?"',r'\1"img-link"',result)
    result=re.sub(r'(class=)"person:.+?"',r'\1"act-link"',result)
    result=re.sub(r'(class=)"theme:.+?"',r'\1"theme-link"',result)
    result=re.sub(r'(class=)"http.+?"',r'\1"ext-link"',result)
    
    
    result=re.sub(r'(proj:)',r'/opere/project/',result)
    result=re.sub(r'(img:)',r'/opere/document/',result)
    result=re.sub(r'(person:)',r'/persone/?el=',result)
    result=re.sub(r'(theme:)',r'/tema/',result)
    
    
    result=result.replace("\n","<br /><br />")
    
    actors=map(int, actors)
    
    imgString="("
    imgStringBody="|".join(str(item) for item in imgs)
    imgString=imgString+imgStringBody+".+)"
   
    
    actorObjs = Actor.objects.filter(id__in=actors).values('id','name')
    projObjs = Project.objects.filter(sigla__in=projects).values('sigla','denominazione')
    themeObjs = Tematica.objects.filter(id__in=themes).values('id','name')
    
    images=list()
    letters=list()
    
    for item in imgs:
        
        currImgs = Drawing.objects.filter(segnatura__icontains=item).values('segnatura','thumbAdress')
        if currImgs:
            print item
            print 'found' +str(currImgs[0]) 
            currImgs=currImgs[0]
            images.append(currImgs)
            
        currLett = Letter.objects.filter(segnatura__icontains=item).values('segnatura','thumbAdress')    
        if currLett:
            print item
            print 'found' +str(currLett[0]) 
            currLett=currLett[0]
            letters.append(currLett)
    
    
    print images
    print letters
    
    res['text']=result
    res['actors']=list(actorObjs),
    res['projects']=list(projObjs),
    res['themes']=list(themeObjs),
    res['images']=list(chain(images,letters))
    
    
    return res



