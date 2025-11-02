import streamlit as st

st.title("SIMULACIÓN DEPREDADOR-PRESA")
st.write("Prueba del front end")

slider= st.slider("Selecciona un valor", 1,2,3)
st.write("Valor seleccionado", slider)

