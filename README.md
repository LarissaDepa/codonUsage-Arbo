
# ibiodados

Este repositório armazena alguns scripts internos para inserção automática de dados biológicos no banco de dados MySQL, esses scripts seguem certos padrões relacionados à localização da coleta de dados.

### Pacotes:
- [pymysql](https://pypi.org/project/PyMySQL/)
- [SeqIO](https://biopython.org/docs/1.75/api/Bio.SeqIO.html)
- [click](https://click.palletsprojects.com/en/7.x/)
- [re](https://docs.python.org/pt-br/3/library/re.html)
- [AlignIO](https://biopython.org/docs/1.75/api/Bio.AlignIO.html)
- [os](https://docs.python.org/pt-br/3/library/os.html?highlight=#module-os)
- [csv](https://docs.python.org/pt-br/3/library/csv.html?highlight=csv#module-csv)
- [collections](https://docs.python.org/pt-br/3/library/collections.html?highlight=collections#module-collections)

### Comandos



|Comando                                      |Uso                              |Descrição
| :---------------------------------------------- | :-------------------------------------- | :----
| **help**        | `command --help`| Ajuda
| **genoma**      | `i_genoma.py [OPTIONS] FILE`  |Insere genomas completos do viprbrc no formato FASTA. 
| **refseq**      | `i_refseq.py [OPTIONS] FILE ` | Insere sequências referências (CDS)-NCBI no formato FASTA.
| **alinhamento** | `i_algn.py [OPTIONS]`|no diretório dos arquivos : python .\i_algn.py --path .  Insere alinhamentos(RefSeq-NCBI x genomas completos-viprbc) e seus ids.
| **códon RNA\DNA**| `i_codon.py [OPTIONS] FILE`| Insere dados sobre códons de DNA e RNA de um arquivo no formato csv.
| **frequência de códons do hospedeiro** | `i_freqhost.py [OPTIONS] FILE`|Insere dados sobre frequência de códons do hospedeiro de um arquivo no formato csv.
| **frequência de genes tRNA** | `i_freqtrna.py [OPTIONS] FILE`| Insere dados sobre frequência de genes de tRNA de um arquivo no formato csv.


#### Exemplo de uso:

 `python3 i_codon.py file.csv`


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
