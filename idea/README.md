# idea/ — 流用できる関数ネタ集

YAJUscan由来の「使えそうな部品」を、説明付き・小分けの**単体関数**でまとめた所。
チームで好きなものを拾って移植 or そのまま import。依存は最小（`fetch` だけ）。ESM。

## 入ってる関数
| ファイル | 役割 | 重さ |
|---|---|---|
| `holderConcentration.js` | **ホルダー取得**：top1/top10集中度（`getTokenLargestAccounts`＋総供給、LP/pool除外が肝） | 軽（無料RPC） |
| `scamFilter.js` | **スキャム**：rug/mint権限/freeze/LP薄/top10集中/流動性 の閾値判定（純関数） | 軽 |
| `relatedWallets.js` | **連結**：各ウォレットの資金源(funder)を辿って繋ぐ | 重（履歴） |
| `walletCluster.js` | **クラスター**：連結結果をfunderで束ねる→偽分散/バンドル疑い（純関数） | 軽（前段が重い） |
| `bundleDetect.js` | **バンドル**：launch近接ブロックの一斉取得を検出 | 重（履歴） |
| `rpcFailover.js` | **RPC基盤**：複数無料RPCをfailover＋重い履歴メソッドはPublicNode優先(method-aware)。上記が内部で使用 | — |

## 使う順序の考え方（重要）
**安い→高い**で段階的に絞る。重い処理（連結/クラスター/バンドル＝履歴依存）は **最後の篩** で少数にだけ回す：
1. 軽い足切り（ホルダー集中度・スキャム）で 多数→数個
2. **残った数個にだけ** 連結→クラスター／バンドルを当てる（偽分散を暴く）

理由：履歴系を100件に回すと無料RPCが即死＆遅い。絞ってから当てるのが正解。

## 注意
- `getTokenLargestAccounts` は上位20まで（RPC仕様）。memecoin選別なら実用十分。完全分布は有料API。
- 連結/バンドルは取引履歴が必要＝無料RPCだと精度頭打ち（YAJUscanの学び）。本格運用は有料RPC、or YAJUscanの実物に差し替え。
- 集中度・クラスターは **LP/プール/dev/CEX を除外してから** 出す。
