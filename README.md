# Análise de Notas de Alunos e Aplicar uma Curva
Parte de um trabalho de graduação, era necessário criar uma interface gráfica com Tkinter que pudesse escolher o tipo de curva para aplicar as notas de alunos, no caso, uma planilha excel, mostrar graficamente e gerar uma planilha com valores atualizados.

Os tipos de ajuste eram :

-Raiz Quadrada (10*sqrt(nota))

-Escala Linear (dado valores target min e max -> f(x) = max + ((min - max) / (min_raw - max_raw)) * (nota - max_raw)))

-Nota mais alta 100 (a nota mais vira 100 e a diferença entre 100 - valor original da maior nota é aplicado para todas as outras notas).
