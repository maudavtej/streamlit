import streamlit as st

st.title("SIMULACIÓN DEPREDADOR-PRESA")
st.write("Prueba del front end")

slider= st.slider("Selecciona un valor", 1,2,3,4,5)
st.write("Valor seleccionado", slider)

st.subheader("PRUEBA")