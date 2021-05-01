import pymysql as MySQLdb
import csv
import click
import os


def conexao():
    try:
        conn = MySQLdb.connect(
            host="localhost", user="root", passwd="", db="db"
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
def inserir_freqtrna(file):
    """Script para inserir automaticamente dados no formato CSV
    em um banco de dados MySQL

    FILE é um arquivo de dados no formato csv

    DADOS = Frequencia de genes tRNA e códons DNA
    """
    arq = csv.reader(file, delimiter=";")
    for item in arq:
        print(item)
        conn = conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT tblFrequenciaGenesTrna(FK_codonDNA,FreqGeneTrna) VALUES(%s, %s)",
                item,
            )
            conn.commit()

            print(
                "INSERT tblFrequenciaGenesTrna(FK_codonDNA,FreqGeneTrna) VALUES(%s, %s)",
                item,
            )

        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")


inserir_freqtrna()
desconectar(conn)
