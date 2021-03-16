import re
import pymysql as MySQLdb
import click


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
@click.argument('file')
def inserir_freqdenv3(file):

    tabela_file = open(file, 'r')
    tabela_lines = tabela_file.readlines()
    tupla_lista = tuple()
    lista_tupla = []
    for tabela_line in tabela_lines:
        tabela_line = tabela_line.rstrip('\n')
        columns = tabela_line.split()

        if not columns == []:
            if (columns[0].isdigit()):

                totalav = columns[0]
                genomaid = columns[3]
                #idg = re.sub("\|Orga", "", genomaid)
                idg = re.sub("\|.*", "", genomaid)
                refseq = "lcl|NC_001475.2_cds_YP_001621843.1_1 "
                for item_tupla in lista_tupla:
                    freqabsoluta = item_tupla[1]
                    try:
                        a = int(item_tupla[1])
                        b = int(totalav)
                        freqrelativa = a/b
                    except ZeroDivisionError:
                        freqrelativa = 0
                    codon = item_tupla[0]
                    conn = conexao()
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            f"INSERT INTO tblFrequenciaCodonVirus(FK_codonRNA,FK_genomaID,FK_RefCdsID,FreqAbsolutaVirus,FreqRelativaVirus,TotalFreqAV)"
                            f"VALUES( '{codon}', '{idg}','{refseq}', '{freqabsoluta}', '{freqrelativa}', '{totalav}');"
                        )
                        conn.commit()
                        print(
                            f"INSERT INTO tblFrequenciaCodonVirus(FK_codonRNA,FK_genomaID,FK_RefCdsID,FreqAbsolutaVirus,FreqRelativaVirus,TotalFreqAV)"
                            f"VALUES('{codon}', '{idg}','{refseq}', '{freqabsoluta}', '{freqrelativa}', '{totalav}');"
                        )

                    except MySQLdb.Error as e:
                        print(f"Erro ao conectar no Servidor MySQL: {e}")
                lista_tupla = []

            elif ((columns[0] == "Phe") or (columns[0] == "Ile") or (columns[0] == "Val")):
                aa1 = (columns[1], columns[2])
                aa2 = (columns[5], columns[6])
                aa3 = (columns[9], columns[10])
                aa4 = (columns[13], columns[14])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif ((columns[0] == "GUC") or (columns[0] == "GUG") or (columns[0] == "AUC") or (columns[0] == "UUC") or (columns[0] == "CUC") or (columns[0] == "CUG")):
                aa1 = (columns[0], columns[1])
                aa2 = (columns[3], columns[4])
                aa3 = (columns[6], columns[7])
                aa4 = (columns[9], columns[10])
                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif (columns[0] == "Leu"):
                aa1 = (columns[1], columns[2])
                aa2 = (columns[4], columns[5])
                aa3 = (columns[8], columns[9])
                aa4 = (columns[12], columns[13])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif (columns[0] == "UUG"):
                aa1 = (columns[0], columns[1])
                aa2 = (columns[3], columns[4])
                aa3 = (columns[6], columns[7])
                aa4 = (columns[10], columns[11])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif (columns[0] == "CUU"):
                aa1 = (columns[0], columns[1])
                aa2 = (columns[4], columns[5])
                aa3 = (columns[8], columns[9])
                aa4 = (columns[12], columns[13])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif ((columns[0] == "GUA") or (columns[0] == "CUA")):
                aa1 = (columns[0], columns[1])
                aa2 = (columns[3], columns[4])
                aa3 = (columns[7], columns[8])
                aa4 = (columns[10], columns[11])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif (columns[0] == "Met"):
                aa1 = (columns[1], columns[2])
                aa2 = (columns[4], columns[5])
                aa3 = (columns[7], columns[8])
                aa4 = (columns[10], columns[11])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            elif (columns[0] == "AUA"):
                aa1 = (columns[0], columns[1])
                aa2 = (columns[3], columns[4])
                aa3 = (columns[7], columns[8])
                aa4 = (columns[11], columns[12])

                lista_tupla.append(aa1)
                lista_tupla.append(aa2)
                lista_tupla.append(aa3)
                lista_tupla.append(aa4)

            else:
                print('ERRO', columns[0])


inserir_freqdenv3()
desconectar(conn)
