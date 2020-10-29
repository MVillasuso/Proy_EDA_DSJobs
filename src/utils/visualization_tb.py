import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px 
import folders_tb as ftb


def graf_bar (col, col2, df, numbars, val_excl, lcolors,lorden,xtit,ytit,tit,rol, emp, fname):
    """
    Crea un gráfico de barras interactivo y lo guarda como html en el directorio /plots segun el nombre indicado en fname
    Selecciona únicamente los registros que representann el top X (siendo X el argumento numbars)
    """
    if emp:
        top_num = df[(df.jobType!="Other")& (df.jobType!="Project Manager")].groupby(col).sum().sort_values("total", ascending = False).total.nlargest(numbars).index.to_list()
    else:
        top_num = df[col].value_counts().head(numbars).index.to_list()

    bar_df = df[(df[col]!=val_excl) & (df[col].isin(top_num)) ].groupby([col,col2]).total.sum().to_frame()
    bar_df.reset_index(inplace=True)
 
    fig=px.bar(bar_df, x=col, y = "total", color = col2, color_discrete_map = lcolors, width=900, height=600)
    
    if lorden:
        xaxisval={'categoryorder':'array', 'categoryarray':lorden} 
    else:
        xaxisval={'categoryorder':'total descending'} 

    fig.update_layout(  
        barmode='stack', xaxis = xaxisval,   
        title = {"text" : tit, "x":0.4, "xanchor":"center"},             
        xaxis_title = xtit,
        yaxis_title = ytit,
        legend=dict(title= rol, y=0.5, font_size=8))

    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()

def graf_pie (df, val, col,tit,lcolor, fname):
    """
    Crea un gráfico de tarta interactivo y lo guarda como html en el directorio /plots segun el nombre indicado en fname
    """
    fig = px.pie(df, values=val, names=col, title=tit, color = col, color_discrete_map = lcolor)
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()

def graf_sbpie (df,lpath,val,col,lcolor,tit, det,fname):
    """
    Crea un gráfico de tarta tipo SunBurnst y lo guarda como html en el directorio /plots segun el nombre indicado en fname
    """
    if det : 
        fig = px.sunburst(df, path=lpath, values=val, color = col, color_discrete_map=lcolor, title=tit)
    else:
        fig = px.sunburst(df, path=lpath, color = col, color_discrete_map=lcolor,title=tit)
    
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()

def graf_snsscat(xval,yval,hueval,df, sizval,colorval, heival,widval, xlab,ylab,titval,fname):
    """
    Crea un gráfico estático de dispersion  y lo guarda como png en el directorio /plots segun el nombre indicado en fname
    """
    plt.subplots(figsize=(heival, widval))
    sns.scatterplot(x=xval, y=yval, hue=hueval, alpha=.6, data=df, size = sizval, sizes = (10,200), palette = colorval, legend = "full")
    plt.ylabel(ylab, fontsize= 15)
    plt.xlabel(xlab, fontsize= 15)
    plt.title (titval)
    ftb.salvar_plot ("../resources/plots/", fname)
    plt.show()

def graf_glscat(df,xval,yval,tval,sval,colorval,titval,widval,heival,fname):
    """"
    Crea un gráfico dinámico de dispersión  y lo guarda como html en el directorio /plots segun el nombre indicado en fname
    """
    fig = go.Figure(data=go.Scattergl(
        x = df[xval],
        y = df[yval],
        text = df[tval],
        mode='markers',
        marker=dict(
            size = df[sval]*2, 
            color=df[sval],
            colorscale='GnBu_r',
            line_width=1,
            showscale=True
        )
    ))
    fig.update_layout(
        title=titval,
        showlegend =False, 
        #legend= dict(title= "Nro-Empleados", y=1.1, font_size=10),
        autosize=False,
        width=widval,
        plot_bgcolor = "darkgrey",
        height=heival)
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()


def graf_hist(df,colval,colorval,titval,xlab, fname, sh=False, binval=0):
    """
    Histograma de la columna indicada. Si el parámetro binval es asignado, cambia los valores de los rangos de agrupación
    Lo guarda como png en el directorio /plots con el nombre de archivo indicado en fname
    """
    if binval:
        sns.distplot(df[colval], color = colorval, bins=binval)
    else:
         sns.distplot(df[colval], color = colorval)
    if sh:
        plt.title(titval, fontsize = 20)
        plt.xlabel(xlab, fontsize = 15)
        ftb.salvar_plot ("../resources/plots/", fname)
        plt.show()

def graf_gobox(df, colval, ycol, diccol, titval, widval, heival,fname):
    """
    Gráfico de caja contrastando por cada valor diferente del argumento colval. Es interactivo. Guarda el resultado como 
    html en el directorio /plots según el nombre indicado en el argumento fname
    """
    x_data =[]
    y_data=[]
    lcolors=[]

    for clave, valor in diccol.items(): 
        x_data.append(clave)
        y_data.append(df[df[colval]==clave][ycol])
        lcolors.append (valor)
    fig = go.Figure()
    for xd, yd, cls in zip(x_data, y_data, lcolors):
            fig.add_trace(go.Box(
                y=yd,
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=2,
                line_width=1)
            )
    fig.update_layout(
        title= titval,
        showlegend =False, 
        autosize=False,
        width=widval,
        height=heival)
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()

def graf_mapam(df,locval,locmodval,colorval, hovval, sval,colorsval,widval, heival,titval, legval,fname):
    """ 
    Crea un mapa mundial interactivo con la oferta laboral en cada país. Puede filtrarse por tipo de oferta 
    Guarda el resultado como html en el directorio /plots según el nombre indicado en el argumento fname
    """ 
    fig = px.scatter_geo(df, locations=locval, locationmode=locmodval ,color=colorval, hover_name=hovval, size=df[sval], projection="natural earth", color_discrete_map = colorsval, width =widval , height = heival, title = titval)
    fig.update_layout(
        showlegend =True, 
        legend= dict(title= legval, y=1.1, font_size=10))
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()

def graf_corr(df,colorval,titval,fname):
    plt.subplots(figsize=(10, 8)) 
    sns.heatmap(df, mask=np.zeros_like(df, dtype=np.bool),  cmap= colorval, square=True,  annot=True)
    plt.title (titval)
    ftb.salvar_plot ( "../resources/plots/", fname)

def graf_proy (df, xval,yval, colval, lcolors,widval,heival, titval, fname):
    fig=px.bar(df, x=xval, y = yval, color = colval, color_discrete_map=lcolors, width=widval, height=heival, title = titval)
    ftb.salvarI_plot(fig,"../resources/plots/", fname)
    fig.show()
