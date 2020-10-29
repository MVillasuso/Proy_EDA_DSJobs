import os, sys
import pandas as pd 
import json 
import miningdata_tb as mtb



# ----------------------
# $$$$$$$ LIMPIEZA Y ESTANDARIZACIÓN DE DATOS DE GLASSDOOR Data Science jobs $$$$$$$$
# ----------------------

def preparar_df (jobfile, cfile):
    """ Limpia, estandariza y prepara los datos para el análisis del data set de entrada (glassdoor.csv).
    Argumentos:
        jobs_df: path del data set con la información a depurar
        countries: path del data set con la lista de países
    Retorna:
        Un archivo en formato json con el dataframe resultante del proceso de Data wrangling and cleaning 
    """

    GlassD_df= pd.read_csv(jobfile, sep=",")
    cnames_df = pd.read_csv(cfile, sep =",")
    GDjobs_df = mtb.elim_cols(GlassD_df)
    GDjobs_df = mtb.transf_cols(GDjobs_df)
    GDjobs_df = mtb.norm_country(GDjobs_df, cnames_df)
    GDjobs_df = mtb.ubicar_loc(GDjobs_df)
    GDjobs_df = mtb.experience (GDjobs_df)
    GDjobs_df = mtb.level (GDjobs_df)
    GDjobs_df = mtb.jobType(GDjobs_df)
    GDjobs_df = mtb.llenar_na(GDjobs_df)
    json_DSjobs = GDjobs_df.to_json()

    return json_DSjobs


