import pandas as pd
import numpy as np
import unicodedata
import re

caminho_csv_retraction = "../watch/retraction_watch.csv"
caminho_saida_csv_com_chave = "../resultados/chave_watch.csv"

df = pd.read_csv(caminho_csv_retraction)
colunas = ["OriginalPaperDOI", "Title", "OriginalPaperDate"]
df_sel = df[colunas].copy()


df_sel["Title"] = df_sel["Title"].fillna("").str.lower()
df_sel["Title"] = df_sel["Title"].apply(
  lambda x: "".join
  (
    c for c in unicodedata.normalize("NFKD", x)
      if not unicodedata.combining(c)
  )
)

df_sel["Title"] = df_sel["Title"].apply(lambda x: re.sub(r"[^a-z0-9\s]", " ", x))
df_sel["Title"] = df_sel["Title"].apply(lambda x: re.sub(r"\s+", " ", x).strip())
df_sel["Title"] = df_sel["Title"].str.replace(" ", "")

df_sel["OriginalPaperDOI"] = df_sel["OriginalPaperDOI"].astype(str)
df_sel["OriginalPaperDOI"] = df_sel["OriginalPaperDOI"].str.replace(
    r".*?(10\.\d{4,9}/\S+)", r"\1", regex=True
)

anos = pd.to_datetime(df_sel["OriginalPaperDate"], errors="coerce").dt.year
df_sel["Ano"] = anos.astype("Int64").astype(str).replace("<NA>", "")

df_sel["Chave"] = df_sel["Title"] + df_sel["Ano"]
df_final = df_sel[["OriginalPaperDOI", "Chave"]]


df_final.to_csv(caminho_saida_csv_com_chave, index=False)
df_final.to_csv(caminho_saida_csv_com_chave, index=False)
