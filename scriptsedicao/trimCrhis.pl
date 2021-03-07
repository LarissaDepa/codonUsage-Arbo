#!/usr/bin/perl

#DESCRIPTION:   trabalhando com fastas para montar arquivos fastas para alinhamento par a par no mafft

use strict;
use Bio::SeqIO::fastq;
use Bio::Seq::PrimaryQual;


my $usage="\nCommand Line:\n$0 [file lista de fastas]\n\n"; 

my $ref = $ARGV[0]|| die "$usage";


open (LISTA, "$ref");
my $line; my @fastas;
while($line=<LISTA>){
    chomp($line);
    push(@fastas,$line)
}
close LISTA;

foreach my $fasta (@fastas){
    my $count=0;
    my $gapsub1;
    my $gapsub2;
    my $lengthseq;
    my $recov1;
    my $nada;
    my $seqs_inU = Bio::SeqIO->new(-format => 'fasta', -file => "$fasta");
    while((my $seqPU = $seqs_inU->next_seq())){
        my $id = $seqPU->display_id;
        my $seq=$seqPU->seq;
        if ($count==0){
            $seq=~m/^-+/;
            my $gap1=$&;
            $gapsub1=length($gap1); 
            print ("\n$gap1\n");
            $seq=~m/-+$/;
            my $gap2=$&;
            $gapsub2=length($gap2);
            print ("\n$gap2\n");
            $lengthseq=length($seq);
            $recov1=$lengthseq-$gapsub2;    
            $seq=~s/^-+//;
            $seq=~s/-+$//;
            my $out1= Bio::Seq->new(-display_id => $id, -seq => $seq);

            my $out = Bio::SeqIO->new(-format => 'fasta', -file => ">$fasta.1");
            $out->write_seq($out1);
            
        }
        if ($count!=0){
            my $ini=substr $seq, 0, $recov1;
            print ("$ini\n");
            my $only=substr $ini, 0, $gapsub1, $nada;
            print("$only\n");
            print("$ini\n");
            my $out2 = Bio::Seq->new(-display_id => $id, -seq => $ini);
            my $out = Bio::SeqIO->new(-format => 'fasta', -file => ">$fasta.2");
            $out->write_seq($out2);
            system("cat $fasta.1 $fasta.2 > $fasta\_cut.aln");


        }
        $count++;

        
    }
}
