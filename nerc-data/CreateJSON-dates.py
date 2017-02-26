
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import json



#timeUnit="especific day" lunes ... es un dia.. septiembre en dia
dictionary={}
tmp_values=['timeUnit', 'specificDays', 'specificMonth', 'specificWeekdays','specifiedBegining', 'specifiedEnd']
parcial_dict={'timeUnit':['day','week', 'month'],'specificDays':['5','0'], 'specificMonth':['5','0'], 'specificWeekdays':['5','0'], 'specifiedBegining':'0', 'specifiedEnd':'0' }
timeUnit={'day':'0', 'week':'0', 'month':'0' }


with codecs.open('Dates.txt', 'r') as infile:
    content = infile.readlines()
    for i in content:
        temp=i.split("\t")
        for tmp_value in tmp_values:
            if temp[0] and temp[0].strip():
                print "Introducing dataset for :"+tmp_value
                dictionary[temp[0]]={}
                for tmp_value in tmp_values:
                    dictionary[temp[0]][tmp_value]={}

#                print temp[0], tmp_value, parcial_dict.get(tmp_value), len(parcial_dict.get(tmp_value))
                    if len(parcial_dict.get(tmp_value))>1:
                        if parcial_dict.get(tmp_value)[0] == '5':
                            valors_posibles=raw_input("introduce "+tmp_value+" (separated by commas):")
                            valors=valors_posibles.split(",")
                            print temp[0], tmp_value, valors
                            dictionary[temp[0]][tmp_value]=valors
                        else:
                            l=[]
                            for lv in parcial_dict.get(tmp_value):
                                valor_final=None
                                valor_simple = raw_input("introduce 1 if needed "+lv+" : ")
                                if int(valor_simple)==1:
                                    valor_final=lv
                        #dictionary[temp[0]]=dict(tmp_value)
                            dictionary[temp[0]][tmp_value]=valor_final
                    else:
                        valor_simple2 = raw_input("introduce "+tmp_value+" : ")
                        dictionary[temp[0]][tmp_value]=valor_simple2
#print json_list(part_nums)

with open('Dates.json', 'w') as outfile:
    outfile.write(json.dumps(dictionary))
