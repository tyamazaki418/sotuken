import math
import collections

# 塩基
bases = 'AUGC'

# FASTAファイルのパス
file_path = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/PSTVd300.fa"

def read_fasta_sequences(file_path):
    sequences = []
    current_seq = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):#ヘッダーの>を削除するやつ
                if current_seq:
                    sequences.append(''.join(current_seq).upper())
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append(''.join(current_seq).upper())
    sequences = [''.join(c for c in seq if c in bases) for seq in sequences]
    return sequences

def compute_conditional_weights(sequences):
    # カウント
    counts = collections.Counter()
    for seq in sequences:
        for i in range(len(seq) - 2):#3塩基数える所
            triplet = seq[i:i + 3]
            if set(triplet) <= set(bases):
                counts[triplet] += 1

    # 条件付き確率と重み
    cond_weights = {}
    for prefix in [a + b for a in bases for b in bases]:#先頭2文字
        total = sum(counts[prefix + c] for c in bases if counts[prefix + c] > 0)
        if total == 0:
            continue
        for c in bases:
            count = counts[prefix + c]
            p = count / total if count > 0 else 1e-10  # log(0)回避
            weight = -math.log(p)
            cond_weights[(prefix, c)] = weight

    return cond_weights
#dat変換
def save_cond_weights_to_dat(cond_weights, dat_file):
    with open(dat_file, 'w') as f:
        for (prefix, base), weight in cond_weights.items():
            f.write(f"{prefix} {base} {weight}\n")

if __name__ == "__main__":
    sequences = read_fasta_sequences(file_path)
    cond_weights = compute_conditional_weights(sequences)
    dat_file = 'cond_weights.dat'
    save_cond_weights_to_dat(cond_weights, dat_file)