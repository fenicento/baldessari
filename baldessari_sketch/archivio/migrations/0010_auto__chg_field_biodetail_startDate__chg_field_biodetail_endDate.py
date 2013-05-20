# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BioDetail.startDate'
        db.alter_column('archivio_biodetail', 'startDate', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'BioDetail.endDate'
        db.alter_column('archivio_biodetail', 'endDate', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'BioDetail.startDate'
        db.alter_column('archivio_biodetail', 'startDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'BioDetail.endDate'
        db.alter_column('archivio_biodetail', 'endDate', self.gf('django.db.models.fields.DateField')(null=True))

    models = {
        'archivio.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'})
        },
        'archivio.biodetail': {
            'Meta': {'object_name': 'BioDetail'},
            'didascalia': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'endDate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgUrl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'titolo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'archivio.drawing': {
            'Meta': {'object_name': 'Drawing'},
            'altezza': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'annotazioni': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'archivio': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'attivita': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cartigli': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'collocazione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'conservazione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dataDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formato_cornice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'img_documents/noimage.jpg'", 'max_length': '100'}),
            'imageAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'largezza': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'multipli': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prestiti': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Project']", 'null': 'True', 'blank': 'True'}),
            'restauri': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'riproduzione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'scala': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'segnatura': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sigla_archivio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'strumento': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'supporto': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tecnica': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'thumbAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archivio.letter': {
            'Meta': {'object_name': 'Letter'},
            'archivio': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'attivita': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dataDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Project']", 'null': 'True', 'blank': 'True'}),
            'segnatura': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'thumbAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'archivio.participation': {
            'Meta': {'object_name': 'Participation'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Actor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'archivio.project': {
            'Meta': {'object_name': 'Project'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'bibliografia': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archivio.Publication']", 'null': 'True', 'blank': 'True'}),
            'denominazione': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'descrizione_prog': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impresa': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'luogo': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'materiali': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'persone': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archivio.Actor']", 'through': "orm['archivio.Participation']", 'symmetrical': 'False'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'archivio.publication': {
            'Meta': {'object_name': 'Publication'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'provenance': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'sup_infos': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'archivio.tematica': {
            'Meta': {'object_name': 'Tematica'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'archivio.themedetail': {
            'Meta': {'object_name': 'ThemeDetail'},
            'didascalia': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'endDate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgUrl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Tematica']", 'null': 'True', 'blank': 'True'}),
            'testo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titolo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'archivio.timeinterval': {
            'Meta': {'object_name': 'TimeInterval'},
            'beginningDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'beginningDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'beginningMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'beginningYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'endMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'endYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Project']"})
        }
    }

    complete_apps = ['archivio']