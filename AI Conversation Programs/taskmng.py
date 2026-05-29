import subprocess
import os

# 定义文件路径
base_dir = r'C:\Users\18660\Desktop\00dkuclass\info104\000final'
test_scanner_path = os.path.join(base_dir, 'testScannerTemp.py')
audio2text_path = os.path.join(base_dir, 'audio2text.py')
testapi102_path = os.path.join(base_dir, 'testapi102.py')
text2speech_path = os.path.join(base_dir, 'text2speech.py')

def run_script(script_path, args=None):
    if args is None:
        args = []
    print(f"Running script: {script_path} with args: {args}")
    subprocess.run(['python', script_path] + args)

# 启动 testScannerTemp.py
run_script(test_scanner_path)
print("Finished testScannerTemp.py")

# 启动 audio2text.py
run_script(audio2text_path)
print("Finished audio2text.py")

# 启动 testapi102.py
result = subprocess.check_output(['python', testapi102_path]).decode().strip()
print(f"testapi102.py result: {result}")

# 启动 text2speech.py 并传入 testapi102.py 返回的字符串
run_script(text2speech_path, [result])
print("Finished text2speech.py")