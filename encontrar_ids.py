import io
import zipfile
import glob
import csv
import pandas as pd
from lxml import etree
from pathlib import Path

df = pd.read_csv("../resultados/cruzamento.csv", dtype={"Id": str})
coluna = set(df["Id"].astype(str).str.strip())

output_path = '../resultados/ids_docentes_irregulares.csv'
header1 = ['Id']

with open(output_path, 'w', newline='', encoding='utf-8') as f_out:
    produtivos_formacao = csv.writer(f_out)
    produtivos_formacao.writerow(header1)

    arquivos = glob.iglob('E:/curriculos_8818077_2024-11-27/data/repo_2024/*/*.*', recursive=True)

    for arquivo in arquivos:
        try:
            with open(arquivo, 'rb') as arquivo_handle:
                content = arquivo_handle.read()

            if arquivo.lower().endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(content)) as zip_data:
                    xml_content = b''
                    for fn in zip_data.namelist():
                        xml_content += zip_data.read(fn)
                    content = xml_content

            root = etree.XML(content)
            numero_identificador = root.xpath('string(/CURRICULO-VITAE/@NUMERO-IDENTIFICADOR)')
            
            if numero_identificador:
                id_limpo = numero_identificador.strip()
                
                if id_limpo in coluna:
                    produtivos_formacao.writerow([id_limpo])

        except Exception as e:
            continue