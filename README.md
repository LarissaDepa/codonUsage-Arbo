
# codonUsage-Arbo

Este repositório contém arquivos gerados com o estudo da avaliação do uso de códons em infecções virais que utiliza como modelos os arbovírus: DENV, ZIKV, CHIKV.

![Python Version](https://img.shields.io/pypi/pyversions/orfipy)       ![Mysql Version](https://img.shields.io/badge/MySQL-8-blue) ![ubuntu Version](
https://img.shields.io/badge/ubuntu-20.4-orange) 

### bibliotecas:
- [pymysql](https://pypi.org/project/PyMySQL/)
- [SeqIO](https://biopython.org/docs/1.75/api/Bio.SeqIO.html)
- [click](https://click.palletsprojects.com/en/7.x/)
- [re](https://docs.python.org/pt-br/3/library/re.html)
- [AlignIO](https://biopython.org/docs/1.75/api/Bio.AlignIO.html)
- [os](https://docs.python.org/pt-br/3/library/os.html?highlight=#module-os)
- [csv](https://docs.python.org/pt-br/3/library/csv.html?highlight=csv#module-csv)
- [collections](https://docs.python.org/pt-br/3/library/collections.html?highlight=collections#module-collections)
- [pathlib](https://docs.python.org/pt-br/3/library/pathlib.html)
- [statistics](https://docs.python.org/3/library/statistics.html)
- [math](https://docs.python.org/3/library/math.html)



###  inserir_banco

Este diretório armazena alguns scripts que foram utilizados para inserção de dados biológicos num banco de dados MySQL.



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






### Validação
Este diretório armazena scripts que foram utilizados para validação da contagem da frequência de códons e ordenação geradas pelo codonW.
|scripts                                   
| :---------------------------------------------- |
| `count.txt`
| `valid_ordfreq.py `






### Cálculos

Este diretório armazena scripts relacionados aos cálculos do estudo.

|scripts                                   
| :---------------------------------------------- |
| `similaridade.py`
| `media.py`


SIMILARIDADE entre duas espécies a e b  = somatório da freqrelativahumano (especieB) * somatório da freqrelativavirusx (espécie A) / raiz do somatório da freqcodonhumano ao quadrado x somatório da freqcodonrelativavirus ao quadrado
```
Output:
Genoma:  gb:MT636909   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636909  e humano é :  0.9131291564221438
Genoma:  gb:MT636910   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636910  e humano é :  0.9143951531026236
Genoma:  gb:MT636911   RefSeq:  lcl|NC_004162.2_cds_NP_690589.2_2
Similaridade entre  gb:MT636911  e humano é :  0.9139864625759921

```
MÉDIA = média de cada códon para cada vírus(refseq).

```
Output:
A média 139.8363448631905, do códon AAA da refseq lcl|NC_001474.2_cds_NP_056776.2_1
refseq ['lcl|NC_001475.2_cds_YP_001621843.1_1']
 A média 127.64048059149722, do códon AAA da refseq lcl|NC_001475.2_cds_YP_001621843.1_1
refseq ['lcl|NC_001477.1_cds_NP_059433.1_1']
 A média 137.1747572815534, do códon AAA da refseq lcl|NC_001477.1_cds_NP_059433.1_1
refseq ['lcl|NC_002640.1_cds_NP_073286.1_1']
 A média 127.35272727272728, do códon AAA da refseq lcl|NC_002640.1_cds_NP_073286.1_1
refseq ['lcl|NC_004162.2_cds_NP_690588.1_1']
 A média 69.66666666666667, do códon AAA da refseq lcl|NC_004162.2_cds_NP_690588.1_1
refseq ['lcl|NC_004162.2_cds_NP_690589.2_2']
 A média 34.666666666666664, do códon AAA da refseq lcl|NC_004162.2_cds_NP_690589.2_2
refseq ['lcl|NC_012532.1_cds_YP_002790881.1_1']
 A média 78.63503649635037, do códon AAA da refseq lcl|NC_012532.1_cds_YP_002790881.1_1
refseq ['lcl|NC_001474.2_cds_NP_056776.2_1']

```




### Contribuidores

[ <img src="https://avatars.githubusercontent.com/u/28652519?v=4" width="100px; "/><br><sub><b>Crhisllane Vasconcelos</b></sub> ](https://github.com/crhisllane) 

[ <img src="https://avatars.githubusercontent.com/u/41396273?v=4" width="100px; "/><br><sub><b>Larisse Depa</b></sub> ](https://github.com/LarisseDepa)

[ <img src="https://avatars.githubusercontent.com/u/41396490?v=4" width="100px; "/><br><sub><b>Larissa Depa</b></sub> ](https://github.com/LarissaDepa) 
