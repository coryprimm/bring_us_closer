from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Event, Team
import bcrypt
import random, string, math, re
from itertools import permutations

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, "main/index.html" )

def admin_landing(request):
    c = Event.objects.filter(author_id = request.session["user_id"])
    d = User.objects.get(id = request.session["user_id"])
    context = {
        "this_user" : d,
        "admins_events" : c
    }
    return render(request, "main/admin_landing.html", context )

def participant_landing(request):
    c = Event.objects.filter(users = request.session["user_id"])
    d = User.objects.get(id = request.session["user_id"])
    context = {
        "this_user" : d,
        "users_events" : c
    }
    return render(request, "main/participant_landing.html", context )

def set_type(request, urlpassed_id):
    if request.method == 'POST':
        j = User.objects.get(id = urlpassed_id)
        j.role = request.POST['role']
        j.save()
        return redirect('/participant_landing')


def unformed_event(request, urlpassed_id):
    event = Event.objects.get(eventcode = urlpassed_id)
    attending_users = User.objects.filter(events = event)
    count = len(attending_users)
    difference = int(event.capacity) - count
    f = User.objects.get(id = request.session["user_id"])
    secondcontext = {
        "the_event" : event,
        "the_count" : count,
        "the_difference" : difference,
        "the_user" : f
        }
    return render(request, 'main/unformed_event.html', secondcontext)

def formed_event(request, urlpassed_id):
    event = Event.objects.get(eventcode = urlpassed_id)
    attending_users = User.objects.filter(events = event)
    count = len(attending_users)
    difference = int(event.capacity) - count
    f = User.objects.get(id = request.session["user_id"])
    relevant_teams = Team.objects.filter(eventcode = event.eventcode)
    myusers = []
    for x in range(0, len(relevant_teams)):
        this_team = relevant_teams[x]
        my_users = User.objects.filter(teams = this_team)
        myusers.append(my_users)

    thirdcontext = {
        "the_event" : event,
        "the_count" : count,
        "the_difference" : difference,
        "the_user" : f,
        "team_groupings" : myusers,
        }
    return render(request, 'main/formed_event.html', thirdcontext)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if request.method == 'POST':
        if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
                return redirect("/")
        else:
            hash_pass = bcrypt.hashpw((request.POST['password']).encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(first_name = request.POST['first_name'],
            last_name= request.POST['last_name'], email = request.POST['email'], password = hash_pass.decode('utf-8'))
            request.session['user_id'] = new_user.id
            messages.success(request, "Success!")
            return redirect("/")

def admin_login(request):
    if request.method == 'POST':
        users_matching = User.objects.filter(email = request.POST['email'])
        if len(users_matching) > 0:
            user = users_matching[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/admin_landing')
            else:
                messages.error(request, 'Invalid Credentials')
            
                return redirect('/')
        else:
            messages.error(request, "Didn't match")
            return redirect('/admin_landing')

def participant_login(request):
    if request.method == 'POST':
        users_matching = User.objects.filter(email = request.POST['email'])
        if len(users_matching) > 0:
            user = users_matching[0]
            if bcrypt.checkpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8')):
                request.session['user_id'] = user.id
                return redirect('/participant_landing')
            else:
                messages.error(request, 'Invalid Credentials')
            
                return redirect('/')
        else:
            messages.error(request, "Didn't match")
            return redirect('/participant_landing')

def make_event(request, urlpassed_id):
    if request.method == 'POST':
        randomstring = ''.join(random.choices(string.digits, k=10))
        new_event = Event.objects.create(title = request.POST['title'], author_id = urlpassed_id,  when = request.POST['when'], capacity = request.POST['capacity'], eventcode = randomstring)
        return redirect('/unformed_event/' + randomstring)

def join_event(request, urlpassed_id):
    if request.method == 'POST':
        this_user = User.objects.get(id = urlpassed_id)
        if len(this_user.role) == 0:
            messages.error(request, 'You cannot sign up for an event if you have no role')
            return redirect('/')
        the_event = Event.objects.get(eventcode = request.POST["eventcode"])
        the_event.users.add(this_user)
        the_event.save()
        this_user.save()
        return redirect('/participant_landing')

def finalize_event(request, urlpassed_id):
     if request.method == 'POST':
        team_num_filter = int(request.POST['howmany'])
        if (team_num_filter) <= 0:
            messages.success(request, "It's no fun if you make no teams")
            return redirect('/')
        event = Event.objects.get(eventcode = urlpassed_id)
        if event.formed == True:
            messages.success(request, "Teams have already been made for this event, if you want to make new teams, make a new event")
            return redirect('/')
        attending_users = User.objects.filter(events = event)
        NumberOfParticipants = len(attending_users)
        if team_num_filter > NumberOfParticipants:
                messages.success(request, "You can't have more teams than you have people")
                return redirect('/')
    
        difference = int(event.capacity) - NumberOfParticipants
        number_Of_Teams = int(request.POST['howmany'])
        CountOF_D = CountOF_I  = CountOF_S = CountOF_C = 0 

        for user in attending_users:
            if user.role == "D":
                CountOF_D = CountOF_D + 1
            if user.role == "I":
                CountOF_I = CountOF_I + 1
            if user.role == "S":
                CountOF_S = CountOF_S + 1
            if user.role == "C":
                CountOF_C = CountOF_C + 1
        
        s = ("D" * CountOF_D) +("I" * CountOF_I) + ("S" * CountOF_S) + ("C" * CountOF_C)

        #Step 1: Create a list of all the permutations of input.
        def createPermList(initialList):	
            if len(initialList) <= 7:
                perms_one = [''.join(p) for p in permutations(initialList)] 
            elif len(initialList) < 15:
                perms_one = []
                for f in range(0, 1000):
                    newStr = ''.join(random.sample(s,len(initialList)))
                    if newStr not in perms_one:
                        perms_one.append(newStr)
            else:
                perms_one = []
                for f in range(0,3000):
                    newStr = ''.join(random.sample(s,len(initialList)))
                    if newStr not in perms_one:
                        perms_one.append(newStr)
            return perms_one

        perms = []
        perms = createPermList(s)

        #Step 2: Create a function that given number of teams and number of participants, writes 
        #instructions for how the permutations are to be parsed.
        def create_Instructions( numberOfParticipants, numberOfTeams):
            difference = numberOfParticipants % numberOfTeams
            num_instructions = []
            for c in range(0, numberOfTeams):
                num_instructions.append(math.floor(numberOfParticipants/numberOfTeams))
            if difference > 0:
                for d in range(0, difference):
                    num_instructions[d] = (num_instructions[d]+1)
            return num_instructions

        the_instructions = create_Instructions(NumberOfParticipants, number_Of_Teams)

        #Step 3: Create a function that given a permutation and instructions returns an array that
        #contains the permutation broken into teams the instructions specified.
        def makeTeams(aStr, instructions):
            teams = []
            # teams.append(aStr[0:(instructions[0])])
            first_team = ''.join(sorted(aStr[0:(instructions[0])]))
            teams.append(first_team)
            lastIndex = instructions[0]
            for i in range(1, len(instructions)):
                # teams.append(aStr[lastIndex:instructions[i] + lastIndex])
                team_to_be_made = (aStr[lastIndex:instructions[i] + lastIndex])
                sorted_team_tbm = ''.join(sorted(team_to_be_made))
                teams.append(sorted_team_tbm)
                lastIndex = instructions[i] + lastIndex
            return teams

        #Step 4: Once the permutation has been broken into teams, this function will score how well the teams 
        #are put together. The score it generates will be compared with other scores.
        def scoreThePerm(listOfStrings):
            #First find max inverse
            valueOfD = valueOfI = valueOfS = valueOfC = -1
            if CountOF_D != 0:
                valueOfD = NumberOfParticipants/CountOF_D
            if CountOF_I != 0:
                valueOfI = NumberOfParticipants/CountOF_I
            if CountOF_S != 0:
                valueOfS = NumberOfParticipants/CountOF_S
            if CountOF_C != 0:
                valueOfC = NumberOfParticipants/CountOF_C
            max_value = valueOfD
            thediscvalues = [valueOfI, valueOfS, valueOfC]
            for i in range (len(thediscvalues)):
                if max_value < thediscvalues[i]:
                    max_value = thediscvalues[i]
            
            score = 0
            for k in range (0, len(listOfStrings)):
                for j in range(len(listOfStrings[k])):
                    if listOfStrings[k][j] == "D":
                        score += NumberOfParticipants/CountOF_D
                    if listOfStrings[k][j] == "I":
                        score += NumberOfParticipants/CountOF_I
                    if listOfStrings[k][j] == "S":
                        score += NumberOfParticipants/CountOF_S
                    if listOfStrings[k][j] == "C":
                        score += NumberOfParticipants/CountOF_C
                if "D" not in listOfStrings[k] and CountOF_D != 0:
                    score -= NumberOfParticipants/CountOF_D
                if "I" not in listOfStrings[k] and CountOF_I != 0:
                    score -= NumberOfParticipants/CountOF_I
                if "S" not in listOfStrings[k] and CountOF_S != 0:
                    score -= NumberOfParticipants/CountOF_S
                if "C" not in listOfStrings[k] and CountOF_C != 0:
                    score -= NumberOfParticipants/CountOF_C
                if "D"  in listOfStrings[k] and  "I"  in listOfStrings[k] and "S"  in listOfStrings[k] and  "C" in listOfStrings[k]:
                    score += max_value
            return score

        #Step 5: Now that we have the ability to score the permutations at every index, we must use this tool
        #to find which permutation and grouping of teams is most desirable. 
        def findBestPerm(wholelist, instructions):
            maxscore = scoreThePerm(makeTeams(wholelist[0], instructions))
            scorechart = []
            permchart = []
            bestIndex = 0
            for b in range(0, len(wholelist)):
                permchart.append(makeTeams(wholelist[b], instructions))
                scorechart.append(scoreThePerm(makeTeams(wholelist[b], instructions)))
                if scoreThePerm(makeTeams(wholelist[b], instructions)) > maxscore:
                    maxscore = scoreThePerm(makeTeams(wholelist[b], instructions))
                    bestIndex = b
            return wholelist[bestIndex]

        findBestPerm(perms, the_instructions)

        optimal_teams = makeTeams((findBestPerm(perms, the_instructions)), the_instructions)

        # At this point optimal_teams are a list of strings representing
        # role dispersement. This list needs to be used with the list of participants
        # to form the real teams.
        print(optimal_teams)

        
        def build_teams(listStringFormat, allParticipants):
            dCount = 0
            cCount = 0
            iCount = 0
            sCount = 0
            teams_back = []
            for k in range (0, len(listStringFormat)):
                teams_back.append([])
            dGrouping = []
            iGrouping = []
            sGrouping = []
            cGrouping = []
            for i in range (0, len(allParticipants)):
                if allParticipants[i].role  == "D":
                    dGrouping.append(allParticipants[i])
                if allParticipants[i].role  == "I":
                    iGrouping.append(allParticipants[i])
                if allParticipants[i].role  == "S":
                    sGrouping.append(allParticipants[i])
                if allParticipants[i].role  == "C":
                    cGrouping.append(allParticipants[i])
            for n in range (0, len(listStringFormat)):
                for j in range (0, len(listStringFormat[n])):
                    if len(dGrouping) > 0:
                        if listStringFormat[n][j] == dGrouping[dCount].role:
                            teams_back[n].append(dGrouping[dCount])
                            if dCount == len(dGrouping)-1:
                                continue
                            else:
                                dCount = dCount + 1
                    if len(iGrouping) > 0:
                        if listStringFormat[n][j] == iGrouping[iCount].role:
                            teams_back[n].append(iGrouping[iCount])
                            if iCount == len(iGrouping)-1:
                                continue
                            else:
                                iCount = iCount + 1
                    if len(sGrouping) > 0:
                        if listStringFormat[n][j] == sGrouping[sCount].role:
                            teams_back[n].append(sGrouping[sCount])
                            if sCount == len(sGrouping)-1:
                                continue
                            else:
                                sCount = sCount + 1
                    if len(cGrouping) > 0:
                        if listStringFormat[n][j] == cGrouping[cCount].role:
                            teams_back[n].append(cGrouping[cCount])
                            if cCount == len(cGrouping)-1:
                                continue
                            else:
                                cCount = cCount + 1
            return(teams_back)

        formed_teams = build_teams(optimal_teams, attending_users)

        #Now given the list of teams in user form... I need to put them in 
        #the database
        new_teams = []
        for h in range(0, len(formed_teams)):
            new_teams.append([])
        for b in range(0, len(formed_teams)):
            new_teams[b] = Team.objects.create(eventcode = event.eventcode)
            for c in range(0, len(formed_teams[b])):
                this_user = User.objects.get(id = formed_teams[b][c].id)
                new_teams[b].players.add(this_user)
                new_teams[b].save()
                this_user.save()

        event.formed = True
        event.save()

        return redirect('/formed_event/' + event.eventcode)

#The logout process:
def logout(request):
    del request.session['user_id']
    return redirect('/')

def delete(request, urlpassedevent_id):
    q = Event.objects.get(id = urlpassedevent_id)
    q.delete()
    return redirect('/admin_landing')