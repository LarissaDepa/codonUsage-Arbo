import pymysql as MySQLdb
from Bio import SeqIO
import click
import re
from collections import defaultdict


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
def inserir_genoma(file):
    """Script para inserir automaticamente sequências de genomas
      completos retiradas do VIPR(https://www.viprbrc.org/) num banco de dados MySQL

    FILE é um arquivo de dados no formato FASTA

    DADOS = sequências de genomas completos.
    """
    click.echo(file)
    for item in SeqIO.parse(file, "fasta"):
        resumo = dict(x.split(":") for x in item.description.split("|"))
        resumo.setdefault("Organism", "None")
        resumo.setdefault("Strain Name", "None")
        resumo.setdefault("Segment", "None")
        resumo.setdefault("Host", "None")
        resumo.setdefault("Subtype", "None")
        cab_id = item.id
        id_name = re.search(r".*\|", cab_id)
        id_name = re.sub("\|", "", id_name[0])
        organism = resumo["Organism"]
        strain_name = resumo["Strain Name"]
        segment = resumo["Segment"]
        host = resumo["Host"]
        subtipo = resumo["Subtype"]
        seq = item.seq
        print(resumo)
        conn = conexao()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO tblGenomaVirus (genomaID, nomeOrganismo, nomeCepa, segmento, hospedeiro, subtipo, seqGenomaVirus) "
                f"VALUES('{id_name}','{organism}','{strain_name}','{segment}','{host}', '{subtipo}','{seq}');"
            )
            conn.commit()

            print(
                f"INSERT INTO tblGenomaVirus (genomaID, nomeOrganismo, nomeCepa, segmento, hospedeiro, subtipo, seqGenomaVirus)"
                f"VALUES('{id_name}','{organism}','{strain_name}','{segment}','{host}', '{subtipo}','{seq}');"
            )
        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")


inserir_genoma()
desconectar(conn)
