# NelfePlay — 认证复古计分

**记录并排名复古游戏的*真实*分数，任何人皆可验证 —— 服务器既不持有 ROM 也不持有模拟器。**

[认证记录 →](records.md){ .md-button .md-button--primary }
[验证分数 →](https://nelfeplay.com/verify/){ .md-button }

![](assets/chain-of-trust-zh.svg)

## 一句话原则
> **规则与验证公开且可重放**。**内存测量**由一个**已认证、已签名、有版本、经审计**的
> **专有监听器**完成。

## 公开的内容（本仓库）
**护照格式**（`schemas/`）· **验证算法**（`ref/`，多语言 *CoreVerifier*）· **已签名的配置
文件**（`manifest/`）· 可重放的**测试向量**（`vectors/`）· **拒绝码**、**排名规则** 与
**Bitcoin 锚定**证明。

## 无需信任我们即可验证
1. **签名** —— 每份护照对其规范形式（JCS, RFC 8785）签名（ECDSA P-256）。
2. **向量** —— 对 `vectors/*` 运行公开验证器：与我们相同的裁决。
3. **先后性** —— 每个分数都通过 **OpenTimestamps 锚定于 Bitcoin**。

## 深入了解
- [认证记录 —— 全过程](records.md)
- [透明度：何为开放，何为不开放](transparence.md)
- [亲自验证一个分数](verifier-un-score.md)
- [自行托管验证器](heberger-le-verifieur.md)
- [监听器认证](homologation.md)
