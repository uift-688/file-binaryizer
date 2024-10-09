from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.styles import Style
import random
import pickle
import colorama
import sys
import os
import base64
from cryptography.fernet import Fernet

# Init: Variable initialization

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

colorama.init(True)
PathComp = PathCompleter()

# Step1: Requests the input of a file path.

fp = prompt("Please enter the file path: ", completer=PathComp, style=style)

if not os.path.isfile(fp):
    print(colorama.Fore.RED + "[!] This is not a file path format.")
    sys.exit(3)

# Step2: Loading Files.

print(colorama.Fore.LIGHTBLUE_EX + "[i] Loading File.")

try:
    with open(fp, "rb") as fc:
        fd = fc.read()
except (FileNotFoundError, IOError) as e:
    print(colorama.Fore.RED + f"[!] Error: {e}")
    sys.exit(1)

# Step3: Create code AST Tree and Compiled object.

print(colorama.Fore.LIGHTBLUE_EX + "[i] Creating Code Object.")

# Step4: Create metadata.

print(colorama.Fore.LIGHTBLUE_EX + "[i] Creating Metadata.")

seed = random.randint(1, 1000)
integrity = str(generate_uuid4(seed))
Key = Fernet.generate_key()
suite = Fernet(Key)

# Step5: Generate file.

print(colorama.Fore.LIGHTBLUE_EX + "[i] Writing to File.")

random.seed(seed)

# 32バイトのランダムな鍵を生成
key = os.urandom(32)

# 乱数を指定のシードで初期化し、バイト列を生成
key = bytearray(random.getrandbits(8) for _ in range(32))

url_safe_key = base64.urlsafe_b64encode(key).decode('utf-8')

Name = prompt("Please Enter File Name: ", style=style)

Ext = prompt("Please enter the extension: ", completer=WordCompleter([".b64", ".b64f", ".b64d", ".b64b", ".b64o", ".b64obj", ".b64data", ".b64file", ".b64serobj", ".b64mpobj", ".b64sermp", ".b64objmp"]), style=style)

try:
    with open(f"./{Name}{Ext}", "wb") as f:
        f.write(base64.b64encode(pickle.dumps({"Seed": seed, "Key": Fernet(url_safe_key).encrypt(Key), "Source": suite.encrypt(pickle.dumps({"File": fd, "UUID": integrity, "UUIDSeed": seed, "ext": fp.split(".")[-1]}))})))
except pickle.PickleError as e:
    print(colorama.Fore.RED + "[!] Could not package data: {e}")
    sys.exit(1)
