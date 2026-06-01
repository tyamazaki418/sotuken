import itertools
from Bio import SeqIO
from collections import defaultdict
import csv

def read_fa(filename):
    seq = ""
    for record in SeqIO.parse(filename, "fasta"):
        seq +=str(record.seq).upper()
    return seq

def count_ATGC(sequence):
    kmer_count = defaultdict(int)
    for i in range(0, len(sequence) - 2):
        kmer = sequence[i:i+3]
        if len(kmer) == 3:
            kmer_count[kmer] += 1
    return kmer_count

def all_codons():
    bases = ["A", "T", "G", "C"]
    return [''.join(p) for p in itertools.product(bases, repeat=3)]

def save_csv(counts, filename="counts_3mer_ATGC.csv"):
    codons = all_codons()
    with open(filename,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["codon","count"])
        for codon in codons:
            writer.writerow([codon, counts.get(codon, 0)])



seq = read_fa("./PSTVd300.fa")
counts = count_ATGC(seq)
save_csv(counts)





