# Search index for haystack to use with solr

from haystack import indexes
from .models import Application
from .models import File
from .models import Component
import string

# These classes represent the indexable data from the database tables
# The first entry is always a text object that connects to a txt file in ~/templates/search/indexes/searchEngine/ directory 
class ComponentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    file_id = indexes.CharField()
    file_name = indexes.CharField()
    file_xml = indexes.CharField()
    app_name = indexes.CharField()
    app_id = indexes.CharField()
    name = indexes.CharField(model_attr='name' )
    android_id = indexes.CharField(model_attr='android_id', null=True)
    src = indexes.CharField(model_attr='src', null=True)
    xmlns_android = indexes.CharField(model_attr='xmlns_android', null=True)
    orientation = indexes.CharField(model_attr='orientation', null=True)
    layout_height = indexes.CharField(model_attr='layout_height', null=True)
    layout_width = indexes.CharField(model_attr='layout_width', null=True)
    layout_weight = indexes.CharField(model_attr='layout_weight', null=True)
    layout_gravity = indexes.CharField(model_attr='layout_gravity', null=True)
    gravity = indexes.CharField(model_attr='gravity', null=True)
    layout_margin = indexes.CharField(model_attr='layout_margin', null=True)
    layout_marginLeft = indexes.CharField(model_attr='layout_marginLeft', null=True)
    layout_marginTop = indexes.CharField(model_attr='layout_marginTop', null=True)
    layout_marginRight = indexes.CharField(model_attr='layout_marginRight', null=True)
    layout_marginBottom = indexes.CharField(model_attr='layout_marginBottom', null=True)
    padding = indexes.CharField(model_attr='padding', null=True)
    paddingLeft = indexes.CharField(model_attr='paddingLeft', null=True)
    paddingTop = indexes.CharField(model_attr='paddingTop', null=True)
    paddingRight = indexes.CharField(model_attr='paddingRight', null=True)
    paddingBottom = indexes.CharField(model_attr='paddingBottom', null=True)
    clickable = indexes.CharField(model_attr='clickable', null=True)
    comp_text = indexes.CharField(model_attr='text', null=True)
    textColor = indexes.CharField(model_attr='textColor', null=True)
    textSize = indexes.CharField(model_attr='textSize', null=True)
    textStyle = indexes.CharField(model_attr='textStyle', null=True)
    textAppearance = indexes.CharField(model_attr='textAppearance', null=True)
    color = indexes.CharField(model_attr='color', null=True)
    background = indexes.CharField(model_attr='background', null=True)
    num_occurrences = indexes.CharField(model_attr='num_occurrences', null=True)
    total_num = indexes.CharField()
    struc_count = indexes.MultiValueField()

    def get_model(self):
        return Component

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    # these are all methods that help make searching faster and easier
    def prepare_file_id(self, obj):
        return obj.file_id.id

    def prepare_app_id(self, obj):
        return obj.file_id.app_id.id
    
    def prepare_app_name(self, obj):
        return obj.file_id.app_id.name
    
    def prepare_file_name(self, obj):
        return obj.file_id.name

    def prepare_file_xml(self, obj):
        return obj.file_id.xml

    def prepare_total_num(self, obj):
        total_num = Component.objects.filter(file_id=obj.file_id.id, name=obj.name).count()

        return str(total_num)
    
    def prepare_struc_count(self, obj):
        attr_list = [0]*17
        if obj.orientation != 'null':
            attr_list[0] = 1
        if obj.layout_height != 'null':
            attr_list[1] = 1
        if obj.layout_width != 'null':
            attr_list[2] = 1
        if obj.layout_weight != 'null':
            attr_list[3] = 1
        if obj.layout_gravity != 'null':
            attr_list[4] = 1
        if obj.gravity != 'null':
            attr_list[5] = 1
        if obj.layout_margin != 'null':
            attr_list[6] = 1
        if obj.layout_marginLeft != 'null':
            attr_list[7] = 1
        if obj.layout_marginTop != 'null':
            attr_list[8] = 1
        if obj.layout_marginRight != 'null':
            attr_list[9] = 1
        if obj.layout_marginBottom != 'null':
            attr_list[10] = 1
        if obj.padding != 'null':
            attr_list[11] = 1
        if obj.paddingLeft != 'null':
            attr_list[12] = 1
        if obj.paddingTop != 'null':
            attr_list[13] = 1
        if obj.paddingRight != 'null':
            attr_list[14] = 1
        if obj.paddingBottom != 'null':
            attr_list[15] = 1
        if obj.clickable != 'null':
            attr_list[16] = 1
        
        return attr_list


class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    file_id = indexes.CharField(model_attr='id')
    app_id = indexes.CharField()
    app_name = indexes.CharField()
    total_comps=indexes.MultiValueField()
    name = indexes.CharField(model_attr='name')
    struc_total = indexes.MultiValueField()
    xml = indexes.CharField(model_attr='xml')
    def get_model(self):
        return File

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    # some helper functions to make searching faster later
    def prepare_app_id(self, obj):
        return obj.app_id.id
    
    def prepare_app_name(self, obj):
        return obj.app_id.name
    
    # takes the total component counts stored into the database as one long string into a list
    def prepare_total_comps(self, obj):
        start_str = obj.total_comps.split()
        return start_str
    
    # calculates the structural data for the application 
    def prepare_struc_total(self, obj):
        comps = Component.objects.filter(file_id=obj.id)
        list_of_count = []
        for item in comps:
            attr_list = [0]*17
            if item.orientation != 'null':
                attr_list[0] = 1
            if item.layout_height != 'null':
                attr_list[1] = 1
            if item.layout_width != 'null':
                attr_list[2] = 1
            if item.layout_weight != 'null':
                attr_list[3] = 1
            if item.layout_gravity != 'null':
                attr_list[4] = 1
            if item.gravity != 'null':
                attr_list[5] = 1
            if item.layout_margin != 'null':
                attr_list[6] = 1
            if item.layout_marginLeft != 'null':
                attr_list[7] = 1
            if item.layout_marginTop != 'null':
                attr_list[8] = 1
            if item.layout_marginRight != 'null':
                attr_list[9] = 1
            if item.layout_marginBottom != 'null':
                attr_list[10] = 1
            if item.padding != 'null':
                attr_list[11] = 1
            if item.paddingLeft != 'null':
                attr_list[12] = 1
            if item.paddingTop != 'null':
                attr_list[13] = 1
            if item.paddingRight != 'null':
                attr_list[14] = 1
            if item.paddingBottom != 'null':
                attr_list[15] = 1
            if item.clickable != 'null':
                attr_list[16] = 1
        
            list_of_count.append(attr_list)

        total = [sum(x) for x in zip(*list_of_count)]
        return total 

