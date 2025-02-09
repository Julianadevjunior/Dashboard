import streamlit as st
import pandas as pd
import defs
import datetime

if 'página' not in st.session_state:
    st.session_state['página'] = 'Home'

if 'entradas' not in st.session_state:
    st.session_state['entradas'] = 'tabela_entrada'

with st.sidebar:
    button_home = st.button('🏡 Home', use_container_width=True)
    button_in = st.button('📥 Entradas', use_container_width=True)
    button_out = st.button('📤 Saídas', use_container_width=True)

if button_home:
    st.session_state['página'] = 'Home'
if button_in:
    st.session_state['página'] = 'Entrada'
if button_out:
    st.session_state['página'] = 'Saída'

if st.session_state['página'] == 'Home':
    defs.home()
if st.session_state['página'] == 'Entrada':
    defs.entradas()
if st.session_state['página'] == 'Saída':
    defs.saidas()
