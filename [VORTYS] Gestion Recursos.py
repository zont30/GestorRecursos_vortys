import pandas as pd
import tkinter as tk
import csv
from tkinter import ttk
from Vortys_functions import *

"""
CSVs
"""
cuadrillas_csv = r"files\cuadrillas.csv"
recursos_csv = r"files\recursos.csv"
elaboraciones_csv = r"files\elaboraciones.csv"

semana = 0

# ['Cuadrilla', 'Nombre', 'PrAscenso', 'Nivel', 'Cansancio', 'Ocupada']

c_list, c = get_cuadrillas(cuadrillas_csv)
r_list = get_resources(recursos_csv)
e_list = get_resources(elaboraciones_csv)

# Total de cuadrillas
total_c = len(c)
# Cuadrillas ocupadas
ocup_c = 0
for ocup in c["Disponible"]:
    if ocup == "No":
        ocup_c += 1


carga_max = 4 # Carga máxima por cuadrilla
carga_carretillo = 10 # Carga máxima con carretillo
carga_carreta = 20 # Carga máxima con carreta

toolBooster = 0.5 # Aumenta un 50% la producción si se usan herramientas
distanceP = 1 # Penalización de recursos por cada casilla de distancia
distanceP_carreta = 0.5 # Penalización de recursos por cada casilla de distancia con carretas


"""DIALOGOS TOTAL CUADRILLAS"""
# if total_c == 0:
#     print("El asentamiento no tiene ninguna cuadrilla.")
# elif total_c == 1:
#     if ocup_c == 0:
#         print("Tu asentamiento cuenta con una cuadrilla y está disponible:")
#         print(c.iloc[1,]["Nombre"])
#     else:
#         print("Tu asentamiento cuenta con una cuadrilla, pero no está disponible.")
# else:
#     if ocup_c == 0:
#         print(f"Hay un total de {total_c} cuadrillas y todas están disponibles:")
#         for e in enumerate(c["Nombre"]):
#             print("-",e[1])
#     elif ocup_c >= 1 < total_c:
#         rem_c = total_c - ocup_c
#         print(f"Hay un total de {total_c} cuadrillas, pero disponible {rem_c}:")
#         for e in enumerate(c["Nombre"]):
#             if c["Disponible"][e[0]] == "Sí":
#                 print("-",e[1])
#     else:
#         print("Hay un total de {total_c} cuadrillas, pero ninguna está disponible.")

"""INTERFAZ"""
ventana = tk.Tk()
ventana.title("GESTIÓN DEL ASENTAMIENTO")
ventana.config(width=1000, height=500)

center_win(ventana,900,500)

etiqueta_temp_cuadrillas = ttk.Label(text="CUADRILLAS")
etiqueta_temp_cuadrillas.place(x=20, y=15)

etiqueta_acciones = ttk.Label(text="========== ACCIONES ==========")
etiqueta_acciones.place(x=20, y=250)

etiqueta_temp_materiales = ttk.Label(text="MATERIALES")
etiqueta_temp_materiales.place(x=600, y=15)

etiqueta_temp_elab = ttk.Label(text="ELABORACIONES")
etiqueta_temp_elab.place(x=600, y=250)

tv = ttk.Treeview(ventana, heigh=8)
tv['columns']= ('Cuadrilla', 'Nombre', 'Progreso', 'Nivel', 'DiasTrabajo', 'Disponible', 'Tarea', 'Herramientas')
tv.column('#0', width=0, stretch="NO")
tv.column('Cuadrilla',anchor="center", width=25)
tv.column('Nombre',anchor="center", width=70)
tv.column('Progreso',anchor="center", width=55)
tv.column('Nivel',anchor="center", width=40)
tv.column('DiasTrabajo',anchor="center", width=70)
tv.column('Disponible',anchor="center", width=65)
tv.column('Tarea',anchor="center", width=100)
tv.column('Herramientas',anchor="center", width=80)

tv.heading('Cuadrilla', text='Nº', anchor="center")
tv.heading('Nombre', text='Nombre', anchor="center")
tv.heading('Progreso', text='Progreso', anchor="center")
tv.heading('Nivel', text='Nivel', anchor="center")
tv.heading('DiasTrabajo', text='Días trabajo', anchor="center")
tv.heading('Disponible', text='Disponible', anchor="center")
tv.heading('Tarea', text='Tarea', anchor="center")
tv.heading('Herramientas', text='Herramientas', anchor="center")

for n,row in enumerate(c_list):
    if row[5] == "Sí":
        tv.insert(parent="",index=n, iid=n, text="", values=row, tags='available')
    else:
        tv.insert(parent="", index=n, iid=n, text="", values=row, tags='unavailable')
tv.tag_configure('available', background='#8BE28C')
tv.tag_configure('unavailable', background='#E28D8B')

tv.place(x=20, y=50)

tv_2 = ttk.Treeview(ventana,heigh=8)
tv_2['columns']= ('Material', 'Stacks')
tv_2.column('#0', width=0, stretch="NO")
tv_2.column('Material',anchor="w", width=200)
tv_2.column('Stacks',anchor="w", width=70)

tv_2.heading('Material', text='Material', anchor="center")
tv_2.heading('Stacks', text='Stacks', anchor="center")

for n,row in enumerate(r_list):
    tv_2.insert(parent="",index=n, iid=n, text="", values=row)

tv_2.place(x= 600, y= 50)

tv_3 = ttk.Treeview(ventana,heigh=8)
tv_3['columns']= ('Elaboración', 'Stacks')
tv_3.column('#0', width=0, stretch="NO")
tv_3.column('Elaboración',anchor="w", width=200)
tv_3.column('Stacks',anchor="w", width=70)

tv_3.heading('Elaboración', text='Elaboración', anchor="center")
tv_3.heading('Stacks', text='Stacks', anchor="center")

for n,row in enumerate(e_list):
    tv_3.insert(parent="",index=n, iid=n, text="", values=row)

tv_3.place(x= 600, y= 280)

"""
DATOS
"""
data = [ventana, tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv]

b_create_cuadrilla = ttk.Button(ventana, text="Crear cuadrilla", command=lambda: create_cuadrilla(ventana, tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv))
b_create_cuadrilla.place(x=25, y=280)

b_delete_cuadrilla = ttk.Button(ventana, text="Eliminar cuadrilla", command=lambda: [delete_cuadrilla(tv,cuadrillas_csv),update_list(tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv)])
b_delete_cuadrilla.place(x=130, y=280)

b_assign_task = ttk.Button(ventana, text="Asignar tarea", command=lambda: assign_task(ventana, tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv))
b_assign_task.place(x=25, y=320)

b_clear_task = ttk.Button(ventana, text="Quitar tarea", command=lambda: [clear_task(tv,cuadrillas_csv),update_list(tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv)])
b_clear_task.place(x=130, y=320)

b_clear_task = ttk.Button(ventana, text="BORRAR", command=lambda: [clear_materials(recursos_csv),update_list(tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv)])
b_clear_task.place(x=750, y=10)

# b_elaborate = ttk.Button(ventana, text="Realizar elaboración")
# b_elaborate.place(x=25, y=360)

# etiqueta_addHappy = ttk.Label(ventana, text="Añadir felicidad")
# etiqueta_addHappy.place(x=160, y=300)
# input_addHappy = tk.Entry(ventana)
# input_addHappy.place(x=260, y=300, width=20)
#
# etiqueta_addUnhappy = ttk.Label(ventana, text="Restar felicidad")
# etiqueta_addUnhappy.place(x=160, y=320)
# input_addUnhappy = tk.Entry(ventana)
# input_addUnhappy.place(x=260, y=320, width=20)

b_start_week = ttk.Button(ventana, text="INICIAR SEMANA", command=lambda: [iniciar_semana(cuadrillas_csv,recursos_csv), update_list(tv, tv_2, tv_3, cuadrillas_csv, recursos_csv, elaboraciones_csv)])
b_start_week.place(x=25, y=420)


ventana.mainloop()
