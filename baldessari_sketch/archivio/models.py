from django.db import models

# Class Actor describes an "actor" present in the life of Baldessari
# Can be one person, several persons or an abstract group/institution
class Actor(models.Model):
    name = models.CharField(max_length = 100)
    TYPO = (
            ('PE', 'persona'),
            ('GR', 'gruppo'),
            ('N', 'piu persone')
            )
    type = models.CharField(max_length=2, choices=TYPO, default = 'PE')
    note = models.CharField(max_length = 500, null = True, blank = True)
    
    def __unicode__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "Attore"
        verbose_name_plural = "Attori"
    
#a Publication is an element of the bibliography about baldessari / for the moment it is very simple, but it could be upgraded with more precise informations
class Publication(models.Model):
    name = models.CharField(max_length = 500)
    title = models.CharField(max_length = 500, null = True, blank = True)
    provenance = models.CharField(max_length = 500, null = True, blank = True)
    pages = models.CharField(max_length = 500, null = True, blank = True)
    author = models.CharField(max_length = 500, null = True, blank = True)
    date = models.DateField(null = True, blank = True)
    sup_infos = models.CharField(max_length = 500, null = True, blank = True)
    
    def __unicode__(self):
        return self.name  
    class Meta:
        verbose_name = "Pubblicazione"
        verbose_name_plural = "Publicazioni"

# Theme
class Tematica(models.Model):
    name = models.CharField(max_length = 500)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Percorso tematico'
        verbose_name_plural = 'Percorsi tematici'

# Project 
class Project(models.Model):

    sigla = models.CharField(max_length = 10) #the letters that represent the project

    #modelisation of people's participation
    persone = models.ManyToManyField(Actor, through='Participation')
    
    tipo = models.CharField(max_length = 50, blank=True, null=True) # type of project : maybe to remplace by a choice setting
    tipo2 = models.CharField(max_length = 50, blank=True, null=True) #second typology for projects
    
    denominazione = models.CharField(max_length = 500, blank=True) #name of the project
    
    address = models.CharField(max_length = 500, blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True) #geographical coordinates - geocoordinates can be created directly, but i didn't do it to keep it simple
    longitude = models.FloatField(blank=True,null=True)
    
    bibliografia = models.ManyToManyField(Publication, blank = True, null = True) #there can be several publications for one project, a publication can deal with several projects
    
    
    impresa = models.CharField(max_length = 200, null = True)
    
    descrizione_prog = models.TextField(null = True)
    
    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
    
    def __unicode__(self):
        # return self.sigla
        return self.denominazione     # "coercing to Unicode" exception

    def related_drawing(self):
        relateddocuments = Drawing.objects.filter(project = self)
        if len(relateddocuments) > 0:
            draw = relateddocuments[0]
        else:
            draw = None
        return draw
 

# Time interval - used for Projects and Documents
class TimeInterval(models.Model):
    #creating a generic foreign key to be able to link the timeslot to any type of object (not implemented)
    #target = models.ForeignKey(ContentType)
    #object_id = models.PositiveIntegerField()
    #uploaded_item = generic.GenericForeignKey() (not implemented)
    
    target = models.ForeignKey(Project)
    
    beginningDate = models.DateField(blank = True, null = True)
    endDate = models.DateField(blank = True, null = True)

    beginningYear = models.IntegerField(blank = True, null = True)
    beginningMonth = models.IntegerField(blank = True, null = True)
    beginningDay = models.IntegerField(blank = True, null = True)

    endYear = models.IntegerField(blank = True, null = True)
    endMonth = models.IntegerField(blank = True, null = True)
    endDay = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return self.beginningYear

    class Meta:
        verbose_name = "Intervallo di tempo"
        verbose_name_plural = "Intervalli di tempo"
    
# Modelisation of the participation to a project by someone, used as a "through" argument when creating a new project
class Participation(models.Model):
    actor = models.ForeignKey(Actor)
    project = models.ForeignKey(Project)
    ROLE_CHOICE = (
                   ('COP', 'coprogettista'),
                   ('COL', 'collaboratore'),
                   ('COM', 'committente'),
                   ('COS', 'costruttore'),
                   ('COR', 'corrispondente'),
                   )
    role = models.CharField(max_length=3, choices = ROLE_CHOICE)
    
    class Meta:
        verbose_name = "Partecipazione"
        verbose_name_plural = "Partecipazioni"
   
    
    
# Abstract class document which is the superclass of all types of documents implementation 
class Document(models.Model):
    project = models.ForeignKey(Project, blank = True, null = True) #link to a project, blank is turned to True because some documents can not be related to any project / note : can a document be related to several projects? if yes this field has to be turned into a Many-To-Many field

    ARCHIVIO_CHOICE = (
                ('ALB', 'Politecnico di Milano'),
                ('MAR', 'MART'),
                ('CAS', 'CASVA')
                )
    
    archivio = models.CharField(max_length = 3, choices = ARCHIVIO_CHOICE, null = True)

    data = models.DateField(null = True, blank = True)
    dataYear = models.IntegerField(null = True, blank = True)
    dataMonth = models.IntegerField(null = True, blank = True)
    dataDay = models.IntegerField(null = True, blank = True)
    
    class Meta:
        abstract = True


# Class Letter inherits from Document
# represents the hand written documents
class Letter(Document):
    segnatura = models.CharField(max_length = 50, blank = True)
    year = models.DateField(null = True, blank = True)

    imageAdress = models.CharField(max_length = 100, blank = True,null=True)
    thumbAdress = models.CharField(max_length = 100, blank = True,null=True)

    def __unicode__(self):
        return self.segnatura

    class Meta:
        verbose_name = "Carteggio"
        verbose_name_plural = "Carteggi"


# Class Drawing inherits from Document
# represents the images associated to projects
class Drawing(Document):
    prestiti = models.NullBooleanField()
    largezza = models.FloatField(blank=True, null=True)
    altezza = models.FloatField(blank=True, null=True)
    
    annotazioni = models.TextField(blank = True, null=True)
    
    tecnica = models.CharField(max_length = 200,blank = True, null=True)
    supporto = models.CharField(max_length = 200, blank = True,null=True)   
    tipo = models.CharField(max_length = 100, blank = True,null=True)
    segnatura= models.CharField(max_length = 50, blank = True)
    strumento= models.CharField(max_length = 200, blank = True, null=True)
    scala = models.CharField(max_length = 50, blank = True, null=True) #for the moment scale is a charfield, but it should be better as a float
    sigla_archivio = models.CharField(max_length = 10)     
    #from here, there are charfield everywhere but there might not be always necessary
    multipli = models.CharField(max_length = 100, null=True, blank = True)
    restauri = models.CharField(max_length = 100, null=True, blank = True)
    formato_cornice= models.CharField(max_length = 100, blank = True,null=True)
    collocazione= models.CharField(max_length = 100, blank = True,null=True)
    conservazione= models.CharField(max_length = 100, blank = True,null=True)
    riproduzione= models.CharField(max_length = 100, blank = True,null=True)
    cartigli= models.CharField(max_length = 100, blank = True,null=True)
    
    imageAdress = models.CharField(max_length = 100, blank = True,null=True)
    thumbAdress = models.CharField(max_length = 100, blank = True,null=True)
            
    def __unicode__(self):
        return self.segnatura

    class Meta:
        verbose_name = "Disegno"
        verbose_name_plural = "Disegni"


# Class for biographic details
class BioDetail(models.Model):
    imgUrl = models.CharField(max_length = 200,blank = True, null=True)
    titolo = models.CharField(max_length = 500,blank = True, null=True)
    testo = models.CharField(max_length = 500,blank = True, null=True)
    didascalia = models.CharField(max_length = 500,blank = True, null=True)
    startDate = models.DateField(null = True, blank = True)
    endDate = models.DateField(null = True, blank = True)

    def __unicode__(self):
        return self.testo

    class Meta:
        verbose_name = "Dettaglio biografico"
        verbose_name_plural = "Dettagli biografici"
        
        
# Class for biographic details
class ThemeDetail(models.Model):
    tema = models.ForeignKey(Tematica, blank = True, null = True)
    imgUrl = models.CharField(max_length = 200,blank = True, null=True)
    titolo = models.CharField(max_length = 500,blank = True, null=True)
    testo = models.CharField(max_length = 500,blank = True, null=True)
    didascalia = models.CharField(max_length = 500,blank = True, null=True)
    startDate = models.DateField(null = True, blank = True)
    endDate = models.DateField(null = True, blank = True)

    def __unicode__(self):
        return self.testo

    class Meta:
        verbose_name = "Dettaglio tematico"
        verbose_name_plural = "Dettagli tematici"

        