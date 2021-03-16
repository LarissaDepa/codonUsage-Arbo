import pymysql as MySQLdb
import csv
import click
import os
import re


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


@click.command()
@click.argument("file", type=click.File())
def inserir_freqhost(file):
    """Script para inserir automaticamente dados no formato CSV
    em um banco de dados MySQL

    FILE é um arquivo de dados no formato csv

    DADOS = Frequencia de genes tRNA e códons DNA
    """
    arq = csv.reader(file, delimiter=";")
    for item in arq:
        print(item)
        print(item[0])
        freqabsol = int(item[1])
        freqtotal = int(item[2])
        freqrelativa = freqabsol/freqtotal
        FK_codon = item[0]
        FK_codon = re.sub("\\ufeff", "", FK_codon)

        conn = conexao()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT tblFrequenciaCodonHost(FK_codonDNA, FreqAbsolutaHost, FreqRelativaHost, TotalFreqAH) VALUES( %s, %s, %s , %s)",
                           (FK_codon, freqabsol, freqrelativa, freqtotal))
            conn.commit()

            print(
                "INSERT tblFrequenciaCodonHost(FK_codonDNA,FreqAbsolutaHost, FreqRelativaHost, TotalFreqAH) VALUES(%s, %s, %s,%s)",
                (FK_codon, freqabsol, freqrelativa, freqtotal)
            )

        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")


inserir_freqhost()
desconectar(conn)
