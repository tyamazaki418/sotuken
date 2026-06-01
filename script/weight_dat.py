import csv
import os
from collections import defaultdict
import math
from Bio import SeqIO

def read_fasta(filename):
    seq=""
    for record in SeqIO.parse(filename,"fasta"):
        seq +=str(record.seq).upper()
    return seq

def load_weight(csv_file):
    weights ={}
    with open(csv_file,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kmer = row["3mer"]
            w = float(row["log4_weight"])
            weights[kmer] = w
    return weights

def DNA_walk(seq, weights):
    map ={
        'A': (1,1),
        'T': (-1,-1),
        'G': (1,-1),
        'C': (-1,1)
    }

    n = len(seq)
    x_list = [0.0]
    y_list = [0.0]

    for i in range(n):
        base = seq[i]
        if base not in map:
            continue
        kmer = seq[(i-2)%n] + seq[(i-1)%n] + seq[i]

        w = weights.get(kmer, 1.0)  # 重みが無ければ1.0
        dx, dy = map[seq[i]]
        x_new = x_list[-1] + dx * w
        y_new = y_list[-1] + dy * w
        x_list.append(x_new)
        y_list.append(y_new)

    return x_list, y_list

def save_dat(x_list, y_list, filename="dnawalk.dat"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for x, y in zip(x_list, y_list):
            writer.writerow([x, y])

fasta_file = "PSTVd300.fa"
weights = load_weight("log_weights_3mer.csv")
output_dir = "output_weight_dat"
os.makedirs(output_dir, exist_ok=True)

for record in SeqIO.parse(fasta_file, "fasta"):
    seq = str(record.seq).upper()
    x_list, y_list = DNA_walk(seq, weights)
    filename = os.path.join(output_dir, f"{record.id}.dat")
    save_dat(x_list, y_list, filename)
    print(f"Saved: {filename}")
