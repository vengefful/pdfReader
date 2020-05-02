# !usr/bin/python3

import PyPDF2
import re
import requests
import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help="Path to torrent file")
args = parser.parse_args()

#Variables
#  name = args.path


def SaveDOasJSON(filename):
    base = 'DO/'
    pdfFile = open(base+filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    count = 0
    num_pages = pdfReader.numPages
    data = []
    text = []
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        text.append(pageObj.extractText())
        count +=1
    data = {'title': filename, 'texto': text}
    return data



def searchTerm(filename, name):
    #  name = "JIMMY SARMENTO RIBEIRO"
    match = None
    with open(filename, 'r') as f:
        data = json.load(f)

    for do in data:
        for i in range(len(do['texto'])):
            match = re.search(name, do['texto'][i])
            if(match):
                print(f"{name} - {do['title']} - page: {i}")

def RetrieveLinks():
    data = []
    url = "http://www.imprensaoficialal.com.br/diario-oficial/"
    r = requests.get(url)
    regex = r"http.*doe-.*2020/(?=\">DOE)"
    for match in re.finditer(regex, r.text):
        data.append(match[0])
    return data

def RetrievesPdfsLinks(data):
    lista = []
    regex = r"http.*COMPLETO.pdf"
    regexTitle = r"DOEAL.*COMPLETO.pdf"
    for d in data:
        r = requests.get(d)
        match = re.search(regex, r.text)
        title = re.search(regexTitle, r.text)
        tmp = {'title': title[0], 'url': match[0]}
        lista.append(tmp)
    return lista 

def DownloadPdfs(data):
    for d in data:
        r = requests.get(d['url'])
        with open(f"DO/{d['title']}", 'wb') as f:
            f.write(r.content)
        print(f"downloaded: {d['title']}")


if __name__ == "__main__":
    filename = 'DO_2020.json'
    name = args.name
    searchTerm(filename, name)








#  if __name__ == "__main__":
    #  data = []
    #  listFilenames = os.listdir('DO/')
    #  for filename in listFilenames:
        #  tmpData = SaveDOasJSON(filename)
        #  data.append(tmpData)  
        #  print(filename)
    
    #  with open('DO_2020.json', 'w') as f:
        #  json.dump(data, f, indent=2)








#  if __name__ == "__main__":
    #  data = RetrieveLinks()
    #  lista = RetrievesPdfsLinks(data)
    #  DownloadPdfs(lista)
    #  print("DONE")
