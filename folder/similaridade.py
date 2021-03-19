import os
import re
import math
import pymysql as MySQLdb


def conexao():
    try:
        conn = MySQLdb.connect(
            host="localhost", user="root", passwd="lares", db="db_codonusage"
        )
        print("conectado")
        return conn
    except MySQLdb.Error as e:
        print(f"Erro ao conectar no Servidor MySQL: {e}")


def desconectar(conn):
    if conn:
        conn.close()


conn = conexao()


especiesA = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "select FK_genomaID,FK_RefCdsID from tblAlinhamentos")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        especiesA.append(myresult)

    # print("select FK_genomaID,FK_RefCdsID from tblAlinhamentos")


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")


FreqsEspecieB = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "select c.codonRNA , h.FreqRelativaHost from  tblCodons c, tblFrequenciaCodonHost h where h.FK_codonDNA = c.codonDNA")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        FreqsEspecieB.append(myresult)

    # print("select c.codonRNA , h.FreqRelativaHost from  tblCodons c, tblFrequenciaCodonHost h where h.FK_codonDNA = c.codonDNA")


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

for especieA in especiesA:
    print("Genoma: ", especieA[0], " RefSeq: ", especieA[1])

    FreqsEspecieA = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"select FK_codonRNA , FreqRelativaVirus from  tblFrequenciaCodonVirus where  FK_genomaID = '{especieA[0]}' and FK_RefCdsID = '{especieA[1]}'")
        conn.commit()
        myresults = cursor.fetchall()
        for myresult in myresults:
            FreqsEspecieA.append(myresult)

       # print( f"select FK_codonRNA , FreqRelativaVirus from  tblFrequenciaCodonVirus where  FK_genomaID = '{especieA[0]}' and FK_RefCdsID = '{especieA[1]}'")

    except MySQLdb.Error as e:
        print(f"Erro ao conectar no Servidor MySQL: {e}")

    # print("Freq EspecieA", FreqsEspecieA)
    tamanhofreq = len(FreqsEspecieA)
    # print('O tamanho da freq é : ', tamanhofreq)

    elementosuperior = []
    elementoinferiorA = []
    elementoinferiorB = []

    for FreqEspecieA in FreqsEspecieA:
        for FreqEspecieB in FreqsEspecieB:
            if FreqEspecieB[0] == FreqEspecieA[0]:
               # print("codon: ", FreqEspecieA[0], " freq: ", FreqEspecieA[1])
               # print("codonB: ", FreqEspecieB[0], " freqB: ", FreqEspecieB[1])

                elementosuperior.append(FreqEspecieA[1]*FreqEspecieB[1])
                elementoinferiorA.append(FreqEspecieA[1]**2)
                elementoinferiorB.append(FreqEspecieB[1]**2)

    soma = sum(elementosuperior)
    somaA = sum(elementoinferiorA)
    somaB = sum(elementoinferiorB)
    raiz = math.sqrt(somaA*somaB)

    similaridade = soma/raiz

    print('Similaridade entre ', especieA[0], 'e humano é : ', similaridade)

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tblCalculos(FK_genomaID,FK_RefseqCdsID,similaridade) VALUES ( %s, %s, %s)",
            (especieA[0], especieA[1], similaridade)
        )
        conn.commit()
        print(
            "INSERT INTO tblCalculos(FK_genomaID,FK_RefseqCdsID,similaridade) VALUES ( %s, %s, %s)",
             (especieA[0], especieA[1], similaridade)

        )

    except MySQLdb.Error as e:
        print(f"Erro ao conectar no Servidor MySQL: {e}")

desconectar(conn)
