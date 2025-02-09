import streamlit as st
import pandas as pd
import datetime

def valorf(n):
    n = f'{float(n):,.2f}'
    if ',' in n:
        n = n.replace(',', '-')

    if '.' in n:
        n = n.replace('.', ',')

    if '-' in n:
        n = n.replace('-', '.')
    return n

def home():
    st.markdown('<div style="text-align:center; font-size:30px"><b>Lucros</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align:center; font-size:30px"><b>💸</b></div>', unsafe_allow_html = True)
    df_lucro = pd.read_excel('.venv/tabela_de_entrada.xlsx')
    df_gastos = pd.read_excel('.venv/tabela_de_saida.xlsx')
    tab_lucro = {}
    tab_gastos = {}
    tab_lucro_liquido = {}

    for i in range(0, len(df_lucro)):
        data = df_lucro['data'].loc[i][3:5]
        valor = float(df_lucro['valor'].loc[i])
        if data in tab_lucro:
            tab_lucro[data] += valor
        else:
            tab_lucro[data] = valor

    for i in range(0, len(df_gastos)):
        data = df_gastos['data'].loc[i][3:5]
        valor = float(df_gastos['valor'].loc[i])
        if data in tab_gastos:
            tab_gastos[data] += valor
        else:
            tab_gastos[data] = valor

    for mes in range(0, 12):
        calc = 0
        if f'0{mes}' in tab_lucro.keys() and f'0{mes}' in tab_gastos.keys():
            calc = tab_lucro[f'0{mes}'] - tab_gastos[f'0{mes}']

        elif f'0{mes}' in tab_lucro.keys() and f'0{mes}' not in tab_gastos.keys():
            calc = tab_lucro[f'0{mes}']

        elif f'0{mes}' not in tab_lucro.keys() and f'0{mes}' in tab_gastos.keys():
            calc = tab_gastos[f'0{mes}']

        else:
            calc = 0

        if calc != 0:
            tab_lucro_liquido[f'0{mes}'] = calc
    meses_grafico(tab_lucro_liquido)

    lucro_bruto = 0
    gastos = 0
    lucro = 0

def entradas():
    bd = pd.read_excel('tabela_de_entrada.xlsx')
    st.markdown('<div> <p><b>Entradas</b></p> </div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        in_table = st.button('Acessar tabela', use_container_width=True)
        if in_table:
            st.session_state['entradas'] = 'tabela_entrada'
    with col2:
        in_dados = st.button('Inserir entradas', use_container_width=True)
        if in_dados:
            st.session_state['entradas'] = 'tabela_dados'

    if st.session_state['entradas'] == 'tabela_entrada':
        st.dataframe(bd,  use_container_width=True)
        grafico('.venv/tabela_de_entrada.xlsx')

    if st.session_state['entradas'] == 'tabela_dados':
        form_entrada()

def saidas():
    bd = pd.read_excel('.venv/tabela_de_saida.xlsx')
    st.markdown('<div> <p><b>Saídas</b></p> </div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        in_table = st.button('Acessar tabela', use_container_width=True)
        if in_table:
            st.session_state['entradas'] = 'tabela_entrada'
    with col2:
        in_dados = st.button('Inserir saídas', use_container_width=True)
        if in_dados:
            st.session_state['entradas'] = 'tabela_dados'

    if st.session_state['entradas'] == 'tabela_entrada':
        st.dataframe(bd,  use_container_width=True)
        grafico('.venv/tabela_de_saida.xlsx')

    if st.session_state['entradas'] == 'tabela_dados':
        form_saida()

def form_entrada():
    form = st.form(key='form_entrada', clear_on_submit=True, enter_to_submit=True, border=True)
    with form:
        st.markdown('<div style="text-align:center; font-size:30px"><b>Dados de recebimento</b></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-size:30px"><b>😁</b></div>',
                    unsafe_allow_html=True)

        col4, col5 = st.columns([1, 1])
        if st.session_state['entradas'] == 'tabela_dados':
            with col4:
                txt = st.markdown('<b>Insira a data do Recebimento</b>', unsafe_allow_html=True)
                data = st.date_input(label=f'Insira a data do pagamento',
                                     format="DD/MM/YYYY",
                                     label_visibility='collapsed')
            with col5:
                txt = st.markdown('<b>Tipo de pagamento</b>', unsafe_allow_html=True)
                tipo = st.selectbox(label='Tipo', options=['Comissão'], label_visibility='collapsed')

            col6, col7 = st.columns([1, 1])
            with col6:
                txt = st.markdown('<b>Insira o valor</b>', unsafe_allow_html=True)
                valor = st.number_input(label='Valor', label_visibility='collapsed')

            with col7:
                txt = st.markdown('<b>Responsável</b>', unsafe_allow_html=True)
                responsavel = st.selectbox(label='Tipo', options=['Karina', 'Natasha', 'Nicolly', 'Pamela'],
                                           label_visibility='collapsed')

            if st.form_submit_button(label='Inserir', use_container_width=True):
                st.success('Cadastrado com sucesso')
                bd = pd.read_excel('.venv/tabela_de_entrada.xlsx')
                bd.loc[len(bd)] = [data.strftime('%d/%m/%Y'), tipo, float(valor), responsavel]
                bd.to_excel('.venv/tabela_de_entrada.xlsx', index=False)

def grafico(bd):
    dados_grafico = {}
    grafico_meses = {}
    df = pd.read_excel(bd)
    df_simples = df[['data', 'valor']]
    meses = ['01/jan', '02/fev', '03/mar', '04/abr',
             '05/mai', '06/jun', '07/jul', '08/ago',
             '09/set', '10/out', '11/nov', '12/dez']
    ctrl = 0
    for indice in range(0, len(df_simples)):
        mes = df_simples['data'].loc[indice][3:5]
        valor = df_simples['valor'].loc[indice]

        if mes in dados_grafico:
            dados_grafico[mes].append(valor)
        else:
            dados_grafico[mes] = [valor]

    # saber qual foi o último mês que houve registro
    if list(dados_grafico.keys())[-1][0] == '0':
        ctrl = int(list(dados_grafico.keys())[-1][1])
    else:
        ctrl = int(list(dados_grafico.keys())[-1])

    for item in dados_grafico:
        dados_grafico[item] = sum(dados_grafico[item])

    for chave in range(0, ctrl):
        chave += 1
        if len(f'{chave}') == 1:
            indice = f'0{chave}'
        else:
            indice = chave

    tot_meses = []
    for chave in dados_grafico.keys():
        if len(f'{chave}') == 2:
            tot_meses.append(str(chave)[1])
        else:
            tot_meses.append(str(chave))


    for mes in range(0, ctrl):
        mes = mes+1
        if str(mes) not in tot_meses:
            if len(str(mes)) == 1:
                dados_grafico[f'0{str(mes)}'] = 0

    st.bar_chart(dados_grafico, x_label='Meses')

def form_saida():
    form = st.form(key='form_entrada', clear_on_submit=True, enter_to_submit=True, border=True)
    with form:
        st.markdown('<div style="text-align:center; font-size:30px"><b>Dados de pagamento</b></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-size:30px"><b>😏</b></div>',
                    unsafe_allow_html=True)

        col4, col5 = st.columns([1, 1])
        if st.session_state['entradas'] == 'tabela_dados':
            with col4:
                txt = st.markdown('<b>Insira a data do Recebimento</b>', unsafe_allow_html=True)
                data = st.date_input(label=f'Insira a data do pagamento',
                                     format="DD/MM/YYYY",
                                     label_visibility='collapsed')
            with col5:
                txt = st.markdown('<b>Tipo de pagamento</b>', unsafe_allow_html=True)
                tipo = st.selectbox(label='Tipo', options=['Meta',
                                                           'Chaves na mão',
                                                           'Imóvel web',
                                                           'Canal Pro',
                                                           'Jetimob',
                                                           'C2S',
                                                           'Secretária',
                                                           'Escritório',
                                                           'Tabela',
                                                           'Comissão',
                                                           'Captação'], label_visibility='collapsed')

            col6, col7 = st.columns([1, 1])
            with col6:
                txt = st.markdown('<b>Insira o valor</b>', unsafe_allow_html=True)
                valor = st.number_input(label='Valor', label_visibility='collapsed')

            with col7:
                txt = st.markdown('<b>Recebedor</b>', unsafe_allow_html=True)
                recebedor = st.selectbox(label='Tipo', options=['Meta',
                                                                'Chaves na mão',
                                                                'Imóvel web',
                                                                'Canal Pro',
                                                                'Jetimob',
                                                                'C2S',
                                                                'Secretária',
                                                                'Escritório',
                                                                'Tabela',
                                                                'Comissão',
                                                                'Captação',
                                                                'Karina',
                                                                'Natasha',
                                                                'Nicolly',
                                                                'Pamela'], label_visibility='collapsed')

            if st.form_submit_button(label='Inserir', use_container_width=True):
                st.success('Cadastrado com sucesso')
                bd = pd.read_excel('.venv/tabela_de_saida.xlsx')
                bd.loc[len(bd)] = [data.strftime('%d/%m/%Y'), tipo, valor, recebedor]
                bd.to_excel('.venv/tabela_de_saida.xlsx', index=False)

def meses_grafico(dic):
    ctrl = 0
    meses_dic = []
    # Quatidade de meses que eu tenho
    for meses_str in dic.items():
        chave, valor = meses_str
        if int(chave) > ctrl:
            ctrl = int(chave)

    # quais meses tem no dic
    for keys in dic:
        meses_dic.append(int(keys))

    # Qual mes que não tem do dic
    for meses in range(0, ctrl):
        meses = meses+1
        if meses not in meses_dic:
            dic[f'0{meses}'] = 0

    st.bar_chart(dic, x_label='Meses')