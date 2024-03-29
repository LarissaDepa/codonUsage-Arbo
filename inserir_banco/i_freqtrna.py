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

log = open('up_mysql_trna.log', 'w')


for codon in codonLines:
    codon = codon.rstrip('\n')
    codonelement = codon.split()
    anticodon = codonelement[1]
    freqGene = codonelement[2]

    anticodon = Seq(anticodon)
    codonDNA = anticodon.reverse_complement()
    codonRNA = re.sub("T", "U", str(codonDNA))
    # frequencia1 = int(freqGene)/429
    print(anticodon, " ", codonDNA, " ", codonRNA,
          " ", freqGene)

    log.write(str(anticodon))

    try:
        sql = 'INSERT INTO tblFrequenciaGenesTrna (FK_codonRNA, FK_codonDNA, trnaHost, countAnticodon) VALUES (%s, %s, %s, %s)'
        sql_data = (codonRNA, codonDNA, anticodon, freqGene)
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


cursor.close()
con.close()
log.close()
codonFile.close()
