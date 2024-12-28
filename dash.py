import yfinance as yf
import pandas as pd
from datetime import datetime

x = 1

data_referencia = datetime.now() - pd.DateOffset(years=x) # Pegando a data de x anos atrás
data_referencia = data_referencia.strftime('%Y-%m-%d') # Convertendo a data de pandas para string

codigo_acoes = [
    'PETR4.SA',
    'VALE3.SA',
    'ITUB4.SA',
    'BBAS3.SA'
]

def obter_cotacoes(data_referencia, codigos_acoes):
    lista_dfs = []

    for cdgo in codigos_acoes:
        df = yf.download(cdgo, start=data_referencia).reset_index()
        df['CD_ACAO'] = cdgo
        if 'Adj Close' in df.columns: 
            df = df[['Date', 'CD_ACAO', 'Adj Close']] 
        else: 
            df = df[['Date', 'CD_ACAO', 'Close']]
        lista_dfs.append(df)

    df = pd.concat(lista_dfs, ignore_index=True)

    return df

def obter_indicadores_fundamentalistas(codigos_acoes):
    lista_indicadores = [] # Lista que armazena os dados de cada ação

    for cdgo in codigos_acoes:
        acao = yf.Ticker(cdgo)
        info = acao.info

        indicadores = {
            'CD_ACOES': cdgo,
            'Setor': info.get('sector'),
            'Indústria': info.get('industry'),
            'Beta': info.get('beta'),
            'Valor de Mercado': info.get('marketCap'),
            'P/L': info.get('trailingPE'),
            'P/VP': info.get('priceToBook'),
            'Dividend Yield (%)': info.get('dividendYield') * 100 if info.get('dividendYield') else None,
            'Margem Bruta (%)': info.get('grossMargins') * 100 if info.get('grossMargins') else None,
            'Margem Operacional': info.get('operatingMargins') * 100 if info.get('operatingMargins') else None,
            'Magem Líquida (%)': info.get('netMargins') * 100 if info.get('netMargins') else None,
            'ROE (%)': info.get('returnOnEquity') * 100 if info.get('returnOnEquity') else None,
            'ROA (%)': info.get('returnOnAssets') * 100 if info.get('returnOnAssets') else None,
            'Dívida/Patrimônio': info.get('debtToEquity'),
            'Crescimento Receira (%)': info.get('revenueGrowth') * 100 if info.get('revenueGrowth') else None
        }

        lista_indicadores.append(indicadores)
    
    df_indicadores = pd.DataFrame(lista_indicadores)

    return df_indicadores
"""
print(obter_cotacoes(data_referencia, codigo_acoes))
print(obter_indicadores_fundamentalistas(codigo_acoes))
"""
df_cotacoes = obter_cotacoes(data_referencia, codigo_acoes) 
df_cotacoes.columns = df_cotacoes.columns.get_level_values(0) 
df_cotacoes.to_excel('cotacoes.xlsx', index=False) 

df_indicadores = obter_indicadores_fundamentalistas(codigo_acoes) 
df_indicadores.columns = df_indicadores.columns.get_level_values(0) 
df_indicadores.to_excel('indicadores.xlsx', index=False)
