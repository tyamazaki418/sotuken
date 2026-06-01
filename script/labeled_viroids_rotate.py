from Bio import SeqIO
import os


# ==== ラベルあり配列ID（pbm・ラベル値なし）====
labeled_ids = {
    # Mild
    'AF483470.1', 'EF192393.1', 'EF192394.1',
    'EF580923.1', 'EU879915.1', 'EU879916.1',
    'JQ806338.1', 'KF418767.1', 'KR611355.1',
    'KT987925.1', 'LC388852.1', 'LC388854.1',
    'M25199.1', 'MG450357.1', 'Y09575.1',

    # Moderate
    'AF454395.1', 'KF683200.1', 'KJ857496.1',
    'KR611360.1', 'M88678.1', 'X17268.1',
    'GQ853461.1', 'EU879913.1',

    # Severe
    'AJ634596.1', 'AY518939.1', 'AY532801.1',
    'DD220185.1', 'FR851463.1', 'JX280944.1',
    'U23060.1', 'X58388.1', 'X76846.1',
    'X97387.1', 'Y09383.1',
    'LC523672.1', 'LC523675.1', 'LC523676.1'
}


def dna_walk(seq, base_map):

    x, y = 0, 0
    coords = [(x, y)]
    for base in seq:
        if base in base_map:
            dx, dy = base_map[base]
            x += dx
            y += dy
            coords.append((x, y))
    return coords


def rna_to_dat(input_file, output_dir):
    # 塩基ごとのベクトル
    base_map = {
        'A': (1, 1),
        'T': (-1, -1),
        'G': (1, -1),
        'C': (-1, 1)
    }

    os.makedirs(output_dir, exist_ok=True)

    for seq_record in SeqIO.parse(input_file, "fasta"):
        seq = str(seq_record.seq).upper()
        name = seq_record.id.encode('ascii', 'ignore').decode('ascii')
        n = len(seq)

        is_labeled = name in labeled_ids

        # ===== ラベルあり：環状RNAとして全回転 =====
        if is_labeled:
            for i in range(n):
                rotated_seq = seq[i:] + seq[:i]
                coords = dna_walk(rotated_seq, base_map)

                output_file = os.path.join(
                    output_dir, f"{name}_start{i:03d}.dat"
                )

                with open(output_file, "w", encoding="utf-8") as f:
                    for x, y in coords:
                        f.write(f"{x},{y}\n")

            print(f"[INFO] {name}: {n} circular DNA-walks generated")




# ==== 使用例 ====
input_file = "PSTVd300.fa"
output_dir = "output_350_dat"
rna_to_dat(input_file, output_dir)
