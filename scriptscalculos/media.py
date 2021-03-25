import pymysql as MySQLdb
import statistics


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
# selecionando somente os genomas sem stopcodon
genomas = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "select genomaID from tblGenomaVirus")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        genomas.append(list(myresult))
        # print(myresult)


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

stopcodons = ['UAA', 'UAG', 'UGA']
genomas_SEMstop = []
for genoma in genomas:
    valorstopcodon = []
    for stopcodon in stopcodons:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"select   FreqAbsolutaVirus  from  tblFrequenciaCodonVirus where FK_codonRNA ='{stopcodon}' and FK_genomaID = '{genoma[0]}' ")
            conn.commit()
            myresults = cursor.fetchall()
            for myresult in myresults:
                valorstopcodon.append(list(myresult))

        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")
    # print(genoma[0], valorstopcodon)

    total_stopcodon = 0
    for i in valorstopcodon:
        total_stopcodon = total_stopcodon + i[0]
    # print(genoma[0], total_stopcodon)
    if total_stopcodon == 1:
        genomas_SEMstop.append(genoma[0])
print('VOCE TEM ', len(genomas_SEMstop), ' genomas sem stop codons ')

# selecionando os codons
codons = []
try:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codonRNA FROM tblCodons")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        codons.append(list(myresult))
        # print(codons)


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

# selecionando as refseqs

refseqs = []
try:
    cursor = conn.cursor()
    cursor.execute("select RefCdsID from  tblRefCds")
    conn.commit()
    myresults = cursor.fetchall()
    for myresult in myresults:
        refseqs.append(list(myresult))
        # print(refseqs)


except MySQLdb.Error as e:
    print(f"Erro ao conectar no Servidor MySQL: {e}")

for codon in codons:
    # print('codon', codon)
    for refseq in refseqs:
        Freqlist = []
        print('refseq', refseq)
        try:
            cursor2 = conn.cursor()
            cursor2.execute(
                f"select  FreqAbsolutaVirus, FK_genomaID from  tblFrequenciaCodonVirus where FK_RefCdsID = '{refseq[0]}' and   FK_codonRNA = '{codon[0]}' ")
            conn.commit()
            myresults2 = cursor2.fetchall()
            for myresult2 in myresults2:
                Freqlist.append(list(myresult2))
                # print(myresult2)

        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")
        frequenciasValor = []
        for freqitem in Freqlist:
            if freqitem[1] in genomas_SEMstop:
                frequenciasValor.append(freqitem[0])

        media = statistics.mean(frequenciasValor)

        print(f' A média {media}, do códon {codon[0]} da refseq {refseq[0]}')

        # try insert aqui nessa linha
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tblCalculosCodon(FK_codonRNA, FK_RefseqCdsID,mediaFreqCodon) VALUES ( %s, %s, %s)",
                (codon[0], refseq[0], media)
            )
            conn.commit()
            print(
                "INSERT INTO tblCalculosCodon(FK_codonRNA, FK_RefseqCdsID,mediaFreqCodon) VALUES ( %s, %s, %s)",
                (codon[0], refseq[0], media)

            )

        except MySQLdb.Error as e:
            print(f"Erro ao conectar no Servidor MySQL: {e}")


desconectar(conn)
