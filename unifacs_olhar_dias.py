import re

s = """Semestre: 1º
Disciplina: ALGORITMOS E PROGRAMAÇÃO
Código: MR01
Dia / Período: SEGUNDA-FEIRA
Horário: 7:15 - 8:30
Sala: 201 PA6 - SALA.COM
Prédio: RV
Professor:
Semestre: 1º
Disciplina: ALGORITMOS E PROGRAMAÇÃO - PA
Código: MR01
Dia / Período: SEGUNDA-FEIRA
Horário: 8:40 - 9:55
Sala: SALA ARTHE PA6
Prédio: RV
Professor:
Semestre: 1º
Disciplina: ALGORITMOS E PROGRAMAÇÃO - PB
Código: MR01
Dia / Período: QUINTA-FEIRA
Horário: 8:40 - 9:55
Sala: PRANCHETAS 03 PA6
Prédio: RV
Professor:
Semestre: 1º
Disciplina: COMUNICAÇÃO
Código: MR01
Dia / Período: SÁBADO
Horário: 8:40 - 9:55
Sala: A DEFINIR
Prédio: RV
Professor:
Semestre: 1º
Disciplina: EXPRESSÃO GRÁFICA
Código: MR01
Dia / Período: SEXTA-FEIRA
Horário: 10:05 - 11:20
Sala: PRANCHETAS 02 PA6
Prédio: RV
Professor:
Semestre: 1º
Disciplina: EXPRESSÃO GRÁFICA
Código: MR01
Dia / Período: SEXTA-FEIRA
Horário: 11:30 - 12:45
Sala: PRANCHETAS 02 PA6
Prédio: RV
Professor:
Semestre: 1º
Disciplina: INTRODUÇÃO A ENGENHARIA
Código: MR01
Dia / Período: TERÇA-FEIRA
Horário: 8:40 - 9:55
Sala: 201 PA6 - SALA.COM
Prédio: RV
Professor:
Semestre: 1º
Disciplina: QUÍMICA GERAL
Código: MR01
Dia / Período: QUINTA-FEIRA
Horário: 11:30 - 12:45
Sala: 07 ANEXO B PA7 - SALA.COM
Prédio: RV
Professor:
Semestre: 1º
Disciplina: QUÍMICA GERAL - PA
Código: MR01
Dia / Período: QUINTA-FEIRA
Horário: 10:05 - 11:20
Sala: 10 ANEXO B PA7
Prédio: RV
Professor:
Semestre: 1º
Disciplina: QUÍMICA GERAL - PB
Código: MR01
Dia / Período: QUINTA-FEIRA
Horário: 10:05 - 11:20
Sala: 09 ANEXO B PA7
Prédio: RV
Professor:"""

materias = re.findall("Semestre:\s?([^\n]*)\n" # index 0, 
                      "Disciplina:\s?([^\n]*)\n" # 1
                      "Código:\s?([^\n]*)\n" #  2
                      "Dia / Período:\s?([^\n]*)\n" #  3
                      "Horário:\s?([^\n]*)\n" # 4
                      "Sala:\s?([^\n]*)\n"  # 5
                      "Prédio:\s?([^\n]*)\n", s) # 6
for dia in ['SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA',
            'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SÁBADO', 'DOMINGO']:
    print(f'*{dia}:*')
    for materia in materias:
        if dia in materia:
            print(f'\t{materia[1]}: {materia[4]} ({materia[5]})')
    print()

