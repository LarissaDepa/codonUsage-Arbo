# Cálculo do valor de g* do “códon rico” e “códon pobre”.

import os
import re
import math
import pymysql as MySQLdb
import functools
import itertools


def conexao():
    try:
        conn = MySQLdb.connect(
            host="localhost", user="root", passwd="laras", db="db_codonusage"
        )
        print("conectado")
        return conn
    except MySQLdb.Error as e:
        print(f"Erro ao conectar no Servidor MySQL: {e}")


def desconectar(conn):
    if conn:
        conn.close()


conn = conexao()

# countAnticodon - tblFrequenciaGenesTrna = Frequência de genes de tRNA (grtnadb) humano.
# codonDNA - tblCodon = codons Fk_codonDNA
# codonRNA - tblCodon = codons Fk_codonRNA


FreqsGenesTrna = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "select c.codonRNA , a.countAnticodon from  tblCodons c, tblFrequenciaGenesTrna a where a.FK_codonDNA = c.codonDNA")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        FreqsGenesTrna.append(myresult)


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

# FreqAbsolutaHost - tblFrequenciaCodonHost = Frequência absoluta de códons do hospedeiro humano.

FreqsAbsHost = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "select c.codonRNA, a.FreqAbsolutaHost from  tblCodons c, tblFrequenciaCodonHost a where a.FK_codonDNA = c.codonDNA")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        FreqsAbsHost.append(myresult)
except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

codonsC = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codonRNA FROM tblCodons where codonRNA like '%C'")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        codonsC.append(list(myresult))
        # print(codons)

except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")


codonsU = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codonRNA FROM tblCodons where codonRNA like '%U'")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        codonsU.append(list(myresult))
        # print(codons)

except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")


# Todas as frequências de códons que terminam com C
freqanticodon_C = []
freqanticodon_U = []

freqanticodon_C2 = []
freqanticodon_U2 = []

for freq in FreqsGenesTrna:
    for codon in codonsC:
        if freq[0] == codon[0]:
            freqanticodon_C.append(freq[1])
            freqanticodon_C2.append(freq[0])

# Todas as frequências de códons que terminam com T ou U

    for codon in codonsU:
        if freq[0] == codon[0]:
            freqanticodon_U.append(freq[1])
            freqanticodon_U2.append(freq[0])

print(freqanticodon_C, freqanticodon_U)
print(freqanticodon_C2, freqanticodon_U2)

# Calculando G que é gi + gj
# G = g_rich + g_poor

# Primeira forma de fazer G
# G = [freqanticodon_C[i] + freqanticodon_U[i]
#      for i in range(len(freqanticodon_C))]
# print("Resultado de G é: " + str(G))

# Segunda forma de fazer G com itertools
G = list(map(sum, zip(freqanticodon_C, freqanticodon_U)))
print("Os valores de G são: ", G)


# Quem é a frequencia de do gtrndb do códon pobre e códon rico
Lista_freqanticodon = list(zip(freqanticodon_C, freqanticodon_U))
print(Lista_freqanticodon)

for i in Lista_freqanticodon:
    print('A freq de g_rich: ', max(i),  ' A freq de g_poor é: ', min(i))


desconectar(conn)
