from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.styles import Style
import random
import pickle
import colorama
from cryptography.fernet import Fernet
import os
import base64
import sys

# Init: Variable initialization

style = Style(
    [
        ('', 'bg:#000000 fg:#ffffff'),  # デフォルトのスタイル
        ('prompt', 'bg:#1e1e1e fg:#00ff00 bold'),  # プロンプトのスタイル
        ('input', 'bg:#1e1e1e fg:#ffffff'),  # 入力エリアのスタイル
        ('completion-menu', 'bg:#1e1e1e fg:#ffffff'),  # 補完メニューのスタイル
        ('completion-menu.selected', 'bg:#00ff00 fg:#000000'),  # 選択された補完のスタイル
        ('hint', 'fg:#888888'),  # ヒントの色
        ('cursor', 'fg:#00ff00'),  # カーソルの色
    ]
)

def generate_uuid4(seed):
    random.seed(seed)
    
    # 128ビットのランダム値を生成
    random_bits = random.getrandbits(128)
    
    # UUIDのバージョンを「0100」に設定 (バージョン4)
    random_bits = (random_bits & ~(0xf << 76)) | (0x4 << 76)
    
    # UUIDのバリアントを「10」に設定 (RFC 4122 variant)
    random_bits = (random_bits & ~(0x3 << 62)) | (0x2 << 62)
    
    # フォーマットをUUID形式に変換
    uuid = '{:032x}'.format(random_bits)
    return '{}-{}-{}-{}-{}'.format(
        uuid[:8],
        uuid[8:12],
        uuid[12:16],
        uuid[16:20],
        uuid[20:]
    )

colorama.init(True) # AUTO-Resetをオンにして初期化する
PathComp = PathCompleter() # パス補完クラスを初期化する

# Step1: Requests the input of a file path.
fp = prompt("[In] Please enter the file path: ", completer=PathComp, style=style)

if not os.path.isfile(fp): # Fileがパスであるかを確認する
    print(colorama.Fore.RED + "[!] This is not a file path format.")
    sys.exit(3)

# Step2: Loading Files.
print(colorama.Fore.LIGHTBLUE_EX + "[i] Loading File.")
try:
    with open(fp, "rb") as fc:
        Obejects = pickle.loads(base64.b64decode(fc.read())) # ファイルを読み込んで、b64デコードをし、そのデータをpickleでロードする
except (FileNotFoundError, IOError) as e:
    print(colorama.Fore.RED + f"[!] Error: {e}")
    sys.exit(1)
except (pickle.UnpicklingError, ValueError) as e:
    print(colorama.Fore.RED + "[!] Error: Invalid file format.")
    sys.exit(1)

# Step3: Code Analysis.
print(colorama.Fore.LIGHTBLUE_EX + "[i] Code Analysis.")

seed = Obejects["Seed"]

random.seed(seed)

# 乱数を指定のシードで初期化し、バイト列を生成
key = bytearray(random.getrandbits(8) for _ in range(32)) # キーの元をシードに基づいて生成する

url_safe_key = base64.urlsafe_b64encode(key).decode('utf-8') # 生成したキーの元をURL-Safeとしてb64エンコードする

Key = Fernet(url_safe_key).decrypt(Obejects["Key"]) # 生成したキーを使用して全体のソースコードのキーを復号化する

try:
    Sources = pickle.loads(Fernet(Key).decrypt(Obejects["Source"])) # 復号化したキーを元にソースコードを復号化してpickleでロードする
except pickle.UnpicklingError as e:
    print(colorama.Fore.RED + f"[!] Could not extract data: {e}")
    sys.exit(1)
Data = Sources["File"]
UUID = Sources["UUID"]
Seed = Sources["UUIDSeed"]
Ext = Sources["ext"]

if UUID != generate_uuid4(Seed): # 含まれているUUIDとシードから生成したUUIDを比較して整合性を確認する
    print(colorama.Fore.RED + "[!] file integrity error.")
    sys.exit(1)

# Step4: Confirmation of consistency.

FN = prompt("[In] Please enter a name to save: ")

print(colorama.Fore.LIGHTBLUE_EX + "[i] Writing...")

with open(f"./{FN}.{Ext}", "wb") as f:
    f.write(Data)
