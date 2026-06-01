# icogen

macOS アプリアイコン用の PNG を一括生成する CLI ツール。  
1024×1024 の元画像から Apple 規定の 10 サイズを一発で出力します。

## 必要なもの

- Python 3.8+
- [Pillow](https://pillow.readthedocs.io/)

### Pillow のインストール

```bash
# pip
pip install Pillow

# uv
uv pip install Pillow
# または依存関係として追加する場合
uv add Pillow
```

## インストール不要で今すぐ使う

```bash
# 1. Pillow を入れる（上記参照）

# 2. curl で実行（YOUR_IMAGE.png を対象ファイルに変えてください）
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/icogen/main/icogen.py \
  | python3 - YOUR_IMAGE.png
```

オプションを渡すときは `python3 -` の後にそのまま続けます：

```bash
# 出力先を指定
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/icogen/main/icogen.py \
  | python3 - YOUR_IMAGE.png -o ./MyApp.iconset

# .icns も生成（macOS 限定）
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/icogen/main/icogen.py \
  | python3 - YOUR_IMAGE.png --icns -v
```

> **Note** `curl | python3 -` の `-` は「標準入力からスクリプトを読む」Python の構文です。  
> スクリプトをダウンロードせずにその場で実行できます。

## ローカルで使う

```bash
# ダウンロード
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/icogen/main/icogen.py -o icogen.py

# 実行権限を付けてどこからでも呼べるようにする（オプション）
chmod +x icogen.py
sudo mv icogen.py /usr/local/bin/icogen

# 使い方
icogen YOUR_IMAGE.png
```

## 使い方

```
usage: icogen [-h] [-o OUTPUT] [--icns] [-v] [--list] [source]
```

| オプション | 説明 |
|---|---|
| `source` | 元画像（PNG 推奨、最低 1024×1024） |
| `-o OUTPUT` | 出力ディレクトリ（デフォルト: `./icons/`） |
| `--icns` | `.icns` ファイルも生成（macOS の `iconutil` が必要） |
| `-v` | 生成ファイルを 1 つずつ表示 |
| `--list` | 生成されるサイズ一覧を表示して終了 |

### 例

```bash
# 基本
python icogen.py AppIcon.png

# 出力先を指定してverbose
python icogen.py AppIcon.png -o ./MyApp.iconset -v

# .icns まで一括生成（macOS のみ）
python icogen.py AppIcon.png --icns

# 生成されるファイル一覧を確認
python icogen.py --list
```

## 出力ファイル

Apple の命名規則に従った 10 ファイルを生成します。

| ファイル名 | 論理サイズ | 実ピクセル |
|---|---|---|
| `icon_16x16.png` | 16×16 | 16×16 |
| `icon_16x16@2x.png` | 16×16 @2x | 32×32 |
| `icon_32x32.png` | 32×32 | 32×32 |
| `icon_32x32@2x.png` | 32×32 @2x | 64×64 |
| `icon_128x128.png` | 128×128 | 128×128 |
| `icon_128x128@2x.png` | 128×128 @2x | 256×256 |
| `icon_256x256.png` | 256×256 | 256×256 |
| `icon_256x256@2x.png` | 256×256 @2x | 512×512 |
| `icon_512x512.png` | 512×512 | 512×512 |
| `icon_512x512@2x.png` | 512×512 @2x | 1024×1024 |

## .icns の生成（macOS のみ）

`--icns` フラグを付けると `iconutil` を呼び出して `.icns` ファイルも生成します。

```bash
python icogen.py AppIcon.png --icns -o ./output
# → ./output/AppIcon.iconset/ （PNG 群）
# → ./output/AppIcon.icns
```

macOS 以外の環境では PNG のみ生成され、手動実行コマンドが表示されます：

```
iconutil -c icns "AppIcon.iconset"
```

## 元画像のガイドライン

- **フォーマット**: PNG（透過対応）推奨
- **サイズ**: 最低 1024×1024px（推奨）
- **形状**: 正方形。非正方形の場合は警告を出して引き伸ばします

## ライセンス

MIT