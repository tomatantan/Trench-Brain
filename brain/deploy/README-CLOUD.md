# serving層のクラウド移設（trenchbrain.fun を家から独立させる）

> 2026-07-08 incident: Windows端末死→Cloudflare 1033→サイト全落ち＋cron pushも7/4から停止していた。
> 根治＝**servingを常時稼働クラウドVMへ**。家（Windows/Mac）は合成専任＝死んでも「賢くなるのが遅れる」だけでサービスは不死。

## アーキテクチャ（移設後）
```
GHA(cloud)        : X収集 → git push          （既存・独立）
家 Windows        : 合成(claude)/live_pulse → git push （既存・止まっても serving 無傷）
クラウドVM(新)     : git pull(15分毎) → ui_server(read-only) + /api/ask(gemini $0)
                    → cloudflared named tunnel → trenchbrain.fun
```

## 本人がやる3つ（1回だけ）
1. **Oracle Cloud** always-free VM 作成（Ampere A1・Ubuntu 22.04/24.04・4OCPU/24GBまで無料）。
   SSH公開鍵はClaude(Mac)が渡すものを登録。パブリックIPを Claude に送る。
2. **Cloudflare dashboard** → Zero Trust → Networks → Tunnels → Create tunnel（名前: trenchbrain）
   → 表示される **token**（`eyJ...`の長い文字列）を Claude に送る
   → 同画面の Public Hostname に `trenchbrain.fun` → `HTTP://localhost:8000` を追加。
3. **GEMINI_API_KEY**（aistudio.google.com で無料発行）を Claude に送る（既にあれば流用）。

## Claude がやる（SSHで）
```bash
# repo の read-only deploy key は gh CLI で登録済み（VM専用・書込不可）
sudo GIT_DEPLOY_KEY_B64=... TUNNEL_TOKEN=... GEMINI_API_KEY=... [TWITTERAPI_KEY=...] \
     bash brain/deploy/bootstrap_vm.sh
```
検証: `/api/health` 200・`/api/ask` が4見出し構造・tunnel経由で `https://trenchbrain.fun` 200。

## 移設後の家side変更
- Windows serve wrapper の cloudflared（quick tunnel）は不要になる＝止めてよい（ui_serverはローカル用に残しても可）。
- Windows は cron_collect.sh（収集pull/合成/push）専任。**pushが止まってないかの監視**が今後の要（7/4-7/7の3日停止を検知できてなかった）。

## 制約・正直な注記
- `/api/live`（今の熱）の鮮度は家のWindowsが `live_pulse.json` を push する頻度に依存＝家が死ぬと live だけ古くなる（ask.sh は「liveが古い時はliveを語らない」ガード済み）。serving自体は死なない。
- `/api/ask` は gemini 専（claude CLI はVMに置かない）。gemini失敗時は正直にエラー（偽の平文は返さない）。
- 秘密（deploy key/GEMINI/TWITTERAPI/tunnel token）はVMローカルのみ・repoに置かない。
