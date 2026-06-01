import csv
from collections import defaultdict
import math


def load_3mer_count(csv_file):
    counts = {}
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kmer = row["codon"]
            cnt = int(row["count"])
            counts[kmer] = cnt
    return counts


def sum_2mer(counts):
    prefix_sum = defaultdict(int)
    for kmer, cnt in counts.items():
        prefix = kmer[:2]
        prefix_sum[prefix] += cnt
    return prefix_sum



def conditional_probability(counts):
    prefix_sum = sum_2mer(counts)
    cond_prob = {}

    for kmer, cnt in counts.items():
        prefix = kmer[:2]
        # その prefix（例：GC）に続く全ての 3mer の合計
        total = prefix_sum[prefix]
        p = (cnt + 1) / (total + 4)
        cond_prob[kmer] = p

    return cond_prob


def convert_to_log_weights(cond_prob):
    weights = {}
    for kmer, p in cond_prob.items():
        weights[kmer] = -math.log2(p)/2
    return weights


def save_csv(weights, filename="log_weights_3mer.csv"):
    with open(filename,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["3mer","log4_weight"])
        for kmer, w in sorted(weights.items()):
            writer.writerow([kmer, w])


counts = load_3mer_count("counts_3mer_ATGC.csv")
cond_prob = conditional_probability(counts)
weights = convert_to_log_weights(cond_prob)
save_csv(weights)
