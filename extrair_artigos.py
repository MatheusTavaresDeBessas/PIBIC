import string
import unicodedata
import os
import glob
from lxml import etree
import io
import zipfile
import pandas as pd
import csv
import unicodedata
import re

zip = glob.iglob(
    'E:/curriculos_8818077_2024-11-27/data/repo_2024/*/*.*',
    recursive=True
)
#inicio = input("Digite o inicio da leitura: ")
#fim = input("Digite o fim da leitura: ")
#count = 0
x = 0

artigos_mestres_e_docentes = csv.writer(open('E:/Matheus/resultados/artigos_mestres_e_doutores.csv', 'w'))

header = [ 'Id', 'DOI', 'Chave', 'Titulo_Original']

artigos_mestres_e_docentes.writerow(header)

for curriculo in zip:
 #if int(inicio)-1 <= int(count) < int(fim):
  try:
    arquivo_handle = open(curriculo, 'rb')
    content = arquivo_handle.read()

    if curriculo.split('.')[-1] == 'zip':
      if type(content) == type(str):
        content = content.encode('utf-8')
      zip_memory = io.BytesIO(content)
      zip_data = zipfile.ZipFile(zip_memory)
      xml = b''

      for fn in zip_data.namelist():
        xml += zip_data.read(fn)
      content = xml

    root = etree.XML(content)

    numero_identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')

    periodicos = root.xpath('/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO')

    for artigo in periodicos:
        titulo = artigo.xpath('string(DADOS-BASICOS-DO-ARTIGO/@TITULO-DO-ARTIGO)')
        
        quantidade = len(titulo.split())

        if quantidade > 4:
          titulo_original = titulo
          ano = artigo.xpath('string(DADOS-BASICOS-DO-ARTIGO/@ANO-DO-ARTIGO)')
          doi = artigo.xpath('string(DADOS-BASICOS-DO-ARTIGO/@DOI)')

          titulo = (titulo or "").lower()

          titulo = "".join(
              c for c in unicodedata.normalize("NFKD", titulo)
              if not unicodedata.combining(c)
          )

          titulo = re.sub(r"[^a-z0-9\s]", " ", titulo)
          titulo = re.sub(r"\s+", " ", titulo).strip()
          titulo = titulo.replace(" ", "")

          doi = str(doi)
          doi = re.sub(r".*?(10\.\d{4,9}/\S+)", r"\1", doi)

          chave = titulo + (ano or "")

          linha = [numero_identificador, doi, chave, titulo_original]

          print(linha)

          artigos_mestres_e_docentes.writerow(linha)
        else:
          pass
  except:
   pass
  #count += 1