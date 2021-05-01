
# codonUsage-Arbo

Este repositório contém arquivos relacionados ao estudo da avaliação do uso de códons em infecções virais utilizando como modelos os arbovírus: DENV, ZIKV, CHIKV.

![Python Version](https://img.shields.io/pypi/pyversions/orfipy)       ![Mysql Version](https://img.shields.io/badge/MySQL-8-blue) ![ubuntu Version](
https://img.shields.io/badge/ubuntu-20.4-orange) 

### Pacotes:
- [pymysql](https://pypi.org/project/PyMySQL/)
- [SeqIO](https://biopython.org/docs/1.75/api/Bio.SeqIO.html)
- [click](https://click.palletsprojects.com/en/7.x/)
- [re](https://docs.python.org/pt-br/3/library/re.html)
- [AlignIO](https://biopython.org/docs/1.75/api/Bio.AlignIO.html)
- [os](https://docs.python.org/pt-br/3/library/os.html?highlight=#module-os)
- [csv](https://docs.python.org/pt-br/3/library/csv.html?highlight=csv#module-csv)
- [collections](https://docs.python.org/pt-br/3/library/collections.html?highlight=collections#module-collections)
- [pathlib](https://docs.python.org/pt-br/3/library/pathlib.html)

###  inserir_banco

Este diretório armazena alguns scripts que foram utilizados para inserção de dados biológicos num banco de dados MySQL.



### Comandos



|Dado                                      |Uso                              |Descrição
| :---------------------------------------------- | :-------------------------------------- | :----
| **help**        | `command --help`| Ajuda
| **genoma**      | `i_genoma.py [OPTIONS] FILE`  |Insere genomas completos do viprbrc no formato FASTA. 
| **refseq**      | `i_refseq.py [OPTIONS] FILE ` | Insere sequências referências (CDS)-NCBI no formato FASTA.
| **alinhamento** | `i_algn.py [OPTIONS]`|no diretório dos arquivos : python .\i_algn.py --path .  Insere alinhamentos(RefSeq-NCBI x genomas completos-viprbc) e seus ids.
| **códon RNA\DNA**| `i_codon.py [OPTIONS] FILE`| Insere dados sobre códons de DNA e RNA de um arquivo no formato csv.
| **frequência de códons do hospedeiro** | `i_freqhost.py [OPTIONS] FILE`|Insere dados sobre frequência de códons do hospedeiro de um arquivo no formato csv.
| **frequência de genes tRNA** | `i_freqtrna.py [OPTIONS] FILE`| Insere dados sobre frequência de genes de tRNA de um arquivo no formato csv.
| **frequência de códons dos vírus** | `i_freqvirus.py [OPTIONS] FILE`| Insere dados sobre frequência de códons dos vírus gerados no codonW.
| **frequência de códons do hospedeiro** | `i_freqhostnovo.py [OPTIONS] FILE`|Insere dados sobre frequência de códons do hospedeiro de um arquivo no formato csv e calcula a frequência relativa
| **similaridade** | `i_similaridade.py`| Insere dados sobre cálculos de similaridade.

#### Exemplo de uso:

Input:

 `$ caminho-arquivo.py/   python3 arquivo.py   caminho-arquivo-ou-pasta/file`


output:

```MySQL
+-----------+-----------+----------+----------------+-------------+
| PK_codons |  codonRNA | codonDNA | nomeAminoacido |  abrev_aa   |
+-----------+-----------+------+---+----------------+-------------+
|     1     |     AAA   |     AAA  |     Lisina     |     Lys     | 
|     2     |     AAG   |     AAG  |     Lisina     |     Lys     |
|     3     |     AAC   |     AAC  |    Asparagina  |     Asn     |
|     ...   |     ...   |     ...  |     ...        |     ...     |
+-----------+-----------+----------+----------------+-------------+
```




### Edição

Este diretório armazena alguns scripts que foram utilizados para edição de sequências de genomas completos dos vírus alinhadas com as cds referência do vírus.

|scripts                                   
| :---------------------------------------------- |
| `trimCrhis.pl`
| `trimHallz.py`
| `trimcds.py`


#### Exemplo de uso:

```
Input:
---aaattcc---cccc--
aactgtgactgcatgcatgactgactg
-----------------------------------
Output:
aaattcc---cccc
tgtgactgcatgcatgactgac

```
### Cálculos
|scripts                                   
| :---------------------------------------------- |
| `similaridade.py`

1.0	SIMILARIDADE entre duas espécies a e b  = somatório da freqrelativahumano (especieB) * somatório da freqrelativavirusx (espécie A) / raiz do somatório da freqcodonhumano ao quadrado x somatório da freqcodonrelativavirus ao quadrado
```
Output:
Genoma:  gb:MT636909   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636909  e humano é :  0.9131291564221438
Genoma:  gb:MT636910   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636910  e humano é :  0.9143951531026236
Genoma:  gb:MT636911   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636911  e humano é :  0.9139864625759921

```



### Colaboradores
