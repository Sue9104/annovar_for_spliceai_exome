# ADD SpliceAI Annotation to Annovar

## WHAT DOES IT DO

annotate spliceai_exome to vcf using annovar, variants with more than one records would be splited into multiple lines.

## PREREQUISITE

- Perl > 5.24
- Python > 3.8
- [Annovar](https://annovar.openbioinformatics.org/en/latest/)
- [SpliceAI](https://github.com/Illumina/SpliceAI): download annotation files

## Usage

- splice_exome vcf to annovar db bed, and build index

```sh
python convert_spliceai_vcf_to_annovar_db.py <spliceai_exome_vcf> <annovar_db_bed>
perl compile_annovar_index.pl <annovar_db_bed> <bin_size> > <annovar_db_bed.idx>
```

> bin_size recommended: 1000
> chromosome should be "1,2..,X,Y"

- annote using annovar
```sh
perl table_annovar.add_spliceai_exome.pl <avinput> <annovar_db> -buildver hg19 -out <outprefix> -protocol <spliceai_exome_db_name> -operation f -nastring . -csvout -polish
```

