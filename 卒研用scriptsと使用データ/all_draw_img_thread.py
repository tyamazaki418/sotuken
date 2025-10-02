import os
import subprocess
import time
#スレッドプールを管理し、複数のタスクを並列に実行するためのやつ
from concurrent.futures import ThreadPoolExecutor

input_file = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/output_dat"
output_base_directory = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/output_PSTVd300_data"
draw_img_script = "C:/Users/torat/Documents/ゼミ/sample/pythonProject1/.venv/Scripts/draw_img.py"

python_executable = "C:/Users/torat/Downloads/projects/saigen/.venv/Scripts/python.exe"

width = 64  # 画像横サイズ
height = 64  # 画像縦サイズ
start_time = time.time() #実行時間

# draw_img.pyを実行するための関数
def run_draw_img(width, height, data_file, output_file):
    try:
        with open(output_file, 'w') as out_file:
            result = subprocess.run(
                [python_executable, draw_img_script, str(width), str(height), data_file],
                stdout=out_file,
                stderr=subprocess.PIPE,
                text=True
            )
        if result.returncode != 0: # subprocessが正常に終了すると0が出力される
            print(f"Error occurred: {result.stderr}") # エラーメッセージが出力された場合、内容が result.stderr に格納される
        #else:
            #print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")

# 処理を実行する関数
def process_dat_file(dat_file):
    family_name = os.path.basename(os.path.dirname(dat_file))
    output_directory = os.path.join(output_base_directory, family_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pbm_file_name = os.path.splitext(os.path.basename(dat_file))[0] + ".pbm"
    pbm_file = os.path.join(output_directory, pbm_file_name)

    run_draw_img(width, height, dat_file, pbm_file)

# ディレクトリを再帰的に探索して、すべての .dat ファイルを処理
dat_files = []
for root, _, files in os.walk(input_file):
    for file in files:
        dat_file = os.path.join(root, file)
        dat_files.append(dat_file)

# スレッドプールの最大スレッド数を指定
max_workers = 1 #CPUが12スレッドだったので

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_dat_file, dat_files) #リストに対して並列に関数を適用する

end_time = time.time()
elapsed_time = end_time - start_time
print("All files have been processed.")
print(f"プログラムの実行時間: {elapsed_time:.2f}秒")
