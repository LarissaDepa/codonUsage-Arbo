from pathlib import Path
import os

# https://www.youtube.com/watch?v=i7oEQ6FXBTU <-- adaptamos o código de programação dinâmica
# https://github.com/programacaodinamica/mini-projetos/blob/master/src/genes.py
# Input
# ---aaattcc---cccc--
# aactgtgactgcatgcatgactgactg
# Output
# aaattcc---cccc
# tgtgactgcatgcatgactgac


def contar_no_comeco(sequencia):
    '''Conta os - no começo da sequência'''

    tracos = 0
    for c in sequencia:
        if c == '-':
            tracos = tracos + 1
        else:
            break
    return tracos


def contar_no_final(sequencia):
    '''Conta os - no final da sequência '''

    return contar_no_comeco(reversed(sequencia))


def editar_sequencias(seq1, seq2):
    _inicio = contar_no_comeco(seq1)
    _final = contar_no_final(seq1)
    # se o final for 0, precisamos ajustar

    # Sim, podemos retornar duas coisas em Python
    return (seq1[_inicio:-_final if _final != 0 else len(seq1)],
            seq2[_inicio:-_final if _final != 0 else len(seq2)])


def teste():
    '''Este é o teste'''

    seq1 = '---aaattcc---cccc--'
    seq2 = 'aactgtgactgcatgcatgactgactg'

    ed1, ed2 = editar_sequencias(seq1, seq2)
    print(ed1)
    print(ed2)


def encontrar_gb(linhas):
    '''Econtra o índice onda há ">gb" '''

    indice = 0
    for l in linhas:
        if '>gb' in l:
            break
        indice = indice + 1
    return indice


if __name__ == "__main__":
    # abre o arquivo para leitura
    teste()
    path = Path(
        r'\Users\BAHIANA\Downloads\sequenciasnovasalinhadas\chikungunya\copias_CHIKV\SeqAlnEditadas_CHIKV2_copia')
    line_files = path.glob('*.fasta.aln')
    for i in line_files:
        with open(i) as fasta:
            conteudo = fasta.read()
            # dividimos o conteúdo em uma lista nas quebra de linhas
            # equivalente ao readlines()
            linhas = conteudo.split('\n')
            # print(linhas)
            cabecalho1 = linhas[0]
            indice = encontrar_gb(linhas)

            cabecalho2 = linhas[indice]
            # reconstruímos as sequências a partir da lista
            sequencia1 = ''.join(linhas[1:indice])
            sequencia2 = ''.join(linhas[indice+1:])

            # abre um novo arquivo para escrita
        with open(os.path.join('pasta', f'{i}.fasta'), 'w') as res:
            # recebemos as duas sequências editadas retornadas
            editada1, editada2 = editar_sequencias(sequencia1, sequencia2)
            # escreve sequencia editada
            res.write(cabecalho1 + '\n')
            res.write(editada1 + '\n')
            res.write(cabecalho2 + '\n')
            res.write(editada2 + '\n')
            print(cabecalho1, "\n", cabecalho2)
        with open(os.path.join('pasta', f'{i}.cds.fasta'), 'w') as res:
            # recebemos as duas sequências editadas retornadas
            editada1, editada2 = editar_sequencias(sequencia1, sequencia2)
            # escreve sequencia editada
            res.write(cabecalho2 + '\n')
            res.write(editada2 + '\n')
            print(cabecalho1, "\n", cabecalho2)
