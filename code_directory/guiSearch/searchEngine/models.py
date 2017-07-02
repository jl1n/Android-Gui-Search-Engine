from django.db import models


#This represents the database schema that fits the current database layout

class Application(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'application'

class File(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    app_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='app_id')
    name = models.CharField(max_length=200)
    total_comps = models.CharField(max_length=1500)
    xml = models.CharField(max_length=60000)
    def __unicode__(self):
        return self.name
    def total_comps_list(self):
        no_colons = self.total_comps.replace(":", "|")
        listy = no_colons.split()
        return listy
    class Meta:
        managed = False
        db_table = 'file'


class Component(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE, db_column='file_id')
    parent_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    android_id = models.CharField(max_length=100)
    src = models.CharField(max_length=100)
    xmlns_android = models.CharField(max_length=100)
    orientation = models.CharField(max_length=100)
    layout_height = models.CharField(max_length=100)
    layout_width = models.CharField(max_length=100)
    layout_weight = models.CharField(max_length=100)
    layout_gravity = models.CharField(max_length=100)
    gravity = models.CharField(max_length=100)
    layout_margin = models.CharField(max_length=100)
    layout_marginLeft = models.CharField(max_length=100)
    layout_marginTop = models.CharField(max_length=100)
    layout_marginRight = models.CharField(max_length=100)
    layout_marginBottom = models.CharField(max_length=100)
    padding = models.CharField(max_length=100)
    paddingLeft = models.CharField(max_length=100)
    paddingRight = models.CharField(max_length=100)
    paddingBottom = models.CharField(max_length=100)
    paddingTop = models.CharField(max_length=100)
    clickable = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    textColor = models.CharField(max_length=100)
    textSize = models.CharField(max_length=100)
    textStyle = models.CharField(max_length=100)
    textAppearance = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    background = models.CharField(max_length=100)
    num_occurrences = models.IntegerField()
    def __unicode__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'component'
    
