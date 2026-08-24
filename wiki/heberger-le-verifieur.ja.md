# 検証ツールをホストする

検証ツールは**自己完結型の HTML ファイル**です。**誰でも、どこでもホスト**できます。すべ
ては訪問者のブラウザで再計算されるため、ホストしても**信頼は下がりません** - 訪問者が自分
で全部を再検証します。

[GitHub のパック →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## `records-viewer/` パック
| ファイル | 役割 |
|---|---|
| `verify.html` | **検証ツール**：ブラウザ内で指紋を再計算し **ECDSA P-256 署名を検証**、続いて Bitcoin 封印の状態を読む。サーバー不要・ビルド不要・依存なし。 |
| `mirror.sh` | **恒久スナップショット**（`snapshot/`）を取得 - 署名付きインデックス、アンカー、各 `.ots` 証明 - **nelfeplay.com が消えても**記録を証明可能に保つ。 |

## ホスト方法（30 秒）
`verify.html` は単なる静的ファイルです：

- **GitHub Pages / Netlify / Cloudflare Pages** - ファイルを置くだけ。
- **ローカル** - `verify.html` を開く、または `python3 -m http.server`。
- **オフライン / アーカイブ** - 先に `./mirror.sh` を実行し、フォルダを保管。

`nelfeplay.com` の**公開 API**（CORS 有効）を読みます。

## 2 つのモード
| モード | 内容 | 意義 |
|---|---|---|
| **ライブ** | ライブ API を参照 | 設定ゼロ、常に最新 |
| **スナップショット** | ローカルコピーで検証（`mirror.sh`） | **検閲耐性**：サイトが消えても動作 |

スナップショットモードは「不変」を**本当に**不変にします。フォルダを保管する限り、記録は
証明可能なまま - 永久に、私たち抜きで。

## 自分の検証ツールを作る
私たちのファイルすら不要です - API は**公開・署名済み**です。

| エンドポイント | 返すもの |
|---|---|
| `GET /api/v1/scores/index` | 署名付きインデックス：`records`、`root`（正規化行の SHA-256）、`signature`（ECDSA P-256, base64url DER）、`issuer_public_key`（SPKI PEM） |
| `GET /api/v1/scores/anchors` | アンカー：`generation`、`root_sha256`、`bitcoin_block`、日時 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 世代の `.ots` 証明（base64） |

3 つとも `Access-Control-Allow-Origin: *` を返します。検証アルゴリズムと正規化（JCS,
RFC 8785）は本リポジトリの `ref/` にあります。
