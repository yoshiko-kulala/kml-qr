# kml-qr

KMLを埋め込んだQRコードをスマホで読み取り、KMLファイルに組み立て直して Google Earth アプリに渡す静的Webツールです（GitHub Pages で配信、ビルド不要）。

公開URL: https://yoshiko-kulala.github.io/kml-qr/

## 使い方

1. スマホのブラウザで公開URLを開き、「読み取りを開始」でQRを読む（カメラはHTTPSが必要）
2. 名前・緯度・経度・方位が表示される
3. 「KMLを保存」でKMLをダウンロードし、ファイルを Google Earth で開く。「このKMLを開くURLをコピー」でURL共有もできる

QRの中身は次のどちらかです。
- `<` で始まるKML本文そのもの
- このページのURL（hash付き）

外部サーバへの送信はなく、データはすべて端末内で処理します。

## hash形式

| 形式 | 例 |
|---|---|
| `#k=<base64url(UTF-8のKML)>` | `#k=PD94bWwg...` |
| `#lat=<緯度>&lng=<経度>&h=<方位>&name=<名前>` | `#lat=35.170915&lng=136.881537&h=90&name=%E5%90%8D%E5%8F%A4%E5%B1%8B%E9%A7%85` |

- 座標は WGS84 の10進度、`h` は北=0°の時計回り、`name` はURLエンコードしたUTF-8
- `lat/lng/h` 形式では、Placemark + inline Style（IconStyle の heading と `shapes/arrow.png` アイコン）の最小KMLを組み立てます
- ページを hash 付きで開くと、読み取りなしで即表示します

## QR画像の作成 (tools/make_qr.py)

```
pip install "qrcode[pil]"

# URLモード（デフォルト）: 小さいQRになり、読み取りやすい
python3 tools/make_qr.py --lat 35.170915 --lng 136.881537 --heading 90 --name 名古屋駅 -o nagoya.png

# KMLモード: KML本文をそのままQR化（アプリに依存せず読めるが、QRは大きくなる）
python3 tools/make_qr.py --lat 35.170915 --lng 136.881537 --heading 90 --name 名古屋駅 --mode kml -o nagoya_kml.png
```

`--base-url` でリーダーのURLを変更できます。誤り訂正はM、出力はPNG。QRのバージョンと文字列長を標準出力に表示します（名古屋駅の例: URLモード version 6 / 98文字、KMLモード version 14 / 328文字。URLモードは `--base-url` の長さで変わります）。

## 端末ごとの既知の挙動

- 「Google Earthで開く」(Web Share) ボタンは、iOS・Android の実機で動作しなかったため削除した。KMLは保存して Google Earth で開く
- カメラが使えるのはHTTPSまたはlocalhostのみ。許可が拒否された場合や非対応環境では、画面に原因（エラー名とメッセージ）を表示する
