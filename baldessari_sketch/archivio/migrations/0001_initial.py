# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Actor'
        db.create_table('archivio_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['Actor'])

        # Adding model 'Publication'
        db.create_table('archivio_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('provenance', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sup_infos', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['Publication'])

        # Adding model 'Tematica'
        db.create_table('archivio_tematica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('archivio', ['Tematica'])

        # Adding model 'Project'
        db.create_table('archivio_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tipo2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('denominazione', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('impresa', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('descrizione_prog', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('archivio', ['Project'])

        # Adding M2M table for field bibliografia on 'Project'
        db.create_table('archivio_project_bibliografia', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['archivio.project'], null=False)),
            ('publication', models.ForeignKey(orm['archivio.publication'], null=False))
        ))
        db.create_unique('archivio_project_bibliografia', ['project_id', 'publication_id'])

        # Adding model 'TimeInterval'
        db.create_table('archivio_timeinterval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Project'])),
            ('beginningDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('beginningYear', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('beginningMonth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('beginningDay', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('endYear', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('endMonth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('endDay', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['TimeInterval'])

        # Adding model 'Participation'
        db.create_table('archivio_participation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Actor'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Project'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('archivio', ['Participation'])

        # Adding model 'Letter'
        db.create_table('archivio_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Project'], null=True, blank=True)),
            ('archivio', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dataYear', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dataMonth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dataDay', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('segnatura', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('year', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('imageAdress', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('thumbAdress', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['Letter'])

        # Adding model 'Drawing'
        db.create_table('archivio_drawing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Project'], null=True, blank=True)),
            ('archivio', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dataYear', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dataMonth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dataDay', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prestiti', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('largezza', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('altezza', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('annotazioni', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tecnica', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('supporto', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('segnatura', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('strumento', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('scala', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sigla_archivio', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('multipli', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('restauri', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('formato_cornice', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('collocazione', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('conservazione', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('riproduzione', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('cartigli', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('imageAdress', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('thumbAdress', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['Drawing'])

        # Adding model 'BioDetail'
        db.create_table('archivio_biodetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imgUrl', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('titolo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('testo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('didascalia', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('startDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['BioDetail'])

        # Adding model 'ThemeDetail'
        db.create_table('archivio_themedetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archivio.Tematica'], null=True, blank=True)),
            ('imgUrl', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('titolo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('testo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('didascalia', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('startDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('archivio', ['ThemeDetail'])


    def backwards(self, orm):
        # Deleting model 'Actor'
        db.delete_table('archivio_actor')

        # Deleting model 'Publication'
        db.delete_table('archivio_publication')

        # Deleting model 'Tematica'
        db.delete_table('archivio_tematica')

        # Deleting model 'Project'
        db.delete_table('archivio_project')

        # Removing M2M table for field bibliografia on 'Project'
        db.delete_table('archivio_project_bibliografia')

        # Deleting model 'TimeInterval'
        db.delete_table('archivio_timeinterval')

        # Deleting model 'Participation'
        db.delete_table('archivio_participation')

        # Deleting model 'Letter'
        db.delete_table('archivio_letter')

        # Deleting model 'Drawing'
        db.delete_table('archivio_drawing')

        # Deleting model 'BioDetail'
        db.delete_table('archivio_biodetail')

        # Deleting model 'ThemeDetail'
        db.delete_table('archivio_themedetail')


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
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgUrl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'titolo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'archivio.drawing': {
            'Meta': {'object_name': 'Drawing'},
            'altezza': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'annotazioni': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'archivio': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'cartigli': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'collocazione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'conservazione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dataDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formato_cornice': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'largezza': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'multipli': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dataDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dataYear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageAdress': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgUrl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archivio.Tematica']", 'null': 'True', 'blank': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
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