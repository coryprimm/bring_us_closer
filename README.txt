#Bring Us Closer

Ever been at a group competition and felt the teams were sub optimized? 
Bring Us Closer was built for this specific problem. 

After participants have joined the event, the organizer can choose how many teams she wants to create. In one click the app will optimize teams using various algorithms.

But what is interesting about this to me, is not only the code, but the problem.

Would you, as a group organizer, prefer even teams? Or to get the most out of the overall performance of the group. I tried to solve the later.
I used a weighted system/ grading scale, that fluctuates based off the quantity of the given role in proportion to the total number of participants. If you take the inverse of this number, you can weight the value of every role.

Given this structure, some roles become more valuable than others. I also gave additional value to any team that had all the roles (attempting to solve the group maximization and not evening)

The code accommodates uneven numbered teams, say if there are 20 people and you want 3 teams. It will make a teams of 7, 7 and 6.

Currently, the problem is best solved through combinations. I have the algorithm generate 3000 combinations of individuals. From that sample, the best result is chosen. I am working on a mathematical equation than would generate the optimum score of a team based off it’s inputs so I could ensure the results.

## Features
open-sourced team organization app written in
⋅ MySQL
⋅ Django 2.2.4
⋅ Python 3.6.4

## Building
It is best to use the python virtualenv tool to build locally:
$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
Then visit http://localhost:8000 to view the app.


