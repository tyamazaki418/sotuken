from Bio import SeqIO
import os


def rna_to_dat(input_file, output_dir):
    # 塩基ごとのベクトル
    base_map = {
        'A': (1, 1),
        'T': (-1, -1),
        'G': (1, -1),
        'C': (-1, 1)
    }

    os.makedirs(output_dir, exist_ok=True)

    # 入力FASTAをUTF-8で明示的に読み込み
    for seq_record in SeqIO.parse(input_file, "fasta"):
        seq = str(seq_record.seq).upper()
        name = seq_record.id.encode('ascii', 'ignore').decode('ascii')

        x, y = 0, 0
        coordinate = [(x, y)]  # 初期座標(0,0)

        for base in seq:
            if base in base_map:
                dx, dy = base_map[base]
                x += dx
                y += dy
                coordinate.append((x, y))

        # FASTAファイルの名前をつける
        output_file = os.path.join(output_dir, f"{name}.dat")


        with open(output_file, "w", encoding='utf-8') as f:
            for cx, cy in coordinate:
                line = f"{cx},{cy}\n"
                f.write(line)

        with open(output_file, 'rb') as f_check:
            content = f_check.read()
            if any(b > 127 for b in content):
                print(f"[WARN] Non-ASCII bytes in {output_file}! Manual cleanup needed.")
            else:
                print(f"[OK] {output_file} is pure ASCII.")

        print(f"[INFO] {output_file} に {len(coordinate)} 点の座標を保存しました。")


# 使用例
input_file = "PSTVd300.fa"
output_dir = "output_dat"
rna_to_dat(input_file, output_dir)