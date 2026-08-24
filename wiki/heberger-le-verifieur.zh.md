# 自行托管验证器

验证器是一个**自包含的 HTML 文件**。**任何人都能在任何地方托管它** - 由于一切都在访问者
的浏览器中重算，托管它**不会降低信任**：访问者会自行重新验证一切。

[GitHub 上的工具包 →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## `records-viewer/` 工具包
| 文件 | 作用 |
|---|---|
| `verify.html` | **验证器**：在浏览器中重算指纹并**验证 ECDSA P-256 签名**，然后读取 Bitcoin 封印状态。无服务器、无构建、无依赖。 |
| `mirror.sh` | 生成**持久快照**（`snapshot/`）- 签名索引、锚点及每份 `.ots` 证明 - 使记录**即使 nelfeplay.com 消失**也可证明。 |

## 托管它（30 秒）
`verify.html` 只是一个静态文件：

- **GitHub Pages / Netlify / Cloudflare Pages** - 放上文件即可。
- **本地** - 打开 `verify.html`，或 `python3 -m http.server`。
- **离线 / 存档** - 先运行 `./mirror.sh`，保留该文件夹。

它读取 `nelfeplay.com` 的**公开 API**（已启用 CORS）。

## 两种模式
| 模式 | 作用 | 意义 |
|---|---|---|
| **实时** | 查询实时 API | 零配置，始终最新 |
| **快照** | 对本地副本验证（`mirror.sh`） | **抗审查**：即使网站消失也能运行 |

快照模式让“不可变”**真正**成立：只要你保留该文件夹，记录就始终可证明 - 永远，无需我们。

## 构建你自己的验证器
你甚至不需要我们的文件 - API 是**公开且签名**的。

| 端点 | 返回 |
|---|---|
| `GET /api/v1/scores/index` | 签名索引：`records`、`root`（规范化行的 SHA-256）、`signature`（ECDSA P-256，base64url DER）、`issuer_public_key`（SPKI PEM） |
| `GET /api/v1/scores/anchors` | 锚点：`generation`、`root_sha256`、`bitcoin_block`、时间 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 某代的 `.ots` 证明（base64） |

三者都发送 `Access-Control-Allow-Origin: *`。验证算法与规范化（JCS, RFC 8785）位于本仓库
的 `ref/`。
