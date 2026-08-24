# NelfePlay - 인증 레트로 스코어링

**레트로 게임의 *진짜* 점수를 기록·순위 매기고 누구나 검증 가능 - 서버는 ROM도 에뮬레이터도
갖지 않습니다.**

[인증된 기록 →](records.md){ .md-button .md-button--primary }
[점수 검증 →](https://nelfeplay.com/verify/){ .md-button }

![](assets/chain-of-trust-ko.svg)

## 한 문장 원칙
> **규칙과 검증은 공개·재현 가능**. **메모리 측정**은 **인증·서명·버전 관리·감사**된
> **독점 리스너**가 수행.

## 공개되는 것 (이 저장소)
**패스포트 형식**(`schemas/`) · **검증 알고리즘**(`ref/`, 여러 언어의 *CoreVerifier*) ·
**서명된 프로필**(`manifest/`) · 재현 가능한 **테스트 벡터**(`vectors/`) · **거부 코드**,
**순위 규칙**, **Bitcoin 앵커링** 증명.

## 우리를 믿지 않고 검증
1. **서명** - 각 패스포트는 정규형(JCS, RFC 8785)에 서명(ECDSA P-256).
2. **벡터** - `vectors/*`에 공개 검증기 실행: 우리와 동일한 판정.
3. **선후성** - 각 점수는 **OpenTimestamps로 Bitcoin에** 앵커.

## 더 알아보기
- [인증된 기록 - 전체 프로세스](records.md)
- [투명성: 무엇이 공개이고 무엇이 아닌가](transparence.md)
- [직접 점수 검증](verifier-un-score.md)
- [검증기 호스팅](heberger-le-verifieur.md)
- [리스너 인증](homologation.md)
