from bs4 import BeautifulSoup
from csv import writer
import re


class Internship:
    def __init__(self, id, name, link, season, freshman, mode):
        self.id = id
        self.name = name
        self.link = link
        self.season = season
        self.freshman = freshman
        self.mode = mode

    def __repr__(self):
        return '{}    {}    {}    {}    {}    {}'.format(self.id, self.name, self.link, self.season, self.freshman, self.mode)

    def toList(self):
        return [self.id, self.name, self.link, self.season, str(self.freshman), self.mode]

class Internships:
    def __init__(self):
        self.internships = []
    
    def add(self, internship):
        self.internships.append(internship)

    def showLinks(self):
        for internship in self.internships:
            print(internship.link)

    def toCSV(self):
        with open('nasa_internships.csv', 'w') as f:
            writer_object = writer(f)
            writer_object.writerow(['ID', 'Name', 'Link', 'Type', 'For Freshman', 'Mode'])
            for internship in self.internships:
                writer_object.writerow(internship.toList())
            f.close()
    
    def num(self):
        print(len(self.internships))
        

keywords = ['computer programming', 'computer science']
freshmanOnly = True
summerOnly = True



HTMLFile = open("text.html", "r", encoding="utf8")
index = HTMLFile.read()
S = BeautifulSoup(index, 'lxml')
  
internships = Internships()

for tag in S.recursiveChildGenerator():
    if tag.name and tag.name == 'tr':
        text = tag.text
        keyword_found = False
        for keyword in keywords:
            if keyword.lower() in text.lower():
                keyword_found = True
        if not keyword_found:
            continue
        freshman = True if 'freshman' in text.lower() else False
        if freshmanOnly and not freshman:
            continue
        season = re.search('>Intern: (.*) 20', str(tag)).group(1)
        if summerOnly and season != 'Summer':
            continue
        id = text[0:6]
        name = re.search('(.*)Intern: ', text[6:len(text)]).group(1)
        link = 'https://stemgateway.nasa.gov' + re.search('href="(.*)" rel', str(tag)).group(1)
        modes = []
        if 'virtual' in text.lower():
            modes.append('Virtual')
        if 'in-person' in text.lower():
            modes.append('In-person')
        mode = '/'.join(modes)
        internships.add(Internship(id, name, link, season, freshman, mode))

internships.toCSV()
internships.num()