import pandas as pd

retraction_data = pd.read_csv("../resultados/chave_watch.csv", encoding="latin-1")
artigos_mestres_e_doutores = pd.read_csv(
    "../resultados/artigos_mestres_e_doutores.csv", 
    encoding="latin-1", 
    dtype={"Id": str}  
)

retraction_doi = retraction_data[retraction_data["OriginalPaperDOI"].notna() & (retraction_data["OriginalPaperDOI"].astype(str).str.strip() != "")].copy()
artigos_doi = artigos_mestres_e_doutores[artigos_mestres_e_doutores["DOI"].notna() & (artigos_mestres_e_doutores["DOI"].astype(str).str.strip() != "")].copy()

testar_doi = pd.merge(
    retraction_doi,
    artigos_doi,
    left_on="OriginalPaperDOI",
    right_on="DOI",
    how="inner"
)

testar_chave = pd.merge(
    retraction_data,
    artigos_mestres_e_doutores,
    on="Chave",
    how="inner"
)

resultado = pd.concat([testar_doi, testar_chave], ignore_index=True)

if "OriginalPaperDOI" in resultado.columns:
    resultado["DOI"] = resultado["DOI"].fillna(resultado["OriginalPaperDOI"])

resultado = resultado.drop_duplicates(subset=["Id", "Chave"])

resultado[["Id", "DOI", "Chave", "Titulo_Original"]].to_csv("../resultados/cruzamento.csv", index=False)