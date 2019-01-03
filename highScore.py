from argparse import ArgumentParser
from lxml import html
import requests
import csv


parser = ArgumentParser(description = "Username to be looked up")
parser.add_argument("-u",dest="user", required=True, help = "User to look up")
parser.add_argument("-s",dest="skill", required=True, help = "Skill to train")
args = parser.parse_args()
user = args.user
skill = args.skill.title()

with open('experienceNeeded.csv','r') as file:
    contents = csv.reader(file)
    experienceTables = [x for x in contents]
experienceTables[0][0] = 1

skills = ['Overall','Attack','Defence',
    	  'Strength','Hitpoints','Ranged','Prayer','Magic','Cooking',
	      'Woodcutting','Fletching','Fishing','Firemaking','Crafting',
	      'Smithing','Mining' ,'Herblore','Agility','Thieving','Slayer','Farming',
	      'Runecraft', 'Hunter','Construction']

def lookup(name):
    url = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='
    url += str(name)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    exp = tree.xpath('//body//text()')[0]
    output,result,experience,final = [],[],[],[]
    [output.append(i) for i in exp.splitlines()]
    for i in range(0, len(output)-1):
        result.append([x.strip() for x in output[i].split(',')])
        final.append(result[i][1])

    levels = dict(zip(skills,final))
    # print(levels)

    for i in range(0,24):
        experience.append(result[i][2])

    experience = dict(zip(skills,experience))
    experienceInLevel = int(experience[skill])

    for i in range(0,len(experienceTables)):
        if experienceInLevel > int(experienceTables[i][1].replace(',','')):
            level = experienceTables[i][0]
            targetLevel = int(level) + 1
            targetExp = experienceTables[i+1][1].replace(',','')
            experienceNeeded = int(targetExp) - int(experienceInLevel)

    print('You are training', skill, 'and need',experienceNeeded, 'exp until you reach level ', targetLevel)
lookup(user)
