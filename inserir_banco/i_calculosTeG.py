import pymysql as MySQLdb
import os
from optparse import OptionParser
from Bio.Seq import Seq
import getpass
import re

argv = OptionParser()
argv.add_option("-I", "--InputTable", action="store", dest="file", type="string",
                help="arquivo de codons")
argv.add_option("-u", "--user", action="store", dest="user", type="string",
                help="usuario do banco de dados")
argv.add_option("-d", "--databank", action="store", dest="db", type="string",
                help="nome do banco de dados")
argv.add_option("-l", "--lhost", action="store", dest="host", type="string",
                help="localhost")

(argumentos, palha_que_nao_interessa) = argv.parse_args()
codonFile = open(argumentos.file, 'r')
codonLines = codonFile.readlines()

password = getpass.getpass('password: ')

con = MySQLdb.connect(host=argumentos.host,
                      user=argumentos.user, passwd=password, db=argumentos.db)
cursor = con.cursor()

log = open('up_mysql_teG.log', 'w')


for codon in codonLines:
    codon = codon.rstrip('\n')
    codonelement = codon.split()
    g_asterisco = codonelement[3]
    g_asterisco = re.sub(",", ".", g_asterisco)
    codon = codonelement[0]
    print(codonelement[0])

    try:
        g_rich_poor = codonelement[4]
    except IndexError:
        g_rich_poor = "NULL"

    try:
        t_valor = codonelement[5]
        t_valor = re.sub(",", ".", t_valor)
    except IndexError:
        t_valor = 0

    try:
        fracao = codonelement[6]
        fracao = re.sub(",", ".", fracao)
    except IndexError:
        fracao = 0
    try:
        G = codonelement[7]
    except IndexError:
        G = 0

    print(codon, "\t", g_asterisco, "\t", g_rich_poor,
          "\t", t_valor, "\t", fracao, "\t", G)

    try:
        sql = 'UPDATE tblFrequenciaGenesTrna SET g_asterisco = %s, g_rich_poor = %s,  t_valor = %s, fracao = %s, G = %s WHERE FK_codonRNA = %s'
        sql_data = (g_asterisco, g_rich_poor, t_valor, fracao, G, codon)
        cursor.execute(sql, sql_data)
        con.commit()

    except MySQLdb.IntegrityError as i:
        print("Mysql IntegrityError")
        dontWork = str(i)
        log.write('\t ' + dontWork)

    except MySQLdb.Error as e:
        print("Mysql ERROR")
        dontWork = str(e)
        log.write('\t ' + dontWork)

    log.write("\n")
