from superset import (
    app,
    talisman
)
from flask import (
    render_template,
    request
)
import psycopg2
import plotly.express as px
import plotly.io as io
import pandas as pd
from pandas import read_sql
import plotly.graph_objects as go
from plotly.subplots import make_subplots

USUARIO_BD = "postgres"
SENHA_BD = "postgres"

@talisman(force_https=False)
@app.route("/boletim_covid")
def boletim_covid():
    full_view = request.args.get('full', default=False, type=bool)
    connection = psycopg2.connect('postgresql://' + USUARIO_BD + ':' + SENHA_BD + '@192.168.0.100:5433/target_pb')
    cursor = connection.cursor()
    cursor.execute('select * from boletim_covid')
    result = cursor.fetchone()
    print(pd.DataFrame(list(result)))
    pagina = render_template('facilit/boletim.html', uti_ocupacao_paraiba=str(result[0]) + '%', enfermaria_ocupacao_paraiba=str(result[1]) + '%',uti_ocupacao_grandejp=str(result[2]) + '%',
                                         enfermaria_ocupacao_grandejp=str(result[3]) + '%', uti_ocupacao_campinagrande=str(result[4]) + '%',
                                         enfermaria_ocupacao_campinagrande=str(result[5]) + '%', uti_ocupacao_sertao=str(result[6]) + '%',
                                         enfermaria_ocupacao_sertao=str(result[7]) + '%', casos_confirmados=result[8], casos_descartados=result[9], obitos_confirmados=result[10],
                                         recuperados=result[11], qtd_cidades=result[12], data_atualizacao=result[13], full=full_view)
    cursor.close()
    connection.close()
    return pagina

@talisman(force_https=False)
@app.route("/trend_paraiba_pcn")
def trend_paraiba_pcn():
    connection = psycopg2.connect('postgresql://' + USUARIO_BD + ':' + SENHA_BD + '@192.168.0.100:5433/target_pb')
    cursor = connection.cursor()
    cursor.execute('''select data as data_casos, "casosNovos" as casos_novos, cast(avg("casosNovos") over (order by data rows between 6 preceding and current row) as numeric(12,2)) pcn 
    from "SES_PB" group by data, "casosNovos" order by data''')
    
    result = cursor.fetchall()
    panda_query = pd.DataFrame(list(result))
    
    data = [
        go.Bar(
            x=panda_query[0],
            y=panda_query[1],
            name='Casos por dia',
            hovertemplate='Data: %{x}<br>Casos confirmados: %{y}'           
         ),
        go.Scatter(
            x=panda_query[0],
            y=panda_query[2],
            name='Media móvel'
        )
    ]
    layout = go.Layout(
            xaxis=go.layout.XAxis(tickmode='auto')
       
    )
    fig = go.Figure(data=data,layout=layout)
    pagina = io.to_html(fig)
    cursor.close()
    connection.close()
    return pagina

@app.route("/trend_paraiba_obitos")
def trend_paraiba_obitos():
    connection = psycopg2.connect('postgresql://' + USUARIO_BD + ':' + SENHA_BD + '@192.168.0.100:5433/target_pb')
    cursor = connection.cursor()
    cursor.execute('''select data as data_casos, "obitosNovos" as obitos_novos, cast(avg("obitosNovos") over (order by data rows between 6 preceding and current row) as numeric(12,2)) pcn 
    from "SES_PB" group by data, "obitosNovos" order by data''')
    
    result = cursor.fetchall()
    panda_query = pd.DataFrame(list(result))
    
    data = [
        go.Bar(
            x=panda_query[0],
            y=panda_query[1],
            name='Obitos por dia',
            hovertemplate='Data: %{x}<br>Obitos: %{y}'           
         ),
        go.Scatter(
            x=panda_query[0],
            y=panda_query[2],
            name='Média movel'
        )
    ]
    layout = go.Layout(
            xaxis=go.layout.XAxis(tickmode='auto')
       
    )
    fig = go.Figure(data=data,layout=layout)
    pagina = io.to_html(fig)
    cursor.close()
    connection.close()
    return pagina


@app.route("/casos_por_sintoma_geral")
def casos_por_sintoma_geral():
    connection = psycopg2.connect('postgresql://' + USUARIO_BD + ':' + SENHA_BD + '@192.168.0.100:5433/target_pb')
    cursor = connection.cursor()
    cursor.execute("select to_char(data_inicio_sintomas, 'YYYY-MM-DD'), casos_novos, casos_acumulados from casos_por_sintoma_geral")

    result = cursor.fetchall()
    panda_query = pd.DataFrame(list(result))

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=panda_query[0],
            y=panda_query[2],
            name='Casos acumulados',
            hovertemplate='Data: %{x}<br>Casos acumulados: %{y}' # # informação que aparece ao passar o mouse por cima
        ),
        secondary_y=True
    )

    fig.add_trace(
        go.Bar(
            x=panda_query[0],
            y=panda_query[1],
            name='Casos novos',
            hovertemplate='Data: %{x}<br>Casos novos: %{y}' # informação que aparece ao passar o mouse por cima
        ),
        secondary_y=False
    )
    
    # esse código aqui serve para caso queira adicionar titulo ao gráfico

    # fig.update_layout( 
    #     title_text="Casos confirmados por data de sintoma"
    # )

    fig.update_xaxes(title_text="data de início de sintomas") # titulo do eixo X

    fig.update_yaxes(title_text="<b>Casos novos</b>", range=[0,6000],secondary_y=False)
    fig.update_yaxes(title_text="<b>Casos acumulados</b>",rangemode='tozero', secondary_y=True)
    
    page = io.to_html(fig)
    
    cursor.close()
    connection.close()
    return page

@app.route("/obitos_por_ocorrencia_geral")
def obitos_por_ocorrencia_geral():
    connection = psycopg2.connect('postgresql://' + USUARIO_BD + ':' + SENHA_BD + '@192.168.0.100:5433/target_pb')
    cursor = connection.cursor()
    cursor.execute("select to_char(data_obito, 'YYYY-MM-DD'), obitos_novos, obitos_acumulados from obitos_por_ocorrencia_geral")

    result = cursor.fetchall()
    panda_query = pd.DataFrame(list(result))

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=panda_query[0],
            y=panda_query[2],
            name='Óbitos acumulados',
            hovertemplate='Data: %{x}<br>Óbitos acumulados: %{y}'
        ),
        secondary_y=True,
        col=1,
        row=1
    )

    fig.add_trace(
        go.Bar(
            x=panda_query[0],
            y=panda_query[1],
            name='Óbitos novos',
            hovertemplate='Data: %{x}<br>Óbitos novos: %{y}'
        ),
        secondary_y=False,
        col=1,
        row=1
    )

    # esse código aqui serve para caso queira adicionar titulo ao gráfico
    
    # fig.update_layout(
    #     title_text="Óbitos confirmados por data dos óbitos" #titulo do chart
    # )

    fig.update_xaxes(title_text="data de ocorrência") # titulo do eixo X

    fig.update_yaxes(title_text="<b>Óbitos novos</b>", range=[0,100],secondary_y=False)
    fig.update_yaxes(title_text="<b>Óbitos acumulados</b>", rangemode='tozero', secondary_y=True)
    
    page = io.to_html(fig)
    cursor.close()
    connection.close()
    return page