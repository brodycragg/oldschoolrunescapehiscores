from argparse import ArgumentParser
from lxml import html
import requests

parser = ArgumentParser(description = "Username to be looked up")
parser.add_argument("-u",dest="user", required=True, help = "User to look up")
args = parser.parse_args()
user = args.user

skills = ['Overall','Attack','Defence',
    	  'Strength','Hitpoints','Ranged','Prayer','Magic','Cooking',
	      'Woodcutting','Fletching','Fishing','Firemaking''Crafting',
	      'Smithing','Mining' ,'Herblore','Agility','Thieving','Slayer','Farming',
	      'Runecraft', 'Hunter','Construction']

def lookup(name):
    url = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='
    url += str(name)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    exp = tree.xpath('//body//text()')[0]
    output,result,final = [],[],[]
    [output.append(i) for i in exp.splitlines()]
    for i in range(0, len(output)-1):
        result.append([x.strip() for x in output[i].split(',')])
        final.append(result[i][1])

    levels = dict(zip(skills,final))
    print(levels)

lookup(user)
