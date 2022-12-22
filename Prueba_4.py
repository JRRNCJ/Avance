import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

#Título
st.title('DISEÑO DE NÚMERO DE CONECTORES DE CORTES')

#Propiedades del conector de corte
st.header("Expresión AISC")
st.latex(r'''Q_{n} = 0.5 A_{st} \sqrt{f'_{c} E_{c}}''')
st.header("Propiedades de conector")

A1=np.array([['C: Diámetro de vástago (pulg)','1/2','5/8','5/8','3/4','3/4','3/4'],
    ['L: Longitud del Vastago (pulg)','2 1/2','2 1/2','3','4','3','4'],
    ['D: Diámetro de Cabeza (pulg)','1','1 1/4','1 1/4','1 1/4','1 1/4','1 1/4'],
    ['H: Altura de Cabeza (mm)','8.5','8.5','8.5','8.5','10','10']])
C1=['Tipo de Conector','NS-500/250','NS-625/250','NS-625/300','NS-625/400','NS-750/300','NS-750/400']
df1 = pd.DataFrame(A1, columns=C1)

#Ploteo de propiedades del conector
col1, col2 = st.columns([5,1])

with col1:
    st.table(df1)

with col2:
    img= Image.open("PernoDimensiones.png")
    st.image(img,width=150,caption="Dimensiones de Perno")

conector=st.selectbox("Seleccione un tipo de conector",['NS-500/250','NS-625/250',
    'NS-625/300','NS-625/400','NS-750/300','NS-750/400'])
for i in range(1,7):
    if conector==C1[i]:
        st.write('Diámetro de Vástago (C):',A1[0,i])
        st.write('Longitud del Vastago (L):',A1[1,i])
        st.write('Diámetro de Cabeza (D):',A1[2,i])
        st.write('Altura de Cabeza (mm):',A1[3,i])
        if A1[0,i]=='1/2':
            Dia=0.5
        elif A1[0,i]=='5/8':
            Dia=5/8
        elif A1[0,i]=='3/4':
            Dia=0.75

st.header("Resistencia del conector: Qn(t)")
fc=st.selectbox("Seleccione un resistencia a compresión del concreto: f'c(kg/cm2)",
    [210,245,280,315,350])
Qn=round(0.5*(Dia*2.54)**2/4*3.1416*((fc*0.0981)*0.043*2400**1.5*(fc*0.0981)**0.5)**0.5/98.1,2)
st.metric('Qn(t):',Qn)


#Propiedades de viga de apoyo
st.header("Propiedades de Viga de Apoyo")

col3, col4 = st.columns([1,3])

with col3:
    d=st.number_input("Peralte de viga (cm):",min_value=0.,key=1)
    bf=st.number_input("Ancho de viga (cm):",min_value=0.,key=2)
    tw=st.number_input("Espesor de alma (cm):",min_value=0.,key=3)
    tf=st.number_input("Espesor de ala (cm):",min_value=0.,key=4)
    fy=st.selectbox("Seleccione el esfuerzo de fluencia del acero: fy(kg/cm2)",
    [3500,4200])

#Gráfica de sección de viga
verts=[(-tw/2,-d/2+tf),(-tw/2,d/2-tf),(-bf/2,d/2-tf),(-bf/2,d/2),(bf/2,d/2),(bf/2,d/2-tf),(tw/2,d/2-tf),
    (tw/2,-d/2+tf),(bf/2,-d/2+tf),(bf/2,-d/2),(-bf/2,-d/2),(-bf/2,-d/2+tf),(-tw/2,-d/2+tf)]
codes=[Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,
    Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
path = Path(verts, codes)

fig1, ax1 = plt.subplots()
patch = patches.PathPatch(path, facecolor='black')
ax1.add_patch(patch)
ax1.set_xlim(min([-d/2,-bf/2]),max([d/2,bf/2]))
ax1.set_ylim(min([-d/2,-bf/2]),max([d/2,bf/2]))

with col4:
    st.pyplot(fig1)

#Ancho Efectivo
L=st.number_input("Longitud de viga (m):",min_value=0.,key=5)
S=st.number_input("Espaciamiento entre vigas (m):",min_value=0.,key=6)
befec=min([L/4,S])
st.metric('Ancho efectivo de losa que colabora con la viga de apoyo (m):',befec)

#Cortante Longitudinal
st.header("Cortante Longitudinal")
Ay=bf*tf*2+tw*(d-2*tf)
st.write("As: Área de sección de viga (cm2):",Ay)
tc=st.number_input("Espesor de losa de concreto encima de la cresta(cm):",min_value=0,key=7)
Ac=befec*100*tc
st.write("Ac: Área de concreto en el ancho efectivo (cm2):",Ac)
Nc=math.ceil(min([0.85*fc*Ac,fy*Ay])/1000/Qn)
st.write("N: Número de conectores:",Nc)
Nf=st.number_input("Número de líneas de conectores:",min_value=1,key=8)
Ncpf=math.ceil(Nc/Nf)
st.write("  Conectores por línea:",Ncpf)
st.write("Espaciamiento de conectores (cm):", math.floor(L/2*100/(Ncpf)/5)*5)

