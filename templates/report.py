import streamlit as st 
from PIL import Image

matrix = Image.open("Confussionmatrix.png")
graph = Image.open("yolo11 graph.png")
st.image(matrix,width=300,caption='Confusion Matrix of Yolo11 model')
st.image(graph,width=300,caption= 'Graph of Yolo11 model')