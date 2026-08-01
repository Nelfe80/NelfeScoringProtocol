# 검증기 호스팅

검증기는 **자기 완결형 HTML 파일**입니다. **누구나, 어디서나 호스팅**할 수 있습니다. 모든
것이 방문자의 브라우저에서 재계산되므로, 호스팅해도 **신뢰가 낮아지지 않습니다** — 방문자가
직접 전부를 재검증합니다.

[GitHub의 팩 →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## `records-viewer/` 팩
| 파일 | 역할 |
|---|---|
| `verify.html` | **검증기**: 브라우저에서 지문을 재계산하고 **ECDSA P-256 서명을 검증**한 뒤 Bitcoin 봉인 상태를 읽음. 서버·빌드·의존성 없음. |
| `mirror.sh` | **영구 스냅샷**(`snapshot/`)을 만듦 — 서명 인덱스, 앵커, 각 `.ots` 증명 — **nelfeplay.com이 사라져도** 기록을 증명 가능하게 유지. |

## 호스팅하기 (30초)
`verify.html`은 그냥 정적 파일입니다:

- **GitHub Pages / Netlify / Cloudflare Pages** — 파일을 올리세요.
- **로컬** — `verify.html`을 열거나 `python3 -m http.server`.
- **오프라인 / 보관** — 먼저 `./mirror.sh`를 실행하고 폴더를 보관.

`nelfeplay.com`의 **공개 API**(CORS 허용)를 읽습니다.

## 두 가지 모드
| 모드 | 하는 일 | 이유 |
|---|---|---|
| **라이브** | 라이브 API 조회 | 설정 없음, 항상 최신 |
| **스냅샷** | 로컬 사본으로 검증(`mirror.sh`) | **검열 저항**: 사이트가 사라져도 동작 |

스냅샷 모드는 “불변”을 **진짜로** 불변으로 만듭니다. 폴더를 보관하는 한 기록은 증명 가능한
채로 남습니다 — 영원히, 우리 없이.

## 자신만의 검증기 만들기
우리 파일조차 필요 없습니다 — API는 **공개·서명**되어 있습니다.

| 엔드포인트 | 반환 |
|---|---|
| `GET /api/v1/scores/index` | 서명 인덱스: `records`, `root`(정규화 행의 SHA-256), `signature`(ECDSA P-256, base64url DER), `issuer_public_key`(SPKI PEM) |
| `GET /api/v1/scores/anchors` | 앵커: `generation`, `root_sha256`, `bitcoin_block`, 시간 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 해당 세대의 `.ots` 증명(base64) |

셋 다 `Access-Control-Allow-Origin: *`를 보냅니다. 검증 알고리즘과 정규화(JCS, RFC 8785)는
이 저장소의 `ref/`에 있습니다.
