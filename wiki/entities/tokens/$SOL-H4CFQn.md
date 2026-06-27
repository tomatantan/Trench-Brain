---
type: entity
kind: token
source: auto-track
status: dead
ticker: $SOL (pump.fun clone)
mint: H4CFQnSz3yjapiB6Z3qAoVH6MguggitXbyoGsgf4pump
created: 2026-06-26
updated: 2026-06-27 (DEAD確定・peak$258k→$22,805/-91.2%・BUphiK需要逆転後崩壊)
tags: [token, pumpfun, graduated, traction0, ai-memes, external-event, multi-mint-wave, tokenized-agent]
---

# $SOL-H4CFQn — GPT-5.6 Sol（H4CFQn）

pump.fun 発。bonding curve 卒業済（complete=true）。OpenAI GPT-5.6 Sol 発表に便乗した multi-mint wave の主体 mint（$212k・最高 mcap）。website は実在の openai.com URL を使用（association marketing）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | H4CFQnSz3yjapiB6Z3qAoVH6MguggitXbyoGsgf4pump |
| name | GPT-5.6 Sol |
| 初検知 mcap | $212,258（2026-06-26T17:07Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし（kol_ticker:RookieXBT は $SOL=Solana 本体ティッカーと被るため noise） |
| twitter | https://x.com/ShabbatMonster/status/2070553974881624160（@ShabbatMonster） |
| website | https://openai.com/index/previewing-gpt-5-6-sol/（OpenAI 公式 URL 借用） |
| tokenized_agent | true（pump.fun フラグ） |
| real_sol | 0 |
| pool_address | CNjhgsu8vYTxnYo4aqg6fNguEMMbXCsa1JGofyJCaPd3 |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|----|-----------|------|------|
| birth(17:07Z) | $212,258 | — | wave 5本同時発射の最高 mcap。reply:0・KOL CA未確認。 |
| change(17:39Z) | **$130,668** | **-49%**（prev $258,297） | BUphiK が $522k に急騰する中、本 mint は下落。波内需要が BUphiK に移行中。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun bonding curve 卒業・$212,258（同波 5mint 中最高）。
- website = openai.com/index/previewing-gpt-5-6-sol/ — 実在する OpenAI 公式 URL を deployer が設定（association marketing）。
- twitter = @ShabbatMonster のツイート（OpenAI 公式でなく個人アカウント）。
- kol_ticker: RookieXBT — ⚠️ $SOL ティッカーは Solana 本体と同一のため全 KOL のツイートが拾われる noise。kol_ca ゼロ＝CA 確認された KOL 言及なし。
- tokenized_agent=true（pump.fun フラグ）・real_sol=0。
- 同時発射 mint: BUphiK($25k)・B7nXgG($1.8k・即死)・3xH5of($7.5k・即死)・F37vBz($4k・即死)＝5本同時のコピー乱立。

**判断（birth時）**:
- OpenAI GPT-5.6 Sol（Solana との統合？）という外部イベント便乗＝[[external-event-to-token-pattern]] の典型。
- $212k は wave 主体 mint として機能しており、他4本の下位 mint は需要が分散/即死。
- tokenized_agent フラグは pump.fun の分類で、実際に AI agent として機能するわけではない——[[ai-memes]] 命名バイアスの一種。
- association marketing: 実在 openai.com URL 使用で信頼感を演出するが kol_ca ゼロ・reply ゼロ。
- ⚠️ [[rug-anatomy]] 赤旗: real_sol=0 × traction0 × association marketing。BREAKOUT-then-dead 候補。
- 次窓で KOL CA 確認・reply 増加がなければ graduated-but-empty 型崩壊へ。

**17:39Z 更新（-49%）**: $258,297→$130,668（-49%）。
- 同波 BUphiK が $65k→$522k（+702%）に急騰する中、本 mint が半値割れ——波内の需要が BUphiK に移行している構図。
- ⚠️ 主体 mint から 2nd mint への需要移行は異常（通常は主体に集中）。deployer が BUphiK に流動性を集中させている可能性。
- traction（reply/KOL CA）ゼロ継続。自然な需要分散でなく人為的操作の疑い。

**DEAD確定（2026-06-27）**: peak $258,297 → last $22,805（-91.2%）。
- cause: mcap -90% from peak。BUphiK への需要移行後、主体 mint も崩壊で完結。
- external-event 便乗（OpenAI GPT-5.6 Sol）× association marketing（openai.com URL借用）× multi-mint wave主体 mint → peak $258k → -91.2% 崩壊。
- T3（reply/KOL CA）ゼロ全期間——「外部イベント命名 × 権威 URL 借用」は organic traction に転換しない事例 N追加。
- outcome: died。[[external-event-to-token-pattern]] / [[rug-anatomy]]（association marketing崩壊型確定）

<!-- synthesis:end -->

## 関連
- [[external-event-to-token-pattern]]（OpenAI 発表便乗・association marketing）
- [[ai-memes]]（tokenized_agent フラグ・AI テーマ命名）
- [[launchpad-economics]]（graduated・$212k・multi-mint wave）
- [[rug-anatomy]]（real_sol 0・traction0・association marketing 赤旗）
- [[$SOL-BUphiK]]（同波 2nd mint・BREAKOUT）
