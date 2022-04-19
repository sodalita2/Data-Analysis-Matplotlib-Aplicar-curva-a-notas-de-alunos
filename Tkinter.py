import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import Tkinter
from tkinter import *
from tkinter import filedialog, messagebox, ttk


class Program:
    def __init__(self,Tk):
        self.df = pd.read_excel(r'students.xlsx', sheet_name='Marks', engine="openpyxl")
        self.df_nativo = pd.read_excel(r'students.xlsx', sheet_name='Marks', engine="openpyxl")
        self.bin = [0, 60, 70, 80, 90, 100]
        self.label = ['F', 'D', 'C', 'B', 'A']
        self.Canvas = Canvas(Tk,bg='black',height=400,width=1000)
        self.Disciplinas = ["History","Geography","Maths","Biology","Physics","Chemistry","Literature"]
        self.Tipos = ["Raiz Quadrada","Escala Linear","Nota mais alta 100"]
        self.value_tipo = tkinter.StringVar(Tk)
        self.value_tipo.set("Escolha tipo de ajuste")
        self.value_inside = tkinter.StringVar(Tk)
        self.value_inside.set("Escolha uma Disciplina")
        self.DisciplinaMenu = Tkinter.OptionMenu(Tk, self.value_inside,*self.Disciplinas)
        self.DisciplinaMenu.pack()
        self.TipoMenu = Tkinter.OptionMenu(Tk, self.value_tipo,*self.Tipos)
        self.TipoMenu.pack()
        self.SubmitButton = tkinter.Button(Tk, text="Atualizar",command=self.printar_tabela_atualizada)
        self.SubmitButton.pack()
        self.ResetButton = tkinter.Button(Tk, text="Resetar",command=self.resetar)
        self.ResetButton.pack()
        self.ConceitoButton = tkinter.Button(Tk, text="Trocar por Conceito",command=self.trocar_nota_por_conceito)
        self.ConceitoButton.pack()
        self.SaveButton = tkinter.Button(Tk, text="Salvar GPA em excel",command=self.save_to_excel)
        self.SaveButton.pack()
        self.Frame = tkinter.LabelFrame(Tk,text="Data")
        self.Frame.pack(fill="both",expand="true")
        self.tv1 = ttk.Treeview(self.Frame)
        self.tv1.place(relheight=1,relwidth=1)
        self.printar_nativo()
        self.tv1.pack()
        self.Canvas.pack()



    ## Printa a tabela primeira vez com os dados originais
    ## e reprinta a original na funcao de resetar
    def printar_nativo(self):
        self.GPA = False
        for i in self.tv1.get_children():
            self.tv1.delete(i)
        for i in self.tv1.selection():
            self.tv1.delete(i)

        DataFrame = self.df_nativo

        self.tv1["column"] = list(DataFrame.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1["columns"]:
            self.tv1.heading(column,text=column)

        df_rows = DataFrame.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert("","end",values=row)


    ## Printa tabela com valores ajustados e chama a funcao gerar grafo atualizado
    ## para gerar dois grafos, original e com valores ajustados
    def printar_tabela_atualizada(self):
        for i in self.tv1.get_children():
            self.tv1.delete(i)
        for i in self.tv1.selection():
            self.tv1.delete(i)

        tabela_modificada = self.gerar_grafo_ajustado(self.value_inside.get(),self.value_tipo.get(),self.df)
        self.tv1["column"] = list(tabela_modificada.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column)

        df_rows = tabela_modificada.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert("", "end", values=row)


    ## Reseta a tabela com valores e o canvas com os dois grafos
    def resetar(self):
        self.GPA = False
        self.df = self.df_nativo
        self.value_inside.set("Escolha uma Disciplina")
        self.value_tipo.set("Escolha tipo de ajuste")
        for i in self.tv1.get_children():
            self.tv1.delete(i)
        for i in self.tv1.selection():
            self.tv1.delete(i)
        self.printar_nativo()
        for item in self.Figure_Canvas1.get_tk_widget().find_all():
            self.Figure_Canvas1.get_tk_widget().delete(item)
        for item in self.Figure_Canvas2.get_tk_widget().find_all():
            self.Figure_Canvas2.get_tk_widget().delete(item)
        self.Figure_Canvas1.get_tk_widget().pack_forget()
        self.Figure_Canvas2.get_tk_widget().pack_forget()
        plt.clf()
        plt.cla()
        plt.close(self.fig1)
        plt.close(self.fig2)

    ## Funcao de probabilidade
    ## @param uma np.array com as notas da disciplina
    ## @return as densidades de probabilidade, eixo y
    def fun_prob(self,x):
        mean = np.mean(x)
        std = np.std(x)
        y = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
        return y

    ## Gera grafo dos valores originais da disciplina
    ## @param String da disciplina
    ## @return um objeto plt.figure
    def grafo_normal(self,disciplina):
        if disciplina == None:
            pass
        else:
            x = np.array(sorted(self.df[disciplina]))

            y = self.fun_prob(x)

            plt.style.use('seaborn')
            self.fig1 = plt.figure(1,figsize=(6, 6))
            plt.plot(x, y, color='black', linestyle='dashed',label="gaussiana")
            plt.scatter(x, y, marker='o', s=25, color='red',label=disciplina)
            plt.legend(loc="upper left")
            plt.fill_between(x, y, 0, alpha=0.2, color='blue')
            plt.title("Curva Original")
            plt.xlabel("nota")
            plt.ylabel("densidade de probabilidade")

            return self.fig1

    ## Limita a nota no maximo 100 para Escalar Linear
    ## @param nota, minimo obtido, maximo obtido
    ## @return nota limitado a 100
    def limit_nota(self,nota,min_raw,max_raw):
        nota = self.formula_linear(nota,min_raw,max_raw)
        if nota > 100:
            return 100
        else:
            return nota

    ## Formula linear
    ## @param nota, minimo obtido, maximo obtido
    ## @return nota ajustada p/ escala linear
    def formula_linear(self,nota,min_raw,max_raw):
        nova_nota = 100 + ((60 - 100) / (min_raw - max_raw)) * (nota - max_raw)
        return nova_nota

    ## Gera grafo com valores ajustados, ele cria as 2 figuras no FigureCanvas e retorn tabela como objeto DataFrame
    ## para a funcao printar_tabela_atualizada
    ## @param String disciplina, String tipo e o um objeto DataFrame
    ## @return objeto DataFrame
    def gerar_grafo_ajustado(self,disciplina,tipo,df):
        self.GPA = False
        if tipo == "Raiz Quadrada":
            df_nativo = df
            dataframe = np.array(sorted(df[disciplina]))
            x = []
            for nota in dataframe:
                nota = np.sqrt(nota)*10
                x.append(nota)

            y = self.fun_prob(x)
            plt.style.use('seaborn')
            self.fig2 = plt.figure(2,figsize=(6, 6))
            plt.plot(x, y, color='black', linestyle='dashed',label="gaussiana")
            plt.scatter(x, y, marker='o', s=25, color='red',label=disciplina)
            plt.legend(loc="upper left")
            plt.fill_between(x, y, 0, alpha=0.2, color='blue')
            plt.title("Curva Ajustada")
            plt.xlabel("10 * sqrt(nota)")
            plt.ylabel("densidade de probabilidade")

            self.Figure_Canvas1 = FigureCanvasTkAgg(self.fig2,master=self.Canvas)
            self.Figure_Canvas2 = FigureCanvasTkAgg(self.grafo_normal(disciplina),master=self.Canvas)

            self.Figure_Canvas1.get_tk_widget().pack(side=LEFT)
            self.Figure_Canvas2.get_tk_widget().pack(side=RIGHT)

            df_nativo[disciplina] = df_nativo[disciplina].apply(lambda x: int(np.rint(np.sqrt(x)*10)))
            return df_nativo

        elif tipo == "Escala Linear":
            ## Nao entendi na prova qual o alcance que quer que ocorra a distribuicao, ou seja, o max valor desejado e o min
            ## Assumi entao valores 60 - 100
            df_nativo = df
            dataframe = np.array(sorted(df[disciplina]))
            min_raw = dataframe.min()
            max_raw = dataframe.max()
            median = df[disciplina].median()

            x = []
            for nota in dataframe:
                nota = self.formula_linear(nota,min_raw,max_raw)
                if nota > 100:
                    x.append(100)
                else:
                    x.append(nota)

            y = self.fun_prob(x)
            plt.style.use('seaborn')
            self.fig2 = plt.figure(2, figsize=(6, 6))
            plt.plot(x, y, color='black', linestyle='dashed', label="gaussiana")
            plt.scatter(x, y, marker='o', s=25, color='red', label=disciplina)
            plt.legend(loc="upper left")
            plt.fill_between(x, y, 0, alpha=0.2, color='blue')
            plt.title("Curva Ajustada")
            plt.xlabel("f(x) = y0 + (y1-y0)/(x1-x0)*(nota-x0)")
            plt.ylabel("densidade de probabilidade")

            self.Figure_Canvas1 = FigureCanvasTkAgg(self.fig2, master=self.Canvas)
            self.Figure_Canvas2 = FigureCanvasTkAgg(self.grafo_normal(disciplina), master=self.Canvas)

            self.Figure_Canvas1.get_tk_widget().pack(side=LEFT)
            self.Figure_Canvas2.get_tk_widget().pack(side=RIGHT)

            df_nativo[disciplina] = df_nativo[disciplina].apply(lambda x: int(np.rint(self.limit_nota(x,min_raw,max_raw))))
            return df_nativo


        elif tipo == "Nota mais alta 100":
            df_nativo = df
            dataframe = np.array(sorted(df[disciplina]))
            max = np.max(dataframe)
            amount_add = 100 - max
            x = []
            for nota in dataframe:
                nota += amount_add
                x.append(nota)

            y = self.fun_prob(x)
            plt.style.use('seaborn')
            self.fig2 = plt.figure(2, figsize=(6, 6))
            plt.plot(x, y, color='black', linestyle='dashed',label="gaussiana")
            plt.scatter(x, y, marker='o', s=25, color='red',label=disciplina)
            plt.legend(loc="upper left")
            plt.fill_between(x, y, 0, alpha=0.2, color='blue')
            plt.title("Curva Ajustada")
            plt.xlabel("nota + (100 - nota max)")
            plt.ylabel("densidade de probabilidade")

            self.Figure_Canvas1 = FigureCanvasTkAgg(self.grafo_normal(disciplina), master=self.Canvas)
            self.Figure_Canvas2 = FigureCanvasTkAgg(self.fig2, master=self.Canvas)

            self.Figure_Canvas1.get_tk_widget().pack(side=LEFT)
            self.Figure_Canvas2.get_tk_widget().pack(side=RIGHT)

            df_nativo[disciplina] = df_nativo[disciplina].apply(lambda x: x+amount_add)
            return df_nativo


    ## Compara valor da nota com os conceitos correspondentes
    ## @param a nota int
    ## @return String com conceito GPA
    def grade(self, nota):
        Arr = []
        Arr.append(nota)
        Grade = pd.cut(Arr, right=False, labels=self.label, bins=self.bin)
        return Grade[0]

    ## Funcao de fato troca a nota na tabela atual e atualiza ela com os conceitos GPA
    ## utiza o DataFrame atual, ou o ultimo modificado
    def trocar_nota_por_conceito(self):
        self.GPA = True
        Disciplina = ['History','Geography','Maths','Biology','Physics','Chemistry','Literature']
        for i in Disciplina:
            self.df[i] = self.df[i].apply(lambda x: self.grade(x))

        for i in self.tv1.get_children():
            self.tv1.delete(i)
        for i in self.tv1.selection():
            self.tv1.delete(i)

        self.tv1["column"] = list(self.df.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1["columns"]:
            self.tv1.heading(column,text=column)

        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert("","end",values=row)

    ## Salva DataFrame atual, ou ultimo modificado para uma planilha excel
    def save_to_excel(self):
        if self.GPA == True:
            self.df.to_excel("gpa.xlsx")
        else:
            tkinter.messagebox.showerror("Error","Notas nao estao em conceito GPA")




Main = Tk()
Program(Main)
Main.mainloop()