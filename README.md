# Secure File Handling and Encryption Tool

このツールは、ファイルを読み込み、暗号化し、安全な形式で保存および復号化するためのPythonプログラムです。  
暗号化には`cryptography.fernet`モジュールを使用し、`prompt_toolkit`によってユーザーフレンドリーなインターフェースを提供します。  
また、UUID生成を通じてデータの整合性を確認し、安全なファイル処理を実現します。

## 機能概要

1. ファイルを指定して読み込み
2. ファイル内容を暗号化し、pickle形式でシリアライズ
3. UUIDによるファイル整合性チェック
4. 復号後にファイルとして再保存

## 必要なモジュール

次のモジュールが必要です。`requirements.txt`を使用するか、以下のコマンドでインストールしてください。

```bash
pip install prompt_toolkit cryptography colorama
```

## 使用方法

### ステップ1: ファイルの暗号化と保存

1. プログラムを実行し、暗号化するファイルのパスを入力します。
2. メタデータ（UUID、シード、暗号化キー）が自動的に生成され、ファイルのデータが暗号化されます。
3. 保存するファイル名と拡張子を指定し、暗号化されたデータがファイルとして保存されます。

```bash
python encrypt_file.py
```

```plaintext
Please enter the file path: ./example.txt
[i] Loading File.
[i] Creating Code Object.
[i] Creating Metadata.
Please Enter File Name: example_encrypted
Please enter the extension: .b64
[i] Writing to File.
```

この処理が完了すると、`example_encrypted.b64`という名前で暗号化ファイルが保存されます。

### ステップ2: ファイルの復号化と読み込み

1. 暗号化されたファイルを指定して読み込みます。
2. UUIDとシードから生成されたUUIDを比較し、データの整合性を確認します。
3. 復号されたファイルを保存するファイル名を指定します。

```bash
python decrypt_file.py
```

```plaintext
[In] Please enter the file path: ./example_encrypted.b64
[i] Loading File.
[i] Code Analysis.
[In] Please enter a name to save: example_decrypted
[i] Writing...
```

この処理により、暗号化された内容が復号され、`example_decrypted.txt`という名前で保存されます。

## コードの詳細説明

### `encrypt_file.py`

- ファイルを読み込み、暗号化して保存するプロセスを担当。
- ランダムなシードに基づいてUUIDを生成し、整合性チェックに使用。
- Fernet暗号化キーを生成し、ファイル内容を暗号化。

### `decrypt_file.py`

- 暗号化されたファイルを読み込み、復号するプロセスを担当。
- ファイルに埋め込まれたUUIDとシードから生成されたUUIDを比較し、整合性を確認。
- 復号後のファイルを指定された名前で保存。

## ファイル形式

- ファイルはBase64エンコードされた状態で保存され、`.b64`拡張子を使用します。
- 保存時にはメタデータとしてシード、UUID、暗号化キーが含まれます。

## エラーハンドリング

- ファイルの読み込みエラー、ピックルエラー、暗号化・復号化の失敗に対応したエラーメッセージを出力します。
- 例外処理を活用し、問題が発生した際には適切にプログラムが終了します。
