import pymysql as MySQLdb
import os
from optparse import OptionParser
from Bio.Seq import Seq
import getpass
import re

argv = OptionParser()
argv.add_option("-u", "--user", action="store", dest="user", type="string",
                help="usuario do banco de dados")
argv.add_option("-d", "--databank", action="store", dest="db", type="string",
                help="nome do banco de dados")
argv.add_option("-l", "--lhost", action="store", dest="host", type="string",
                help="localhost")

(argumentos, palha_que_nao_interessa) = argv.parse_args()

password = getpass.getpass('password: ')

con = MySQLdb.connect(host=argumentos.host,
                      user=argumentos.user, passwd=password, db=argumentos.db)
cursor = con.cursor()

log = open('up_mysql_tscore.log', 'w')

try:
    sql = 'select FK_codonRNA, FK_genomaID , FK_RefCdsID , FreqRelativaVirus  from  tblFrequenciaCodonVirus'
    cursor.execute(sql)
    con.commit()
    myresult = cursor.fetchall()
    try:
        for x in myresult:
            resultado = (list(x))
            print("virus", resultado[0], "\t", resultado[1])
            codonRNA = resultado[0]
            genomaID = resultado[1]
            refcdsID = resultado[2]
            freqrelativav = resultado[3]

            sql1 = 'select FK_codonRNA,FK_codonDNA,t_valor from  tblFrequenciaGenesTrna WHERE FK_codonRNA = "%s"' % (
                codonRNA)
            cursor.execute(sql1)
            con.commit()
            myresult_H = cursor.fetchall()
            try:
                for H in myresult_H:
                    resultado_H = (list(H))
                    print(
                        "humano", "\t", resultado_H[0], "\t", resultado_H[1], "\t", resultado_H[2])
                    t_valor = resultado_H[2]
                    codonDNA = resultado_H[1]

                    sql2 = 'select FK_codonDNA, FreqRelativaHost from  tblFrequenciaCodonHost WHERE FK_codonDNA = "%s"' % (
                        codonDNA)
                    cursor.execute(sql2)
                    con.commit()
                    myresult_H2 = cursor.fetchall()
                    try:
                        for H2 in myresult_H2:
                            resultado_H2 = (list(H2))
                            print("frequencia", "\t",
                                  resultado_H2[0], "\t", resultado_H2[1])
                            freqhost = resultado_H2[1]

                            try:
                                tscoreparte01 = (
                                    freqrelativav - freqhost) / freqhost
                            except ZeroDivisionError:
                                tscoreparte01 = 0

                            try:
                                tscore = tscoreparte01 / t_valor
                            except ZeroDivisionError:
                                tscore = 0

                            print("resultado \t", codonRNA, "\t",
                                  genomaID, "\t", refcdsID, "\t", tscore)

                            # INSERINDO RESULTADO NA TABELA
                            try:
                                sql_insert = 'UPDATE  tblFrequenciaCodonVirus SET tscore = %s WHERE FK_codonRNA = %s and FK_genomaID =%s and FK_RefCdsID = %s'
                                sql_data_insert = (tscore, codonRNA,
                                                   genomaID, refcdsID)
                                cursor.execute(sql_insert, sql_data_insert)
                                con.commit()

                            except MySQLdb.IntegrityError as i:
                                print("Mysql IntegrityError")
                                dontWork = str(i)
                                log.write('\t ' + dontWork)

                            except MySQLdb.Error as e:
                                print("Mysql ERROR")
                                dontWork = str(e)
                                log.write('\t ' + dontWork)

                    except IndexError:
                        print("---Erro")

            except IndexError:
                print("---Erro")

    except IndexError:
        print("---Erro")

except MySQLdb.IntegrityError as i:
    print("Mysql IntegrityError")
    dontWork = str(i)
    log.write('\t ' + dontWork)

except MySQLdb.Error as e:
    print("Mysql ERROR")
    dontWork = str(e)
    log.write('\t ' + dontWork)

# select f.FK_codonRNA, f.FreqRelativaVirus, g.nomeOrganismo from  tblFrequenciaCodonVirus f, tblGenomaVirus g WHERE g.genomaID = f.FK_genomaID;
