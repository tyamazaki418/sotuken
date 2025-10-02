import os
import numpy as np

# ファイルパス (PyCharmで編集して実際のパスに置き換え)
file_path = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/PSTVd300.fa"
weights_file = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/cond_weights.dat"
output_folder = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/output_dat"
os.makedirs(output_folder, exist_ok=True)

# 各塩基に割り当てたベクトル
base_vectors = {
    'A': np.array([1.0, 1.0]),
    'C': np.array([1.0, -1.0]),
    'G': np.array([-1.0, 1.0]),
    'U': np.array([-1.0, -1.0])
}

def read_fasta_sequences(file_path):#fastaの名前抽出
    sequences = []
    names = []
    current_seq = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append(''.join(current_seq).upper())
                    current_seq = []
                names.append(line[1:].split()[0])
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append(''.join(current_seq).upper())
    sequences = [''.join(c for c in seq if c in 'AUGC') for seq in sequences]
    return names, sequences

def load_cond_weights_from_dat(weights_file):
    cond_weights = {} #辞書の初期化
    with open(weights_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                prefix = parts[0]
                base = parts[1]
                weight = float(parts[2])#重みをfloatに変換
                cond_weights[(prefix, base)] = weight
    return cond_weights

def generate_coordinates(sequences, cond_weights, image_size=64):
    all_coordinates = [] #配列の座標列格納
    start_pos = np.array([image_size / 2, image_size / 2])  # 中心
    for seq in sequences:
        pos = start_pos.copy()
        coordinates = [pos.copy()]
        for i in range(2, len(seq)):
            prefix = seq[i - 2:i] #直前2塩基
            base = seq[i] #現在の塩基
            w = cond_weights.get((prefix, base), 0.0) #辞書から重みを読み込む
            alpha = w / (w + 1) if w > 0 else 0.5
            vec = base_vectors.get(base, np.array([0.5, 0.5]))
            pos = pos * (1 - alpha) + vec * alpha
            coordinates.append(pos.copy())
        # 64x64のスケーリング
        coords = np.array(coordinates)#中心からのずれ
        max_coord = np.max(np.abs(coords - start_pos))
        if max_coord > 0:
            coords = (coords - start_pos) * (image_size / 2 / max_coord) + start_pos
        all_coordinates.append(coords)
    return all_coordinates

def save_coordinates_to_dat(names, coordinate_data, output_folder):
    for name, coords in zip(names, coordinate_data):
        safe_name = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)
        output_file = os.path.join(output_folder, f"{safe_name}.dat")
        with open(output_file, 'w') as f:
            for coord in coords:
                f.write(f"{coord[0]},{coord[1]}\n")


if __name__ == "__main__":
    names, sequences = read_fasta_sequences(file_path)
    cond_weights = load_cond_weights_from_dat(weights_file)
    coords = generate_coordinates(sequences, cond_weights, image_size=64)
    save_coordinates_to_dat(names, coords, output_folder)