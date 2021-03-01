import pymysql as MySQLdb
from Bio import SeqIO
import click
import re
from Bio import AlignIO
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
@click.option(
    "--path", default=".", type=click.Path(exists=True), help="Path para ser listado."
)
def inserir_alinh(path):
    with os.scandir(path) as d:
        conn = conexao()
        for e in d:
            if not e.name.startswith(".") and e.is_file():
                lista_line = e.name
                for i in lista_line:
                    seqaln = AlignIO.read(lista_line, "fasta")
                    for record in seqaln:
                        id_alnRef = seqaln[0].id  # id RefSeq
                        id_alnG = seqaln[1].id
                        id_alnGE = re.search(r".*\|", id_alnG)  # id genoma
                        id_alnGE = re.sub("\|", " ", id_alnGE[0])
                        seq1 = seqaln[0].seq  # sequência refseq
                        seq2 = seqaln[1].seq  # sequência genoma
                        alinhamento = (
                            ">"
                            + id_alnRef
                            + "\n"
                            + seq1
                            + "\n"
                            + ">"
                            + id_alnGE
                            + "\n"
                            + seq2
                            + "\n"
                        )
            try:
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO tblAlinhamentos(FK_genomaID,FK_RefCdsID, seqAln)"
                    f"VALUES( '{id_alnGE}', '{id_alnRef}','{alinhamento}');"
                )
                conn.commit()
                print(
                    f"INSERT INTO tblAlinhamentos(FK_genomaID, FK_RefCdsID, seqAln)"
                    f"VALUES('{id_alnGE}', '{id_alnRef}', '{alinhamento}');"
                )
            except MySQLdb.Error as e:
                print(f"Erro ao conectar no Servidor MySQL: {e}")


inserir_alinh()
desconectar(conn)
