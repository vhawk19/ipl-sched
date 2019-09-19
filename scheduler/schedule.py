from math import ceil
from random import shuffle
import datetime
class IPL:

    def __init__(self, passedTeams=None):
        self.teams=passedTeams
        self.finished=False
        self.error=''
        self.matchdaysCreated=False
        self.rawMatchesCreated=False
        self.freeTicket=True
        self.freeTicketIdentifier='Freeeeeeeeeee'
        self.matchDayCount=0
        self.matchDayPointer=0
        self.matchPointer=0
        self.matches=[]

    def saveMatchday(self):
        matchesTemp=[]
        for i in range(0,len(self.teams1)):
            if(self.freeTicket or (self.teams1[i] != self.freeTicketIdentifier and self.teams2[i]!=self.freeTicketIdentifier)):
                matchesTemp+=[[self.teams1[i],self.teams2[i]]]
        self.matches+=matchesTemp
        return True
    
    def rotate(self):
        temp=self.teams1[1]
        for i in range(1,len(self.teams1)-1):
            self.teams1[i]=self.teams1[i+1]
        self.teams1[len(self.teams1)-1]=self.teams2[-1]
        for i in range(len(self.teams2)-1,0,-1):
            self.teams2[i]=self.teams2[i-1]
        self.teams2[0]=temp
        return True
    
    def validTeamArray(self):
        if not isinstance(self.teams,list) or len(self.teams)<2:
            self.error='not enough number of teams'
            print(self.error)
            self.resetClassState()
            print(self.error)
            return False
        else:
            return True

    def resetClassState(self):
        self.finished=False
        self.rawMatchesCreated=False
        self.matchdaysCreated=False
        self.matches=[]
        self.clearPointer()
        self.matchdayCount=0
        return True
    
    def clearPointer(self):
        self.matchdayPointer=0
        self.matchPointer=0
        return True

    def createMatches(self):
        if self.validTeamArray() == False:
            return False
        self.matches=[]
        teamCount=len(self.teams)
        if teamCount & 1:
            self.teams1=teams[:ceil(teamCount/2)]
            self.teams2=teams[ceil(teamCount/2):]
        else:
            self.teams1=teams[:(teamCount//2)]
            self.teams2=teams[(teamCount//2):]
        team1Count=len(self.teams1)
        team2Count=len(self.teams2)
        if self.matchDayCount==0:
            for i in range(2,team1Count*2):
                self.saveMatchday()
                self.rotate()
            self.saveMatchday()
        else:
            if self.matchDayCount<0:
                self.error='No negative matchDay count allowed'
                self.resetClass()
                return True
            shuffle(self.teams1)
            shuffle(self.teams2)
            if(len(self.teams)>=self.matchDayCount):
                for i in range(0,self.matchDayCount):
                    self.saveMatchday()
                    self.rotate()
                self.saveMatchday()
            else:
                for i in range(2,len(self.teams1)*2):
                    self.saveMatchday()
                    self.rotate()
                self.saveMatchday()
                diff=self.matchdayCount - len(self.teams)
                for i in range(0,diff):
                    self.matches+=[]
        self.finished=True
        self.rawMatchesCreated=False
        self.matchdayCreated=True
        self.clearPointer()

        return self.matches

def isweekend(currDate):
    if currDate.weekday()>4:
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
    homeMatch['matchPair']=matchPair
    homeMatch['stadium']=stadiums[teams.index(matchPair[0])]
    awayMatch['home-team']=matchPair[1]
    awayMatch['away-team']=matchPair[0]
    awayMatch['match']=matchPair[1]+" vs "+matchPair[0]
    awayMatch['matchPair']=matchPair
    awayMatch['stadium']=stadiums[teams.index(matchPair[1])]
    homeMatches.append(homeMatch)
    awayMatches.append(awayMatch)
matches=homeMatches+awayMatches
matches=setDates(matches,startDate)