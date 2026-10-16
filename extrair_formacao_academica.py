import string
import unicodedata
import os
import glob
from lxml import etree
import io
import zipfile
import pandas as pd
import csv
from pathlib import Path

df = pd.read_csv("../resultados/cruzamento.csv", dtype={"Id": str})
coluna = df["Id"].to_list()
coluna = set(df["Id"].astype(str).str.strip())

print(coluna)

arquivos = glob.iglob(
    'E:/curriculos_8818077_2024-11-27/data/repo_2024/*/*.*',
    recursive=True
)
#count = 0
x = 0

path1 = Path('../resultados/cruzamento.csv')

header1 = ['Id', 'Nome', 'Grande-Area', 'Area', 'Graduacao', 'Instituicao', 'Inicio', 'Fim', 'Curso', 'Instituicao', 'Inicio', 'Fim', 'Especializacao', 'Instituicao', 'Inicio', 'Fim', 'Mestrado', 'Instituicao', 'Inicio', 'Fim', 'Doutorado', 'Instituicao', 'Inicio', 'Fim']

produtivos_formacao = csv.writer(open('../resultados/docentes_irregulares.csv', 'w'))
produtivos_formacao.writerow(header1)

#count = 1

# inicio = input("Digite o número inicial: ")
# fim = input("Digite o número final:")

for arquivo in arquivos:
  # if(count >= int(inicio) and count <= int(fim)):
    try:
      #print(count)

      arquivo_handle = open(arquivo, 'rb')
      content = arquivo_handle.read()

      if arquivo.split('.')[-1] == 'zip':
        if type(content) == type(str):
          content = content.encode('utf-8')
        zip_memory = io.BytesIO(content)
        zip_data = zipfile.ZipFile(zip_memory)
        xml = b''

        for fn in zip_data.namelist():
          xml += zip_data.read(fn)
        content = xml

      root = etree.XML(content)
      numero_identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)').strip()
      
      if numero_identificador in coluna:   
            grande_area = area_atuacao = ""

            titulo_curso_g = nome_instituicao_g = ano_inicio_g = ano_conclusao_g = ""
            titulo_curso_c = nome_instituicao_c = ano_inicio_c = ano_conclusao_c = ""
            titulo_curso_e = nome_instituicao_e = ano_inicio_e = ano_conclusao_e = ""
            titulo_curso_m = nome_instituicao_m = ano_inicio_m = ano_conclusao_m = ""
            titulo_curso_d = nome_instituicao_d = ano_inicio_d = ano_conclusao_d = ""

            area = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/AREAS-DE-ATUACAO/AREA-DE-ATUACAO')
            gradu = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/GRADUACAO')
            curso = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/CURSO-TECNICO-PROFISSIONALIZANTE')
            espec = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/ESPECIALIZACAO')
            mestr = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/MESTRADO')
            douto = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO')
            projetos = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL/ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO/PROJETO-DE-PESQUISA')
            endereco = root.xpath('/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL')

            instituicao = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/ENDERECO/ENDERECO-PROFISSIONAL/@NOME-INSTITUICAO-EMPRESA)')
            x = 0

            for dado in area:
                try:
                    if(x == 0):
                        grande_area = dado.xpath('string(@NOME-GRANDE-AREA-DO-CONHECIMENTO)')
                        area_atuacao = dado.xpath('string(@NOME-DA-AREA-DO-CONHECIMENTO)')

                        x = 1
                except:
                    pass

            x = 0

            for dado in gradu:
                try:
                    if(x == 0):
                        titulo_curso_g = dado.xpath('string(@NOME-CURSO)')
                        nome_instituicao_g = dado.xpath('string(@NOME-INSTITUICAO)')
                        ano_inicio_g = dado.xpath('string(@ANO-DE-INICIO)')
                        ano_conclusao_g = dado.xpath('string(@ANO-DE-CONCLUSAO)')

                        x = 1
                except:
                    pass

            x = 0

            for dado in curso:
                try:
                    if(x == 0):
                        titulo_curso_c = dado.xpath('string(@NOME-CURSO)')
                        nome_instituicao_c = dado.xpath('string(@NOME-INSTITUICAO)')
                        ano_inicio_c = dado.xpath('string(@ANO-DE-INICIO)')
                        ano_conclusao_c = dado.xpath('string(@ANO-DE-CONCLUSAO)')

                        x = 1
                except:
                    pass

            x = 0

            for dado in espec:
                try:
                    if(x == 0):
                        titulo_curso_e = dado.xpath('string(@NOME-CURSO)')
                        nome_instituicao_e = dado.xpath('string(@NOME-INSTITUICAO)')
                        ano_inicio_e = dado.xpath('string(@ANO-DE-INICIO)')
                        ano_conclusao_e = dado.xpath('string(@ANO-DE-CONCLUSAO)')

                        x = 1
                except:
                    pass

            x = 0

            for dado in mestr:
                try:
                    if(x == 0):
                        titulo_curso_m = dado.xpath('string(@NOME-CURSO)')
                        nome_instituicao_m = dado.xpath('string(@NOME-INSTITUICAO)')
                        ano_inicio_m = dado.xpath('string(@ANO-DE-INICIO)')
                        ano_conclusao_m = dado.xpath('string(@ANO-DE-CONCLUSAO)')

                        x = 1
                except:
                    pass

            x = 0

            for dado in douto:
                try:
                    if(x == 0):
                        titulo_curso_d = dado.xpath('string(@NOME-CURSO)')
                        nome_instituicao_d = dado.xpath('string(@NOME-INSTITUICAO)')
                        ano_inicio_d = dado.xpath('string(@ANO-DE-INICIO)')
                        ano_conclusao_d = dado.xpath('string(@ANO-DE-CONCLUSAO)')

                        x = 1
                except:
                    pass

            name = root.xpath('string(/CURRICULO-VITAE/DADOS-GERAIS/@NOME-COMPLETO)')

            linha = [numero_identificador, name, grande_area, area_atuacao, titulo_curso_g, nome_instituicao_g, ano_inicio_g, ano_conclusao_g, titulo_curso_c, nome_instituicao_c, ano_inicio_c, ano_conclusao_c, titulo_curso_e, nome_instituicao_e, ano_inicio_e, ano_conclusao_e, titulo_curso_m, nome_instituicao_m, ano_inicio_m, ano_conclusao_m, titulo_curso_d, nome_instituicao_d, ano_inicio_d, ano_conclusao_d]

            produtivos_formacao.writerow(linha)
            print(linha)

            #count += 1
    except:
        #count += 1
        pass
#count = 0