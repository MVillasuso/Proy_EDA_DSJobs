import pandas as pd
import numpy as np

 
def elim_cols(df):

    """ 
    Retorna un DF con un subconjunto de las columnas del DF de entrada (seleccionado únicamente las columnas con información relevante
    o con  datos )) y las renombra para más facilidad en su uso 
    """

    newdf=df.loc[:,['gaTrackerData.empSize', 'header.easyApply','header.employerName', 'header.jobTitle',
       'header.posted', 'header.salaryHigh', 'header.salaryLow','job.description', 'job.jobSource', 'map.country',
        'map.lat', 'map.lng', 'map.location','overview.foundedYear', 'overview.industry',
       'overview.revenue', 'overview.sector', 'overview.size','overview.type']]

    newdf = newdf.rename(columns={'gaTrackerData.empSize':'empSize','header.easyApply':'easyApply', 
    'header.employerName':'empName', 'header.jobTitle': 'jobTitle', 'header.posted': 'jobDate', 
    'header.salaryHigh':'salHigh','header.salaryLow':'salLow', 'job.description': 'jobDesc', 
    'job.jobSource':'jobSource', 'map.country':'country','map.lat': 'lat', 'map.lng': 'long', 'map.location': 'location', 
    'overview.foundedYear': 'foundedYear','overview.industry':'industry', 'overview.revenue': "revenue",
    'overview.sector':'sector', 'overview.size': 'size', 'overview.type':'type'})

    newdf.drop_duplicates (inplace = True)      #Elimina las filas duplicadas (misma oferta que procede de diferentes fuentes)

    return newdf

def transf_cols(df):
    """
    Cambia el tipo de dato a fecha y actualiza ciertas columnas a formato title para su facil manipulacion y visualización
    """
    df["jobDate"] = pd.to_datetime(df["jobDate"])
    lista_cols= ['empName','jobTitle','location', 'industry', 'sector', 'type']
    for elem in lista_cols:
        df[elem]=df[elem].str.title()
    return df

def norm_country(df, names_df):
    """"
    Estandarización de los datos relacionados al país
    """
    # Estandarizar como país United Kingdom cuando en la location se indique que la ciudad pertenece a England 
    # (había diferentes valores en la columna country  (United Kingdom, UK, GBR, England, GB, gb) 
    list_Eng = df[(df["location"].str.contains(", England", na=False))].index.to_list()
    df["country"][df.index.isin (list_Eng)] = "GB"

    # Estandarizar valores pertenecientes a United States
    df["country"][df.country.isin (["US", "United States", "USA"])] = "US"
    df["country"][((df["location"].str.contains(",", na=False))) & (df["country"].isnull())] = "US"

    # Asignar el valor de location a la columna country cuando esta sea nula
    df["country"][df.country.isnull()] = df["location"]

    # Actualizaciom para estandarizar registros de India
    df["country"][df.country.isin (["India", "IN"])] = "IN"

    # Estandarizacion de códigos de países y nombres con info del df de códigos
    df=pd.merge(df, names_df, left_on='country', right_on='Name', how = "left")
    df=pd.merge(df, names_df, left_on='country', right_on='Code', how = "left")
    df['Code_x'] = np.where(df['Code_x'].isnull(), df['Code_y'], df['Code_x'])
    df['Name_x'] = np.where(df['Name_x'].isnull(), df['Name_y'], df['Name_x'])
    df.drop(columns=["Name_y", "Code_y"], inplace = True)
    df.rename(columns={"Name_x":"cname", "Code_x":"ccode"}, inplace=True)

    return df

def ubicar_loc (df):
    """
    Función para asignar pais a localizaciones (45000 aprox)sin este valor que existan en otros registros con valor único 
    en el dataframe
    """
    #Eliminar las filas que contienen location null
    df.drop(df[df.location.isnull()].index, inplace=True)

    #Buscar las location que cumplan esta condicion (5788 en total)
    regs_df= df.loc[:,[ "location", "cname","ccode"]]
    regs_df.drop_duplicates(inplace=True)
    regs_df.dropna(inplace=True)
    a = (regs_df.location.value_counts()>1).to_frame()
    a.drop(a[(a.location == False)].index, inplace=True)
    regs_df.drop(regs_df[regs_df.location.isin (a.index)].index, inplace=True)

    # Merge para asignar valor al pais cuando la localizacion ya exista con valor unico
    df=pd.merge(df, regs_df, on='location', how="left")

    df['ccode_x'] = np.where(df['ccode_x'].isnull(), df['ccode_y'], df['ccode_x'])
    df['cname_x'] = np.where(df['cname_x'].isnull(), df['cname_y'], df['cname_x'])
    df.drop(columns=["cname_y", "ccode_y"], inplace = True)
    df.rename(columns={"cname_x":"cname", "ccode_x":"ccode"}, inplace=True)
    #Elimina los registros de los cuales no pudo determinar la localizacion (6.000 aprox)
    df.drop(df[df.ccode.isnull()].index, inplace=True)

    return df

def experience (df):
    """
    Determina la experiencia segun algunos valores indicados en JobTitle
    """
    df["exp"]= np.where(df.jobTitle.str.contains('Senior|Sr.|Director'), "Senior","N/A")
    df["exp"]= np.where((df.jobTitle.str.contains('Junior|Jr.')), "Junior", df.exp)
    df["exp"]= np.where((df.jobTitle.str.contains('Internship|Apprentice|Summer|Intern,')), "Internship", df.exp)
    return df

def level(df):
    """
    Determina el nivel de responsabilidad segun algunos valores indicados en JobTitle
    """
    df["level"]= np.where((df.jobTitle.str.contains('Assistant')), "Assistant", "N/A")
    df["level"]= np.where((df.jobTitle.str.contains('Analyst')), "Analyst", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Management|Mgmt|Controller|Lead|Coord|Project')), "PMO", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Technical|Engineer|Ingénieur')), "Technical", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Dba|Admin|Database')), "Dba", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Scientist|Stat|Math')), "Scientist", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Research')), "Research", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Developer|Programmer')), "Developer", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Product')), "Product", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Consult')), "Consultant", df.level)
    df["level"]= np.where(df.jobTitle.str.contains('Manager'), "Manager",df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Director')), "Director",df.level)
    return df

def jobType (df):
    """
    Calcula el tipo de perfil demandado relacionado con Data Science  segun lo especificado en JobTitle
    Crea una columna "sal" para el salario medio de la banda salarial del cargo (la media entre Low y High)
    """
    df["jobType"]= np.where(df.jobTitle.str.contains('Learning|Ai |Deep|Ml |Artific'), "ML_AI","Other")
    df["jobType"]= np.where((df.jobTitle.str.contains('Data') & df.jobTitle.str.contains('Analyst|Analist') ), "Data Analyst", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Business|Intelligence|Bi ') & df.jobTitle.str.contains('Analyst') ), "Business Analyst", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Data Scien')), "Data Scientist", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Data Engineer|Big Data')), "Data Engineer", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Project Manager')), "Project Manager", df.jobType)
    df["sal"] = np.where(df.salLow > 0, (df['salLow']+ df['salHigh'])/2,0)
    return df


def llenar_na(df):
    """
    Actualización del dataframe con valores útiles para el análisis y gráficos
    """
    # Llenar con el valor "N/A" (Not Available) los casos en que el valor este vacio --> nulo
    df["sector"].fillna("N/A", inplace=True)
    df["industry"].fillna("N/A", inplace=True)
    df["empSize"].fillna("N/A", inplace=True)
    df["empSize"]= np.where((df.empSize=='-1-0'), "N/A", df.empSize)
    df["size"].fillna("N/A", inplace=True)
    df["type"].fillna("N/A", inplace=True)
    df["revenue"].fillna("Unknown / Non-Applicable", inplace=True)
    # Eliminación de filas con nombre de empresa null (mas o menos 3500) o JobDesc null (4 registros). 
    # Se eliminan pues no aportan informacion
    df.drop(df[df["empName"].isnull()].index, axis = 0, inplace=True)
    df.drop(df[df["jobDesc"].isnull()].index, axis = 0, inplace=True)
    #Asignar orden al tamano de la empresa segun la cantidad de empleados en empSize
    df["size"]= np.where((df.empSize=="1-50"), 1, df["size"])
    df["size"]= np.where((df.empSize=="51-200"), 2, df["size"])
    df["size"]= np.where((df.empSize=="201-500"), 3, df["size"])
    df["size"]= np.where((df.empSize=="501-1000"), 4, df["size"])
    df["size"]= np.where((df.empSize=="1001-5000"), 5, df["size"])
    df["size"]= np.where((df.empSize=="5001-10000"), 6, df["size"])
    df["size"]= np.where((df.empSize=="10000--1"), 7, df["size"])
    df["size"]= np.where((df.empSize=="N/A"), 8, df["size"])
    df["size"] = pd.to_numeric(df["size"], downcast='integer')
    return df

def resumen_df (df):
    """"
    Dataframe resumen con la información agregada y sumarizada para facilitar el análisis
    """
    res_df = df.groupby(["size", "empSize", "sector", "industry", "type","ccode", "cname", "exp", "level","jobType"]).agg({'jobTitle':['size'],'salLow':['min','max','mean'], 'salHigh':['min','max','mean'],'sal':['mean']})
    res_df.reset_index(inplace=True)
    res_df.columns = ['size','empSize','sector','industry','type','ccode','cname','exp','level','jobType','total','salLow_min','salLow_max', 'salLow_mean','salHigh_min', 'salHigh_max', 'salHigh_mean','sal_mean']
  
    return res_df

def res_emp_df (df):
    """"
    Dataframe resumen con la información agregada por EMPRESA y sumarizada para el análisis
    """
    emp_df = df.groupby(["size", "empSize", "empName", "sector", "industry", "type","jobType"]).agg({'jobTitle':['size'],'sal':['mean']})
    emp_df.reset_index(inplace=True)
    emp_df.columns = ['size','empSize', 'empName','sector','industry','type','jobType','total','sal_mean']
    return emp_df