import pymysql as MySQLdb
from Bio import SeqIO
import click
import re


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
def inserir_refseq(file):
    """Script para inserir automaticamente sequências referências (CDS)
     retiradas do NCBI(https://www.ncbi.nlm.nih.gov/) num banco de dados MySQL

    FILE é um arquivo de dados no formato FASTA

    DADOS = sequências referências(cds)
    """
    click.echo(file)
    for item in SeqIO.parse(file, "fasta"):
        resumo = dict(x.split(":") for x in item.description.split("[]"))
        id_name = item.id
        seq = item.seq
        print(resumo)
        conn = conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO tblRefCds(RefCdsID, seqRefCds) "
                f"VALUES('{id_name}','{seq}');"
            )
            conn.commit()

            print(
                f"INSERT INTO tblRefCds(RefCdsID, seqRefCds)"
                f"VALUES('{id_name}','{seq}');"
            )
        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")


inserir_refseq()
desconectar(conn)
