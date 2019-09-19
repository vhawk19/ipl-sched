from django.shortcuts import render
import datetime
import random
import itertools
from scheduler.schedule import IPL
from django.http import JsonResponse
# Create your views here.


def isweekend(currDate):
    if currDate.weekday()>5:
        return True
    else:
        return False

def setDates(schedule,startingDate):
    currDate=startingDate    
    schedule[0]['date']=currDate.strftime('%d/%m/%Y')
    schedule[0]['count']=1
    weekendCount=0
    for i in range(1,len(schedule)):
        if not isweekend(currDate):
            currDate+=datetime.timedelta(days=1)
        else:
            weekendCount+=1
        if weekendCount==2:
            currDate+=datetime.timedelta(days=1)
            weekendCount=0
        schedule[i]['date']=currDate.strftime('%d/%m/%Y')
        schedule[i]['count']=i+1
    return schedule

def setSchedule(startDate):
    teams=['Team A','Team B','Team C','Team D','Team E','Team F','Team G','Team H']
    stadiums=['Chennai','Kochi','Bangalore','Pune','Bombay','Delhi','Jaipur','Kolkata']
    roundRobin=IPL(teams)
    roundRobin.createMatches()
    if roundRobin.finished == True:
        matches=(roundRobin.matches)

    homeMatches=[]
    awayMatches=[]
    for matchPair in matches:
        homeMatch={}
        awayMatch={}
        homeMatch['home-team']=matchPair[0]
        homeMatch['away-team']=matchPair[1]
        homeMatch['match']=matchPair[0]+" vs "+matchPair[1]
        homeMatch['stadium']=stadiums[teams.index(matchPair[0])]
        awayMatch['home-team']=matchPair[1]
        awayMatch['away-team']=matchPair[0]
        awayMatch['match']=matchPair[1]+" vs "+matchPair[0]
        awayMatch['stadium']=stadiums[teams.index(matchPair[1])]
        homeMatches.append(homeMatch)
        awayMatches.append(awayMatch)
    matches=homeMatches+awayMatches
    return setDates(matches,startDate)
def schedule(req,year,month,day):
    startDate=datetime.date(year,month,day)
    print(year,month,day)
    print(startDate)
    return JsonResponse(setSchedule(startDate),safe=False)

