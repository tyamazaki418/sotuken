import os
import main
import time


#ファイルパス
python_executable = ""
draw_img_script = "draw_img.py"
dat_folder = ""
output_folder = ""
img_x, img_y = 64,64  # 画像サイズ
start_time = time.time()

os.makedirs(output_folder, exist_ok=True)


#draw_img.py を呼び出すやつ
def run_draw_img(width, height, data_file, output_file):
    try:
        with open(output_file, 'w') as out_file:
            result = subprocess.run(
                [python_executable, draw_img_script, str(width), str(height), data_file],
                stdout=out_file,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'

            )
        if result.returncode != 0:
            print(f"{data_file}でエラー:\n{result.stderr}")
        else:
            print(f"{output_file}を出力")
    except Exception as e:
        print(f"{data_file}でエラー： {e}")


# フォルダ内の座標データの処理
for fname in os.listdir(dat_folder):
    if fname.endswith(".dat"):
        data_file = os.path.join(dat_folder, fname)
        output_file = os.path.join(output_folder, fname.replace(".dat", ".pgm"))
        run_draw_img(img_x, img_y, data_file, output_file)
end_time = time.time()
