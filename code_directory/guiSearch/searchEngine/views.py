from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Application
from .models import File
from .models import Component
import operator
import xml.dom.minidom
from xml.dom.minidom import Node
from collections import OrderedDict
from haystack.query import SearchQuerySet
import string
import datetime
from scipy.linalg import norm
import numpy
from .forms import AddDataForm
from .search_indexes import FileIndex
from .search_indexes import ComponentIndex
import copy


def index(request):
    return render(request, 'searchEngine/index.html') 

def about(request):
    return render(request, 'searchEngine/about.html')

def usage(request):
    return render(request, 'searchEngine/usage.html');

def invalidFile(request):#in case of searching without a file, or file is invalid
    return render(request, 'searchEngine/invalidFile.html')

def add_data(request):
# this function generates the form used to add the application data
    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
             return render(request, 'searchEngine/invalidFile.html')
    else:
        form = AddDataForm()

    return render(request, 'searchEngine/add_data.html', {'form': form})


def parse_new_data(request):
    #parse the new data
    if request.method == 'POST':
        if len(request.FILES) > 0:
            #grab the files if they exist
            inputFiles = request.FILES.getlist('files')
        else:
            print("something wrong with the input array")
            return render(request, 'searchEngine/invalidFile.html')
        # adds the application into the database
        app_name = request.POST.get('appName')
        result = add_application(app_name)
        if result == -1:
            print("error with adding application object")
            return render(request, 'searchEngine/invalidFile.html')
        for newfile in inputFiles:
            #copy the file because going through the parser alters the file in some way
            copy_file = copy.deepcopy(newfile)
            file_ret = add_file(result, copy_file)
            if file_ret == -1:
                print("error with adding file object")
                return render(request, 'searchEngine/invalidFile.html')
            comp_ret = add_comp(file_ret, newfile) 
            if comp_ret == -1:
                print("error with adding component objects")
                return render(request, 'searchEngine/invalidFile.html')

    return render(request, 'searchEngine/index.html')

def add_application(app_name):
    # adds the application to the database, returning -1 if the operationg fails
    new_id = Application.objects.all().count() + 1
    app = Application(id=str(new_id), name=app_name)
    try:
        app.save()
    except ValueError:
        return -1
    return app


def add_file(app_name, file_data):
    name = file_data.name
    # parses the file to get a count of total components
    comp_count = parseInputCount(file_data)
    if comp_count == None:
        return -1
    # reads the xml into a string to get put into the database
    xml = file_data.read()
    count_str = ''
    # generates the string stored in component count
    for key, value in comp_count.items():
        count_str += str(key)+ ':' + str(value) + ' '
    new_id = File.objects.all().count() + 1
    # attempts to add the data to the db and returns an error if it fails
    new_file = File(id=str(new_id), app_id=app_name, name=name, total_comps=count_str, xml=xml)
    try:
        new_file.save()
    except ValueError:
        return -1
    # indexes into solr as well
    solr = FileIndex()
    solr.update_object(new_file)
    return new_file


def add_comp(file_name, data):
    new_id = Component.objects.all().count() + 1
    # gets component data from the xml file
    comp_dict = parseInput(data)
    if comp_dict == None:
         return -1
    solr = ComponentIndex()
    # goes through the dictionary returned from the parser and adds the component to the database and to solr
    for key, value in comp_dict.items():
        for indiv_comp in value:
            new_comp = Component(id=str(new_id), file_id=file_name, parent_id='null', name=key, android_id=indiv_comp[0], src=indiv_comp[1], xmlns_android=indiv_comp[2], orientation=indiv_comp[3], layout_height=indiv_comp[4], layout_width=indiv_comp[5], layout_weight=indiv_comp[6], layout_gravity=indiv_comp[7], gravity=indiv_comp[8], layout_margin=indiv_comp[9], layout_marginLeft=indiv_comp[10], layout_marginTop=indiv_comp[11], layout_marginRight=indiv_comp[12], layout_marginBottom=indiv_comp[13], padding=indiv_comp[14], paddingLeft=indiv_comp[15], paddingTop=indiv_comp[16], paddingRight=indiv_comp[17], paddingBottom=indiv_comp[18], clickable=indiv_comp[19], text=indiv_comp[20], textColor=indiv_comp[21], textSize=indiv_comp[22], textStyle=indiv_comp[23], textAppearance=indiv_comp[24], color=indiv_comp[25], background=indiv_comp[26], num_occurrences=indiv_comp[27])
            try:
                new_comp.save()
            except ValueError:
                return -1
            solr.update_object(new_comp)
    return 1

    
########################################### SearchAlgorithm ###################################
def searchAlg(request):
    
    print("this is the length of the file dict" + str(len(request.FILES.getlist('file'))))
    if request.method == 'POST' and len(request.FILES) > 0:
        # Checks to see if the file was successfully passed in
        thefiles = request.FILES.getlist('file')
    appDict = {}
    file_comps = []
    file_names = []
    file_list_len = len(thefiles)
    for thefile in thefiles:
        print("Parsing new file")
        file_names.append(thefile.name)
        data_copy = copy.deepcopy(thefile)
        data = parseInput(thefile)
        input_count = parseInputCount(data_copy)
        if data == None:
            return render(request, 'searchEngine/invalidFile.html')
        file_comps.append(input_count.items())
        appsAlreadyHit = {}
        if data == None:
            return render(request, 'searchEngine/invalidFile.html')
        totalComps = SearchQuerySet().models(Component).all().count()
        for inputCompName, value in data.items():
            print("in the for loop for " + inputCompName)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Loops through all of the components from the file that was passed in
            for entry in value:
                screensAlreadyHit = {}
                count = 0
                results = SearchQuerySet().models(Component).filter(name=inputCompName).raw_search('src:'+entry[1]+' OR '+'orientation:'+entry[3]+' OR '+ 'layout_height:'+entry[4]+' OR '+'layout_width:'+entry[5]+' OR '+'layout_weight:'+entry[6]+' OR '+'layout_gravity:'+entry[7]+' OR '+'gravity:'+entry[8]+' OR '+'layout_margin:'+entry[9]+' OR '+'layout_marginLeft:'+entry[10]+' OR '+'layout_marginTop:'+entry[11]+' OR '+'layout_marginRight:'+entry[12]+' OR '+'layout_marginBottom:'+entry[13]+' OR '+'padding:'+entry[14]+' OR '+'paddingLeft:'+entry[15]+' OR '+'paddingTop:'+entry[16]+' OR '+'paddingRight:'+entry[17]+' OR '+'paddingBottom:'+entry[18]+' OR '+'clickable:'+entry[19]+' OR '+'comp_text:'+entry[20]+' OR '+'textColor:'+entry[21]+' OR '+'textSize:'+entry[22]+' OR '+'textStyle:'+entry[23]+' OR '+'textAppearance:'+entry[24]+' OR '+'color:'+entry[25]+' OR '+'background:'+entry[26])
                # Does a search of all of the attributes of each component, ordered by best match
                # looks through only the top 150 to optimize speed
                for component in results[:150]:
                    count+=1
                    if component.file_id not in screensAlreadyHit:
                        screensAlreadyHit[component.file_id] = 1
                        # if the xml file has already been hit, then we don't want to hit it twice in one component
                        if component.app_id in appDict:
                            # adds the data to a dictionary within a dictionary that keeps a count of how many times an xml file has been seen and an average of the similarity score for the xml file
                            if component.file_id in appDict[component.app_id]:
                                appDict[component.app_id][component.file_id][0] += 1
                                appDict[component.app_id][component.file_id][1] = (appDict[component.app_id][component.file_id][1] + (count/totalComps)) / 2
                            else:
                                appDict[component.app_id][component.file_id] = [1, count/totalComps, component.app_name, component.file_name, component.file_xml, component.file_id]
                            # calculates a running average for the best match of each result returned per screen
                        else:
                            appDict[component.app_id] = { component.file_id:[1, count/totalComps, component.app_name, component.file_name, component.file_xml, component.file_id]}
    results_dict = {}
    for key, file_result in appDict.items():
        # sorts the xml files based on greatest hits and lowest similarity score for each app
        sorted_results = sorted(file_result.values(), key=lambda e:(-e[0], e[1]))
        app_sim_total = -1
        total_hits = 0
        list_name_xml = []
        app_name = ''
        # adds these to a list of results, limiting the number of xml files per application to the number of files submitted in the query
        # this happens for each application to find the best matching xml file per application
        for item in sorted_results[:file_list_len]:
           
            if app_sim_total == -1:
                app_sim_total = item[1]
            else:
                app_sim_total = (app_sim_total + item[1]) / 2
            total_hits += item[0]
            comp_count = SearchQuerySet().models(File).filter(file_id=item[5])[0].total_comps
            list_name_xml.append((item[3], item[4], comp_count))
            app_name = item[2]
        results_dict[key] = [total_hits, app_sim_total, app_name, list_name_xml]
    
    print("finished searching ")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sorted_results = sorted(results_dict.values(), key=lambda e:(-e[0], e[1]))       
    # sorts based on most number of hits, but lowest value of the running average
    ending_dict = {}
    ending_dict['results'] = sorted_results
    ending_dict['input_stuff'] = zip(file_names,file_comps)
            
    return render(request, 'searchEngine/results.html', {'sorted_results': ending_dict})



############################### COUNTING SEARCH ALGORITHM ##############################################
def countSearch(request):
    print("In count search")
    print("this is the length of the file dict" + str(len(request.FILES.getlist('file'))))
    if request.method == 'POST' and len(request.FILES) > 0:
        # Checks to see if the file was successfully passed in
        thefiles = request.FILES.getlist('file')
    appDict = {}
    file_comps = []
    file_names = []
    for thefile in thefiles:
        print("Parsing a new file")
        alreadyHit = {}
        file_names.append(thefile.name)
        # only want one app hit per file search, so this will help find the best matched result
        data = parseInputCount(thefile)
        if data == None:
            return render(request, 'searchEngine/invalidFile.html')
        print("About to start calculating cos sim")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for dbFile in SearchQuerySet().models(File).all():
            countDict = {}
            if dbFile.total_comps == None:
                continue
            for item in dbFile.total_comps:
                # splits up the total_comps list
                splitup = item.split(":")
                if len(splitup) == 2:
                    countDict[splitup[0]] = int(splitup[1])
            if len(countDict.values()) > 0 and dbFile.app_id not in alreadyHit:
                # calculates the cosine similarity and adds it into the application dictionary
                returnVal = simple_cosine_sim(data, countDict)
                alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name,  dbFile.name, dbFile.xml, dbFile.total_comps]
                # if it's not already in the dict add it as the first match for that app
            elif len(countDict.values()) > 0 and dbFile.app_id in alreadyHit:
                returnVal = simple_cosine_sim(data, countDict)
                if returnVal > alreadyHit[dbFile.app_id][0]:
                    # replace with better matching apps throughout the search
                    alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name, dbFile.name, dbFile.xml, dbFile.total_comps]
            
        print ("Finished calculating cos sim. Starting the ranking")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for key, value in alreadyHit.items():
            if key in appDict:
                # if this app has already been seen before (with multi-files this will always happen) aggregate the scores
                appDict[key][0] = (value[0] + appDict[key][0]) / 2
                if value[3] not in appDict[key][3]:
                    # add the file name and xml to the list of relevant files seen
                    appDict[key][3].append((value[3], value[4], value[5]))
            else:
                appDict[key] = [value[0], value[1], value[2], [(value[3], value[4], value[5])]]
        print("finished with one file")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        file_comps.append(data.items())
    sorted_results = sorted(appDict.values(), reverse=True)
    
    ending_dict = {}
    ending_dict['results'] = sorted_results
    ending_dict['input_stuff'] = zip(file_names,file_comps)
      
    return render(request, 'searchEngine/results.html', {'sorted_results': ending_dict})


def simple_cosine_sim(a, b):
    if len(b) < len(a):
        a, b = b, a

    res = 0
    for key, a_value in a.items():
        res += int(a_value) * int(b.get(key, 0))
    if res == 0:
        return 0

    try:
        res = res / norm(list(a.values())) / norm(list(b.values()))
    except ZeroDivisionError:
        res = 0
    return res 

def euclidean_search(request):
    print("this is the length of the file dict" + str(len(request.FILES.getlist('file'))))
    if request.method == 'POST' and len(request.FILES) > 0:
        # Checks to see if the file was successfully passed in
        thefiles = request.FILES.getlist('file')
    appDict = {}
    file_comps = []
    file_names = []
    for thefile in thefiles:
        print("Parsing a new file")
        file_names.append(thefile.name)
        data_copy = copy.deepcopy(thefile)
        data = parseInputHE(thefile)
        input_count = parseInputCount(data_copy)
        file_comps.append(input_count.items())
        alreadyHit = {}
        if data == None:
            return render(request, 'searchEngine/invalidFile.html')
        
        print("About to start calculating euc dist")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for dbFile in SearchQuerySet().models(File).all():
            if dbFile.struc_total == None:
                print("struc total issue " + dbFile.name)
                continue

            if dbFile.app_id not in alreadyHit:
                # if it hasn't been seen, calculate the euclidean distance and add it to the dictionary of applications
                num_data = numpy.array(data).astype(int)
                num_dbFile = numpy.array(dbFile.struc_total).astype(int)
                returnVal = numpy.linalg.norm(num_data - num_dbFile)
                alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name,  dbFile.name, dbFile.xml, dbFile.total_comps]
            elif dbFile.app_id in alreadyHit:
                # if it's already been seen, replace the value in the dictionary if the euclidean distance is less than what's already in the dictionary
                num_data = numpy.array(data).astype(int)
                num_dbFile = numpy.array(dbFile.struc_total).astype(int)
                returnVal = numpy.linalg.norm(num_data - num_dbFile)
                if returnVal < alreadyHit[dbFile.app_id][0]:
                    alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name, dbFile.name, dbFile.xml, dbFile.total_comps]
            
        
        print("Finished calculating, now onto ranking")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # aggregate the results
        for key, value in alreadyHit.items():
            if key in appDict:
                appDict[key][0] = (value[0] + appDict[key][0]) / 2
                if value[3] not in appDict[key][3]:
                    appDict[key][3].append((value[3], value[4], value[5]))
            else:
                appDict[key] = [value[0], value[1], value[2], [(value[3], value[4], value[5])]]
       
        
        print("Finished with one file")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sorted_results = sorted(appDict.values())
    
    ending_dict = {}
    ending_dict['results'] = sorted_results
    ending_dict['input_stuff'] = zip(file_names,file_comps)
       
    return render(request, 'searchEngine/results.html', {'sorted_results': ending_dict})

def hamming_search(request):
    print("this is the length of the file dict" + str(len(request.FILES.getlist('file'))))
    if request.method == 'POST' and len(request.FILES) > 0:
        # Checks to see if the file was successfully passed in
        thefiles = request.FILES.getlist('file')
    appDict = {}
    file_comps = []
    file_names = []
    for thefile in thefiles:
        print("Parsing a new file")
        file_names.append(thefile.name)
        data_copy = copy.deepcopy(thefile)
        data = parseInputHE(thefile)
        input_count = parseInputCount(data_copy)
        file_comps.append(input_count.items())
        alreadyHit = {}
        if data == None:
            return render(request, 'searchEngine/invalidFile.html')
        for dbFile in SearchQuerySet().models(File).all():
            if dbFile.struc_total == None:
                continue
            if dbFile.app_id not in alreadyHit:
                # create a string and calculate the hamming distance
                str_data = ''.join(str(e) for e in data)
                str_dbFile = ''.join(str(e) for e in dbFile.struc_total)
                returnVal = sum(map(operator.ne, str_data, str_dbFile))
                # it's not in the dictionary of already hit applications, so add it in
                alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name,  dbFile.name, dbFile.xml, dbFile.total_comps]
            elif dbFile.app_id in alreadyHit:
                str_data = ''.join(str(e) for e in data)
                str_dbFile = ''.join(str(e) for e in dbFile.struc_total)
                returnVal = sum(map(operator.ne, str_data, str_dbFile))
                # only replace the value if the hamming distance is less than the one already in the dictionary
                if returnVal < alreadyHit[dbFile.app_id][0]:
                    alreadyHit[dbFile.app_id] = [returnVal, 1, dbFile.app_name, dbFile.name, dbFile.xml, dbFile.total_comps]
            

        for key, value in alreadyHit.items():
            # aggregate the results
            if key in appDict:
                appDict[key][0] = (value[0] + appDict[key][0]) / 2
                if value[3] not in appDict[key][3]:
                    appDict[key][3].append((value[3], value[4], value[5]))
            else:
                appDict[key] = [value[0], value[1], value[2], [(value[3], value[4], value[5])]]
            

    sorted_results = sorted(appDict.values())
    
    ending_dict = {}
    ending_dict['results'] = sorted_results
    ending_dict['input_stuff'] = zip(file_names,file_comps)
       
    return render(request, 'searchEngine/results.html', {'sorted_results': ending_dict})



############################### FILE PARSER ##################################
def parseInput(rawfile):
#Store every type of component as key in dictionary. Values are list of lists of attributes of each occurrence for that component type. Returns a hashmap."""
    try:
        dom = xml.dom.minidom.parse(rawfile)
    except xml.parsers.expat.ExpatError:
        return None

    hmap=OrderedDict()
    # Store every type of component as key in dictionary
    # Values are list of lists of attributes of each occurrence for that component type
    for elem in dom.getElementsByTagName("*"):
        if(elem.tagName not in hmap):
	    
            hmap[elem.tagName] = []

        tempList = ['null'] * 28
        for key in elem.attributes.keys():
            if key == "android:id":
                tempList[0] = elem.attributes[key].value
            elif key == "android:src":
                tempList[1] = elem.attributes[key].value
            elif key == "xmlns:android":
                tempList[2] = elem.attributes[key].value
            elif key == "android:orientation":
                tempList[3] = elem.attributes[key].value
            elif key == "android:layout_height":
                tempList[4] = elem.attributes[key].value
            elif key == "android:layout_width":
                tempList[5] = elem.attributes[key].value
            elif key == "android:layout_weight":
                tempList[6] = elem.attributes[key].value
            elif key == "android:layout_gravity":
                tempList[7] = elem.attributes[key].value
            elif key == "android:gravity":
                tempList[8] = elem.attributes[key].value
            elif key == "android:layout_margin":
                tempList[9] = elem.attributes[key].value
            elif key == "android:layout_marginLeft":
                tempList[10] = elem.attributes[key].value
            elif key == "android:layout_marginTop":
                tempList[11] = elem.attributes[key].value
            elif key == "android:layout_marginRight":
                tempList[12] = elem.attributes[key].value
            elif key == "android:layout_marginBottom":
                tempList[13] = elem.attributes[key].value
            elif key == "android:padding":
                tempList[14] = elem.attributes[key].value
            elif key == "android:paddingLeft":
                tempList[15] = elem.attributes[key].value
            elif key == "android:paddingTop":
                tempList[16] = elem.attributes[key].value
            elif key == "android:paddingRight":
                tempList[17] = elem.attributes[key].value
            elif key == "android:paddingBottom":
                tempList[18] = elem.attributes[key].value
            elif key == "android:clickable":
                tempList[19] = elem.attributes[key].value
            elif key == "android:text":
                tempList[20] = elem.attributes[key].value
            elif key == "android:textColor":
                tempList[21] = elem.attributes[key].value
            elif key == "android:textSize":
                tempList[22] = elem.attributes[key].value
            elif key == "android:textStyle":
                tempList[23] = elem.attributes[key].value
            elif key == "android:textAppearance":
                tempList[24] = elem.attributes[key].value
            elif key == "android:color":
                tempList[25] = elem.attributes[key].value
            elif key == "android:background":
                tempList[26] = elem.attributes[key].value
                  
            tempList[27] = 1
        hmap[elem.tagName].append(tempList)
         	
    return hmap



def parseInputCount(rawfile):
#Store every type of component as key in dictionary. Values are list of lists of attributes of each occurrence for that component type. Returns a hashmap."""

    try:
        dom = xml.dom.minidom.parse(rawfile)
    except xml.parsers.expat.ExpatError:
        return None

    hmap=OrderedDict()
    
    # Store every type of component as key in dictionary
    # count how many times you see each one
    for elem in dom.getElementsByTagName("*"):
        if(elem.tagName not in hmap):
	    
            hmap[elem.tagName] = 1
        else:
            hmap[elem.tagName] += 1

    return hmap


def parseInputHE(rawfile):
    
    try:
        dom = xml.dom.minidom.parse(rawfile)
    except xml.parsers.expat.ExpatError:
        return None
    
    # only count specific components
    compCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for elem in dom.getElementsByTagName("*"):
        
        for key in elem.attributes.keys():
            
            if key == "android:orientation":
                compCount[0] += 1
            elif key == "android:layout_height":
                compCount[1] += 1
            elif key == "android:layout_width":
                compCount[2] += 1
            elif key == "android:layout_weight":
                compCount[3] += 1
            elif key == "android:layout_gravity":
                compCount[4] += 1
            elif key == "android:gravity":
                compCount[5] += 1
            elif key == "android:layout_margin":
                compCount[6] += 1
            elif key == "android:layout_marginLeft":
                compCount[7] += 1
            elif key == "android:layout_marginTop":
                compCount[8] += 1
            elif key == "android:layout_marginRight":
                compCount[9] += 1
            elif key == "android:layout_marginBottom":
                compCount[10] += 1
            elif key == "android:padding":
                compCount[11] += 1
            elif key == "android:paddingLeft":
                compCount[12] += 1
            elif key == "android:paddingTop":
                compCount[13] += 1
            elif key == "android:paddingRight":
                compCount[14] += 1
            elif key == "android:paddingBottom":
                compCount[15] += 1
            elif key == "android:clickable":
                compCount[16] += 1
    return compCount
