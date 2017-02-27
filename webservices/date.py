# -*- coding: utf-8 -*-

import json
import time
import warnings
from datetime import timedelta, date
from copy import deepcopy
from pprint import pprint



from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin

from lxml import etree
import os
import sys
from subprocess import Popen, PIPE
import re
import codecs
import json


#informacion: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask



app = Flask(__name__)

CORS(app)



@app.route('/findDates', methods=['POST'])

def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    else:
        return parse_file(request.json['title'])



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def parse_file(document):
#    text = "Hola me ll Naiara Perez y vivo en Donostia. Naiara Perez es muy majo. Quiero ir a un Concierto a Barcelona pasado mañana."
    #print result
    with open('../TemporalAnalysis/Fechas.json') as json_data:
        d = json.load(json_data)
        print(d)
#    data = {"dias que sean martes y 13 en los siguientes 10 years": {'timeUnit':'year','specificWeekdays':['martes'],'specificDays': [13],'specifiedEnd':10}}

#    pprint(data)
    text=parseJsonInput(d[document])
    print data.keys()
    return text
    #return result

"""Some functions to filter from NLP to a datetime span. Incredibly hardcoded, but hopefully, useful."""
def daterange(start_date, end_date):
    """iterates over different dates"""
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + timedelta(n)

def timeUnitConvert(timeUnit):
    """Converts the timespan of the time unit to num. of days"""
    if timeUnit == 'day':
        return 1
    elif timeUnit == 'week':
        return 7
    elif timeUnit == 'month':
        currentYear = time.localtime()[0]
        currentMonth = time.localtime()[1]
        if currentMonth in [1,3,5,7,8,10,12]:
            return 31
        elif currentMonth == 2:
            if currentYear % 4 == 0:
                "All this stuff is for leap years"
                if currentYear % 100 == 0 and currentYear %400==0:
                    return 29
                elif currentYear % 4 == 0 and currentYear % 100 != 0:
                    return 29
                else:
                    return 28
            return 28
        else:
            return 30
    elif timeUnit == 'year':
        return 365
    else:
        warnings.warn('Unexpected timespan, returning as 1')
        return 1


def isWeekday(timestamp):
    """Given a timestam if its a weekday written in EN/ES returns its index +1 (for consistency with datetime package)"""
    daylist_en = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    daylist_es = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo'] #please no tildes
    if timestamp in daylist_en:
        return daylist_en.index(timestamp)
    elif timestamp in daylist_es:
        return daylist_es.index(timestamp)
    else:
        return None

def isMonth(timestamp):
    """Given a timestam if its a month written in EN/ES returns its index +1 (for consistency with datetime package)"""
    monthlist_en = ['january','february','march','april','may','june','july','august','september','october','november','december']
    monthlist_es = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    if timestamp in monthlist_en: return monthlist_en.index(timestamp)+1
    if timestamp in monthlist_es: return monthlist_es.index(timestamp)+1
    return None

def filterMonths(outputTimespan,specificMonths):
    """Given a list of datetimes, filters those which are not in the specified months"""
    timespanCopy = deepcopy(outputTimespan)
    monthsToPreserve = []
    for selectedMonth in specificMonths:
        monthIndex = isMonth(selectedMonth)
        monthsToPreserve.append(monthIndex)
    for outputTime in outputTimespan:
        if outputTime.month not in monthsToPreserve: timespanCopy.remove(outputTime)
    return timespanCopy

def filterDays(outputTimespan,specificDays):
    """Given a list of datetimes, filters those which are not in the specified Days"""
    timespanCopy = deepcopy(outputTimespan)
    for outputTime in outputTimespan:
        if outputTime.day not in specificDays: timespanCopy.remove(outputTime)
    return timespanCopy

def filterWeekdays(outputTimespan,specificWeekdays):
    """Given a list of datetimes, filters those which are not in the specified Weekdays"""
    timespanCopy = deepcopy(outputTimespan)
    weekdaysToPreserve = []
    for selectedDay in specificWeekdays:
        weekdayIndex = isWeekday(selectedDay)
        weekdaysToPreserve.append(weekdayIndex)
    for outputTime in outputTimespan:
        if outputTime.weekday() not in weekdaysToPreserve: timespanCopy.remove(outputTime)
    return timespanCopy

def filterDaysAndMonths(outputTimespan,specificDays,specificMonths,specificWeekdays):
    """Filters those values from the output timespan that does not correspond to the specific days and months"""
    if specificMonths is not None: outputTimespan = filterMonths(outputTimespan,specificMonths)
    if specificDays is not None: outputTimespan = filterDays(outputTimespan,specificDays)
    if specificWeekdays is not None: outputTimespan = filterWeekdays(outputTimespan,specificWeekdays)
    return outputTimespan


def date_to_span( timeUnit='day', specificDays=None,specificMonths=None, specificWeekdays = None, specifiedBeginning = None, specifiedEnd = None, specialDay = None):
    """Calculates a timespan of possible values.
    Input:
        --timeUnit: {day, week, month} - the unit of time to measure the interval.
        --specificDays = List of str or None {monday, tuesday, wednesday, thursday, friday, saturday, sunday}
                        Specific days that should only be on the timespan
        --specificMonths = List of str or None {january, february,... and so on}, the same as above but with months
        --specifiedBeggining = weekday/month If the user has specified any beggining day/month "El primer concierto en las primeras dos semanas de febrero"
        --specifiedEnd = integer/weekday/month If the user has specified any ending day/month "Todos los conciertos hasta el viernes, En los proximos tres dias."


    Output:
        List (or json?) of strings corresponding to date/time.
        """
    #Some sanity check for the input
    if specificWeekdays is not None:
        if not isinstance(specificWeekdays,list): specificWeekdays = [specificWeekdays]
    if specificDays is not None:
        if not isinstance(specificDays,list): specificDays = [specificDays]
    if specificMonths is not None:
        if not isinstance(specificMonths,list): specificMonths = [specificMonths]
    outputTimespan = []
    today = time.localtime()
    curYear, curMonth, curDay , curWeekday ,curYearday= today[0],today[1], today[2], today[7], today[8]
    timeUnitInt = timeUnitConvert(timeUnit)
    if specialDay is not None:
        if specialDay == 'manana':
            return [date(curYear,curMonth,curDay)+timedelta(1)]
        elif specialDay == 'pasadomanana':
            return [date(curYear,curMonth,curDay)+timedelta(2)]
        elif specialDay == 'navidad':
            return [date(curYear,12,24)]
        elif specialDay == 'siguientemes':
            dayIter = 0
            startDate = None
            endDate = None
            todayDate = date(curYear,curMonth,curDay)
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.month == curMonth+1 and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.month == curMonth+2:
                    endDate = nextDay
                    break

                dayIter += 1
            for singleDate in daterange(startDate, endDate):
                outputTimespan.append(singleDate)
                outputTimespan = filterDaysAndMonths(outputTimespan,specificDays,specificMonths,specificWeekdays)
            return outputTimespan


        #Se pueden hardcodear asi todos los que quieras
    if isinstance(specifiedEnd,int) and specifiedBeginning is None:
        "Timespan desde hoy hasta el dia Today +X, es decir e.g: quiero un concierto dentro de los dos dias siguientes"
        startDate = date(curYear,curMonth,curDay)
        endDate = startDate + timedelta(timeUnitInt*specifiedEnd)


    elif isinstance(specifiedEnd,(str,unicode)) and specifiedBeginning is None:
        "Dime los conciertos hasta febrero / el viernes"
        todayDate = date(curYear,curMonth,curDay)
        month = isMonth(specifiedEnd)
        endYear = curYear
        startDate = todayDate
        if month is None:
            day = isWeekday(specifiedEnd)
            endDate = None
            dayIter = 0
            while endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if startDate is not None and nextDay.weekday() == day:
                    endDate = nextDay
                    break
                dayIter += 1
        else:
            if month < curMonth:
                endYear += 1
            if month in [1,3,5,7,8,10,12]:
                endDate = date(endYear,month,31)
            elif month == 2:
                try:
                    endDate = date(endYear,month,29)
                except:
                    endDate = date(endYear,month,28)
            else:
                endDate = date(endYear,month,30)


    elif isinstance(specifiedEnd,int) and isinstance(specifiedBeginning,int):
        """"-Quiero algo del dia 28 al dia 7 / quiero algo del mes 4 al 6"""
        endMonth = curMonth
        endYear = curYear
        timeLapse = 0
        if timeUnit == 'day':
            if specifiedEnd < specifiedBeginning:
                timeLapse += (31-specifiedBeginning + specifiedEnd)
            else:
                timeLapse += specifiedEnd - specifiedBeginning +1
            if specifiedBeginning < curDay:
                nextMonth = curMonth+1
                if nextMonth == 13: nextMonth = 1
                startDate = date(curYear,nextMonth ,specifiedBeginning)
            else:
                startDate = date(curYear,curMonth,specifiedBeginning)

        elif timeUnit == 'month':
            if specifiedEnd < specifiedBeginning:
                timeLapse += (12-specifiedBeginning + specifiedEnd)
            else:
                timeLapse += specifiedEnd - specifiedBeginning +1
            timeLapse *= 30.5
            timeLapse = int(timeLapse)
            if specifiedBeginning < curMonth:
                startDate = date(curYear+1,specifiedBeginning ,1)
            else:
                startDate = date(curYear,specifiedBeginning ,1)
        endDate = startDate + timedelta(timeLapse)


    elif specifiedEnd is None and isinstance(specifiedBeginning,int):
        "Quiero algo a partir del mes de febrero. Quiero algo a partir del dia 3. Si son dias, devuelve el rango de 1 mes. Si son meses, 3 meses."
        if timeUnit == 'day':
            if specifiedBeginning < curDay:
                startDate = date(curYear,curMonth+1,specifiedBeginning)
                endDate = date(curYear,curMonth+2,specifiedBeginning)
            else:
                startDate = date(curYear,curMonth,specifiedBeginning)
                endDate = date(curYear,curMonth+1,specifiedBeginning)
        elif timeUnit == 'month':
            if specifiedBeginning < curMonth:
                startDate = date(curYear+1,specifiedBeginning,1)
                try:
                    endDate = date(curYear+1,specifiedBeginning+3,31)
                except:
                    try:
                        endDate = date(curYear+1,specifiedBeginning+3,30)
                    except:
                        try:
                            endDate = date(curYear+1,specifiedBeginning+3,29)
                        except:
                            endDate = date(curYear+1,specifiedBeginning+3,28)

    elif isinstance(specifiedBeginning,(str,unicode)) and specifiedEnd is None:
        """Quiero algo el lunes. Quiero algo en febrero"""
        endYear = curYear
        month = isMonth(specifiedBeginning)
        if month is None:
            day = isWeekday(specifiedBeginning)
            if day is None: raise Exception('Unknown value for End: '+str(specifiedBeginning))
            todayDate = date(curYear,curMonth,curDay)
            for n in range(100):
                nextDay = todayDate + timedelta(n)
                if nextDay.weekday() == day:
                    endDate = nextDay
                    break
            startDate = endDate
        else:
            if month < curMonth:
                endYear += 1
            startDate = date(endYear,month,1)
            if month == 2:
                endDate = date(endYear,month,28)
            elif month in [1,3,5,7,8,10,12]:
                endDate = date(endYear,month,31)
            else:
                endDate = date(endYear,month,30)


    elif isinstance(specifiedEnd,(str,unicode)) and isinstance(specifiedBeginning, int):
        "Quiero algo desde el dia 6 hasta febrero. Quiero algo desde el dia 10 hasta el domingo"
        endYear = curYear
        startDate = date(curYear,curMonth,curDay)
        month = isMonth(specifiedEnd)
        todayDate = date(curYear,curMonth,curDay)
        if timeUnit=='week':specifiedBeginning *= timeUnitInt
        if month is not None:
            startDate = None
            endDate = None
            dayIter = 0
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.day == specifiedBeginning and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.month == month:
                    endDate = nextDay
                    break
                dayIter += 1
        else:
            weekday = isWeekday(specifiedEnd)
            startDate = None
            endDate = None
            dayIter = 0
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.day == specifiedBeginning and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.weekday() == weekday:
                    endDate = nextDay
                    break
                dayIter += 1
    elif isinstance(specifiedBeginning,(str,unicode)) and isinstance(specifiedEnd, int):
        "Quiero algo desde febrero hasta el 15. Quiero algo a partir del lunes y hasta el dia 30."
        endYear = curYear
        startDate = date(curYear,curMonth,curDay)
        month = isMonth(specifiedBeginning)
        todayDate = date(curYear,curMonth,curDay)
        if timeUnit=='week':specifiedEnd *= timeUnitInt
        if month is not None:
            startDate = None
            endDate = None
            dayIter = 0
            endMonth = month
            if timeUnit == 'month':
                endMonth += specifiedEnd
                endMonth %= 12
                print endMonth
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.month == month and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.day == specifiedEnd and nextDay.month == endMonth:
                    endDate = nextDay
                    break
                dayIter += 1
        else:
            weekday = isWeekday(specifiedBeginning)
            startDate = None
            endDate = None
            dayIter = 0
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.weekday() == weekday and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.day == specifiedEnd:
                    endDate = nextDay
                    break
                dayIter += 1

    elif isinstance(specifiedEnd, (str,unicode)) and isinstance(specifiedBeginning,(str,unicode)):
        #Desde el lunes hasta el viernes / desde miercoles hasta lunes
        #Desde febrero hasta marzo
        #Desde lunes hasta Julio
        endYear = curYear
        beginningDay = isWeekday(specifiedBeginning)
        if beginningDay is not None:
            todayDate = date(curYear,curMonth,curDay)
            endDay = isWeekday(specifiedEnd)
            if endDay is not None:
                startDate = None
                endDate = None
                dayIter = 0
                while startDate is None or endDate is None:
                    nextDay = todayDate + timedelta(dayIter)
                    if nextDay.weekday() == beginningDay and startDate is None:
                        startDate = nextDay
                    if startDate is not None and nextDay.weekday() == endDay:
                        endDate = nextDay
                        break
                    dayIter += 1
            else:
                endMonth = isMonth(specifiedEnd)
                startDate = None
                endDate = None
                dayIter = 0
                while startDate is None or endDate is None:
                    nextDay = todayDate + timedelta(dayIter)
                    if nextDay.weekday() == beginningDay and startDate is None:
                        startDate = nextDay
                    if startDate is not None and nextDay.month == endMonth:
                        endDate = nextDay
                    dayIter += 1
        else:
            beginningMonth = isMonth(specifiedBeginning)
            endMonth = isMonth(specifiedEnd)
            todayDate = date(curYear,curMonth,curDay)
            if endMonth is None: endMonth = beginningMonth + 1
            if endMonth >12: endMonth = 1
            startDate = None
            endDate = None
            dayIter = 0
            while startDate is None or endDate is None:
                nextDay = todayDate + timedelta(dayIter)
                if nextDay.month == beginningMonth and startDate is None:
                    startDate = nextDay
                if startDate is not None and nextDay.month == endMonth:
                    endDate = nextDay
                    break
                dayIter += 1
    elif specifiedEnd is None and specifiedBeginning is None:
        startDate = date(curYear,curMonth,curDay)
        endDate = date(curYear+1,curMonth,curDay)
    else:
        warnings.warn('Cuidado: Caso no contemplado en el filtro de fechas' )

    try:
        for singleDate in daterange(startDate, endDate):
                outputTimespan.append(singleDate)
    except:
        warnings.warn('Cuidado: no se ha podido establecer un intervalo, devolviendo la fecha de hoy...' )
        outputTimespan.append(date(curYear,curMonth,curDay))
    outputTimespan = filterDaysAndMonths(outputTimespan,specificDays,specificMonths,specificWeekdays)
    return outputTimespan

def outputToString(outputTimespan):
    """Concatenates in a text the output of the date_to_span function"""
    text=''
    for timespan in outputTimespan:
        text+=str(timespan.day)+'/'+str(timespan.month)+'/'+str(timespan.year)+','
    return text[:-1]

def parseJsonInput(inputJson):
    """Parses a Json and returns the set of possible dates in a concatenated txt"""
    for phrase in inputJson.keys():
        phrase_dict = inputJson[phrase]
        if 'specificWeekdays' in phrase_dict.keys():
            specificWeekdays = phrase_dict['specificWeekdays']
        else:
            specificWeekdays = None
        if 'timeUnit' in phrase_dict.keys():
            timeUnit = phrase_dict['timeUnit']
        else:
            timeUnit = 'day'
        if 'specifiedBeginning' in phrase_dict.keys():
            specifiedBeginning = phrase_dict['specifiedBeginning']
        else:
            specifiedBeginning = None

        if 'specifiedEnd' in phrase_dict.keys():
            specifiedEnd = phrase_dict['specifiedEnd']
        else:
            specifiedEnd = None

        if 'specificDays' in phrase_dict.keys():
            specificDays = phrase_dict['specificDays']
        else:
            specificDays = None

        if 'specificMonths' in phrase_dict.keys():
            specificMonths = phrase_dict['specificMonths']
        else:
            specificMonths = None
        if 'specialDay' in phrase_dict.keys():
            specialDay = phrase_dict['specialDay']
        else:
            specialDay = None

    outputTimespan = date_to_span(timeUnit=timeUnit, specificDays=specificDays, specificWeekdays=specificWeekdays , specificMonths=specificMonths ,
            specifiedBeginning=specifiedBeginning , specifiedEnd=specifiedEnd , specialDay = specialDay)
    textOutput = outputToString(outputTimespan)
    return textOutput

def testFunction(debug=False):
    """Given the possible values that it may take, iterates over the whole set of possibilities. These can be up to 3 Billion items
    so be careful."""
    import itertools, sys
    timeUnitInterval = ['day','month','week']
    specificDaysInterval = [None]
    specificWeekdaysInterval = [None]
    specificMonthsInterval = [None]
    specifiedBeginningInterval = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']+ specificMonthsInterval + range(1,32)+[None]
    specifiedEndInterval = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']+ specificMonthsInterval + range(1,32)+[None]
    combinations = [timeUnitInterval,specificDaysInterval,specificWeekdaysInterval,specificMonthsInterval,specifiedBeginningInterval, specifiedEndInterval]
    totalCount = 0.0
    passCount = 0.0
    for option in itertools.product(*combinations):
        try:
            _ =date_to_span(timeUnit=option[0], specificDays = option[1], specificWeekdays = option[2], specificMonths = option[3], specifiedBeginning = option[4], specifiedEnd = option[5])
            passCount += 1
        except:
            if debug:
                print option
                print sys.exc_info()
        totalCount += 1.0
        if int(totalCount) % 1000 == 0 and totalCount != 0:
            print '{}/{} tests passed - some of then have no sense-, a total of {}%'.format(passCount,totalCount,float(passCount)/float(totalCount))
    print '{}/{} tests passed - some of then have no sense-, a total of {}%'.format(passCount,totalCount,float(passCount)/float(totalCount))




if __name__ == '__main__':
    #testFunction()

    app.run(host='0.0.0.0',port=5063, debug=True)
    #with open('Dates.json','rb') as data_file:
    #    data = json.load(data_file)
#    data = {"el mes que viene": {"specificWeekdays": None, "specifiedEnd": None "specifiedBeginning": None, "timeUnit": "month", "specificDays": None, "specificMonths": None,"specialDay": "siguientemes"}}
