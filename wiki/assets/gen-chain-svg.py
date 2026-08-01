#!/usr/bin/env python3
# Génère le schéma « chaîne de confiance » en 6 langues : chain-of-trust-<lng>.svg
# Panneau sombre autonome (cohérent avec l'app), lisible en thème clair comme sombre.
import os

L = {
 'fr':{'title':'La chaîne de confiance','sub':'De la mesure jusqu’à Bitcoin — vérifiable par quiconque',
   'closed':'Fermé · homologué','open':'Ouvert · public · rejouable',
   's':[('1','Jeu — RAM','Le listener homologué lit le score en mémoire'),
        ('2','Machine','Passeport de session signé (ECDSA P-256, clé matérielle)'),
        ('3','Serveur','Vérifie les règles PUBLIQUES → publié / retenu / refusé'),
        ('4','Index signé','Liste complète des records + empreinte SHA-256 signée'),
        ('5','OpenTimestamps → Bitcoin','Empreinte horodatée : antériorité prouvée, immuable'),
        ('6','Quiconque','Re-vérifie tout dans son navigateur — sans nous faire confiance')],
   'foot':'La sécurité repose sur l’ouvert, jamais sur le secret.'},
 'en':{'title':'The chain of trust','sub':'From measurement to Bitcoin — verifiable by anyone',
   'closed':'Closed · homologated','open':'Open · public · replayable',
   's':[('1','Game — RAM','The homologated listener reads the score from memory'),
        ('2','Machine','Session passport signed (ECDSA P-256, hardware key)'),
        ('3','Server','Checks the PUBLIC rules → published / held / refused'),
        ('4','Signed index','Full record list + signed SHA-256 fingerprint'),
        ('5','OpenTimestamps → Bitcoin','Fingerprint timestamped: priority proven, immutable'),
        ('6','Anyone','Re-verifies everything in their browser — trusting no one')],
   'foot':'Security rests on the open, never on the secret.'},
 'es':{'title':'La cadena de confianza','sub':'De la medición a Bitcoin — verificable por cualquiera',
   'closed':'Cerrado · homologado','open':'Abierto · público · repetible',
   's':[('1','Juego — RAM','El listener homologado lee la puntuación en memoria'),
        ('2','Máquina','Pasaporte de sesión firmado (ECDSA P-256, clave hardware)'),
        ('3','Servidor','Verifica las reglas PÚBLICAS → publicado / retenido / rechazado'),
        ('4','Índice firmado','Lista completa de récords + huella SHA-256 firmada'),
        ('5','OpenTimestamps → Bitcoin','Huella sellada: anterioridad probada, inmutable'),
        ('6','Cualquiera','Re-verifica todo en su navegador — sin confiar en nosotros')],
   'foot':'La seguridad se basa en lo abierto, nunca en el secreto.'},
 'ja':{'title':'信頼の連鎖','sub':'計測から Bitcoin まで — 誰でも検証可能',
   'closed':'非公開 · 認定','open':'公開 · 誰でも再現可能',
   's':[('1','ゲーム — RAM','認定リスナーがメモリからスコアを読む'),
        ('2','端末','セッションパスポートに署名（ECDSA P-256、ハードウェア鍵）'),
        ('3','サーバー','公開ルールを検証 → 公開 / 保留 / 却下'),
        ('4','署名付きインデックス','全記録リスト + 署名付き SHA-256 指紋'),
        ('5','OpenTimestamps → Bitcoin','指紋を刻印：先行性を証明、不変'),
        ('6','誰でも','ブラウザで全てを再検証 — 誰も信用せずに')],
   'foot':'安全性は「秘密」ではなく「公開」に基づく。'},
 'zh':{'title':'信任链','sub':'从测量到 Bitcoin — 任何人皆可验证',
   'closed':'闭源 · 已认证','open':'开放 · 公开 · 可重放',
   's':[('1','游戏 — RAM','认证监听器从内存读取分数'),
        ('2','本机','会话护照签名（ECDSA P-256，硬件密钥）'),
        ('3','服务器','校验公开规则 → 发布 / 保留 / 拒绝'),
        ('4','签名索引','完整记录清单 + 已签名 SHA-256 指纹'),
        ('5','OpenTimestamps → Bitcoin','指纹盖时间戳：证明先后，不可变'),
        ('6','任何人','在浏览器中重新验证一切 — 无需信任我们')],
   'foot':'安全性建立在开放之上，绝不依赖秘密。'},
 'ko':{'title':'신뢰의 사슬','sub':'측정에서 Bitcoin까지 — 누구나 검증 가능',
   'closed':'비공개 · 인증됨','open':'공개 · 누구나 재현 가능',
   's':[('1','게임 — RAM','인증된 리스너가 메모리에서 점수를 읽음'),
        ('2','기기','세션 패스포트 서명 (ECDSA P-256, 하드웨어 키)'),
        ('3','서버','공개 규칙 검증 → 게시 / 보류 / 거부'),
        ('4','서명된 인덱스','전체 기록 목록 + 서명된 SHA-256 지문'),
        ('5','OpenTimestamps → Bitcoin','지문 타임스탬프: 선후 증명, 불변'),
        ('6','누구나','브라우저에서 모든 것을 재검증 — 아무도 믿지 않고')],
   'foot':'보안은 비밀이 아니라 공개에 기반합니다.'},
}

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def svg(d):
    W=860; top=118; gap=132; H=top+gap*6+64
    accents=['#ff9d3c','#2a7de1','#2a7de1','#ffd24a','#f7931a','#39d353']
    parts=[]
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Segoe UI,system-ui,-apple-system,Roboto,sans-serif">')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="#0b1330"/>')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="none" stroke="#26386f"/>')
    parts.append(f'<text x="34" y="48" fill="#eaf0ff" font-size="26" font-weight="800">{esc(d["title"])}</text>')
    parts.append(f'<text x="34" y="76" fill="#9fb0d6" font-size="14.5">{esc(d["sub"])}</text>')
    # rail gauche : frontière de confiance
    railx=40
    parts.append(f'<line x1="{railx}" y1="{top-8}" x2="{railx}" y2="{top+gap*6-40}" stroke="#2c3f78" stroke-width="2"/>')
    for i,(num,t,dd) in enumerate(d['s']):
        y=top+gap*i; ac=accents[i]
        bx=84; bw=W-bx-40; bh=96
        # pastille numéro sur le rail
        parts.append(f'<circle cx="{railx}" cy="{y+bh//2}" r="15" fill="{ac}"/>')
        parts.append(f'<text x="{railx}" y="{y+bh//2+5}" fill="#06121f" font-size="15" font-weight="900" text-anchor="middle">{num}</text>')
        # carte
        parts.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="#0e1838" stroke="#2c3f78"/>')
        parts.append(f'<rect x="{bx}" y="{y}" width="5" height="{bh}" rx="2.5" fill="{ac}"/>')
        parts.append(f'<text x="{bx+22}" y="{y+38}" fill="#eaf0ff" font-size="19" font-weight="800">{esc(t)}</text>')
        parts.append(f'<text x="{bx+22}" y="{y+66}" fill="#a6b6da" font-size="14.5">{esc(dd)}</text>')
        # flèche vers la carte suivante
        if i<5:
            ay=y+bh; parts.append(f'<path d="M{railx} {ay} L{railx} {ay+gap-bh}" stroke="#2c3f78" stroke-width="2"/>')
            parts.append(f'<path d="M{railx-5} {ay+gap-bh-8} L{railx} {ay+gap-bh} L{railx+5} {ay+gap-bh-8}" fill="none" stroke="#2c3f78" stroke-width="2"/>')
    # étiquettes frontière (fermé sur 1, ouvert sur 2-6)
    parts.append(f'<text x="{W-46}" y="{top+18}" fill="#ff9d3c" font-size="12" font-weight="700" text-anchor="end">{esc(d["closed"])}</text>')
    parts.append(f'<text x="{W-46}" y="{top+gap+18}" fill="#39d353" font-size="12" font-weight="700" text-anchor="end">{esc(d["open"])}</text>')
    # pied
    parts.append(f'<text x="{W//2}" y="{H-24}" fill="#63739e" font-size="13.5" font-style="italic" text-anchor="middle">{esc(d["foot"])}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)

here=os.path.dirname(os.path.abspath(__file__))
for lng,d in L.items():
    open(os.path.join(here,f'chain-of-trust-{lng}.svg'),'w',encoding='utf-8').write(svg(d))
    print('écrit chain-of-trust-'+lng+'.svg')
