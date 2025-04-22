import random
# name files yoinked from https://github.com/dominictarr/random-name
# this is pretty much just a scratch program and doesn't do much unless you know how to use the data it generates

first_names = []
with open("first-names.txt") as fn:
    first_names = fn.readlines()

first_names = [fn.strip() for fn in first_names]

last_names = []
with open("names.txt") as ln:
    last_names = ln.readlines()

last_names = [ln.strip() for ln in last_names]

email_domains = ["fmail.com","coldmail.net","inlook.org","positron.me","example.com"]
positions = ["Center","Left Wing","Right Wing","Left Defense","Right Defense","Goalie"]

person = []
for i in range(0,100):
    id = i
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    gyear = 2030
    dob = f"{random.randrange(2007,2011)}-{random.randrange(0,13)}-{random.randrange(0,29)}"
    email = f"{fn}.{ln}@{random.choice(email_domains)}"
    phone = str(random.randrange(1000000000,9999999999))
    position = random.choice(positions)
    rank = i
    tuple = (id,fn,ln,gyear,dob,email,phone,position,rank)
    person.append(tuple)

samplesville = person[0:20]
fakesland = person[20:40]
exampletown = person[40:60]
anyplace = person[60:80]
madeupburb = person[80:100]

teamplayers = [samplesville,fakesland,exampletown,anyplace,madeupburb]

teams = [
    (1,"Samplesville Saints","Joe","Sampleton","joe.sampleton@samplesville.org","samplesville.org"),
    (2,"Fakesland Foxes","George","Fakerton","fakertongeorge@fakesland.org","fakesland.org"),
    (3,"Exampletown Eagles","Samantha","Examplesmith","examplesmiths@exampletown.org","exampletown.org"),
    (4,"Anyplace Armadillos","Martin","Anyman","manyman@anyplace.org","anyplace.org"),
    (5,"Madeupburb Muskrats","Alice","Madeupperson","alicem@madeupburb.org","madeupburb.org")
]

teammembership = []
for t in range(0,5):
    for p in range(0,20):
        id = t*20 + p
        teammembership.append((id,p,teamplayers[t][p][0],t))

for p in map(str,person):
    print(p+",")

for p in map(str,teammembership):
    print(p+",")

