import pandas as pd
import tkinter as tk
import csv
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def selectItem(tree):
    curItem = tree.focus()
    item = tree.item(curItem)
    if not item['values']:
        return "None"
    else:
        return item['values']

def get_cuadrillas(csv):
    c = pd.read_csv(csv)
    # print(c.head())
    c_list = []
    for x in c.values:
        temp = []
        for item in x:
            temp.append(item)
        c_list.append(temp)
    return c_list, c

def get_resources(csv):
    r = pd.read_csv(csv)
    # print(r.head())
    r_list = []
    for x in r.values:
        temp = []
        for item in x:
            temp.append(item)
        r_list.append(temp)
    return r_list

def update_list(tree,csv):
    tree.delete(*tree.get_children())
    c_list, c = get_cuadrillas(csv)
    for n, row in enumerate(c_list):
        if row[5] == "Sí":
            tree.insert(parent="", index=n, iid=n, text="", values=row, tags='available')
        else:
            tree.insert(parent="", index=n, iid=n, text="", values=row, tags='unavailable')
    tree.tag_configure('available', background='#8BE28C')
    tree.tag_configure('unavailable', background='#E28D8B')

def center_win(root,w,h):
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    return root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def add_cuadrilla_row(file, input, top):
    name = input.get()
    with open(file, "r", encoding="UTF-8") as f:
        reader = csv.reader(f)
        names = []
        count = 0
        for row in reader:
            names.append(row[1])
            count += 1
        if name in names:
            messagebox.showerror("Error: Nombre duplicado","Ya existe una cuadrilla con ese nombre. Elige uno diferente.")
            print("Ya existe una cuadrilla con ese nombre. Elige otro nombre.")
            top.lift()
            top.focus()
        elif name == None:
            messagebox.showerror("Error: Falta nombre","No has introducido ningún nombre. Escribe uno.")
            print("No has introducido ningún nombre. Escribe uno.")
            top.lift()
            top.focus()
        else:
            line = [count, name, 0, 1, 0, 'Sí','Ninguna']
            f = open(file, "a+", newline='', encoding="UTF-8")
            writer = csv.writer(f)
            writer.writerow(line)
            f.close()
            top.destroy()
            top.update()

def create_cuadrilla(csv,root,tree):
    win = Toplevel(root)
    win.title("CUADRILLA")
    win.config(width=200, height=150)

    center_win(win,200,150)

    def exit_btn(top):
        top.destroy()
        top.update()

    tag_name = ttk.Label(win, text="Nombre de la cuadrilla")
    tag_name.place(x=10, y=20)


    input_name = tk.Entry(win)
    input_name.place(x=10, y=50)
    input_name.focus()

    win.bind('<Return>', lambda event: [add_cuadrilla_row(csv,input_name,win),update_list(tree,csv)])

    b_ok = ttk.Button(win, text="Aceptar", command= lambda: [add_cuadrilla_row(csv,input_name,win),update_list(tree,csv)])
    b_ok.place(x=10, y=100)

    b_cancel = ttk.Button(win, text="Cancelar", command= lambda: exit_btn(win))
    b_cancel.place(x=100, y=100)

    win.focus()
    win.mainloop()

def delete_cuadrilla(tree,file):
    cuadrilla = selectItem(tree)
    if cuadrilla == "None":
        messagebox.showerror("Error: Cuadrilla no seleccionada", "No has seleccionado ninguna cuadrilla. Elige una para eliminarla.")
    else:
        c_name = cuadrilla[1]
        lines = []
        with open(file, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            counter = 1
            for row in reader:
                if c_name != row[1]:
                    if row[0].isnumeric() == True:
                       row[0] = str(counter)
                       lines.append(row)
                       counter +=1
                    else:
                        lines.append(row)
                else:
                    pass
            f.close()
        with open(file, "w", encoding="UTF-8", newline='') as f:
            counter = 0
            writer = csv.writer(f)
            writer.writerows(lines)
            f.close()

def assign_task(tree,root,file,file_2):
    cuadrilla = selectItem(tree)
    if cuadrilla == "None":
        messagebox.showerror("Error: Cuadrilla no seleccionada", "No has seleccionado ninguna cuadrilla. Elige una para asignarle una tarea.")
    else:
        if cuadrilla[6] == "Ninguna":
            win = Toplevel(root)
            win.title("TAREAS")
            win.config(width=200, height=200)

            center_win(win, 200, 250)

            tag_name = ttk.Label(win, text="Tareas disponibles")
            tag_name.place(x=50, y=20)

            def add_task(top,task,item,file_2):
                cuadrilla = item[1]
                lines = []
                with open(file_2, "r", encoding="UTF-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        lines.append(row)
                    f.close()
                for line in lines:
                    if line[1] == cuadrilla:
                        line[5] = 'No'
                        line[6] = task
                    else:
                        pass
                with open(file_2,"w",encoding="UTF-8",newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(lines)
                    f.close()
                    top.destroy()
                    top.update()

            list = get_resources(file)
            y= 50
            for item in list:
                name = item[0]
                b_list = ttk.Button(win, text=name, command=lambda x=name: [add_task(win,x,cuadrilla,file_2), update_list(tree, file_2)])
                b_list.place(x=50, y=y)
                y+= 30

            win.update()


        else:
            messagebox.showerror("Error: Cuadrilla ocupada", "La cuadrilla que has seleccionado ya tiene una tarea asignada.")

def clear_task(tree,file):
    cuadrilla = selectItem(tree)
    if cuadrilla == "None":
        messagebox.showerror("Error: Cuadrilla no seleccionada", "No has seleccionado ninguna cuadrilla. Elige una para quitarle la tarea.")
    elif cuadrilla[5] == "Sí":
        messagebox.showerror("Error: Cuadrilla sin tarea", "La cuadrilla que has seleccionado no tiene ninguna tarea asignada todavía.")
    else:
        c_name = cuadrilla[1]
        lines = []
        with open(file, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                lines.append(row)
            f.close()
        for line in lines:
            if line[1] == c_name:
                line[5] = 'Sí'
                line[6] = 'Ninguna'
            else:
                pass
        with open(file, "w", encoding="UTF-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lines)
            f.close()

"""
LÓGICA
"""

def iniciar_semana(file, file_2):
    lines = []
    with open(file, "r", encoding="UTF-8") as f:
        reader = csv.reader(f)
        for row in reader:
            lines.append(row)
        f.close()
    for line in lines:
        if line[0].isnumeric() == True:
            progress = line[2]
            level = line[3]
            exhaust = line[4]
            task = line[6]

    # with open(file, "w", encoding="UTF-8", newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(lines)
    #     f.close()

def recolection(progress, level, exhaust, task):
    carga_max = 4  # Carga máxima por cuadrilla

