# Checkpoint 下載優化（多檔 manifest 場景）

大模型 checkpoint 從 HF Hub 更新（兩 revision 間只差部分 shard）時的標準流程：

1. **先拉 Hub tree API 比對差集，不盲下**：`GET https://huggingface.co/api/models/<repo>/tree/<revision>?recursive=true` 取兩個 revision 的檔案清單，比對 LFS oid（sha256）差集——oid 相同的 shard 用本機既有副本 hardlink（零拷貝、零頻寬），只下載真差異檔。
2. **hardlink 前確認同檔案系統**：hardlink 跨不了 mount point；目標與來源同一 partition 才可用，否則退回 copy。
3. **aria2c 用 resolve URL 下載時的改名坑**：經 resolve/redirect URL 下載，落盤檔名會變成 content-hash 而非原檔名。用 LFS oid（sha256）`sha256sum` 比對確認內容後 rename 回正名，再做 manifest 對帳——不要相信下載工具回報的檔名。
4. **下載完入 manifest 對帳**：逐檔核對 size＋sha256 後才標完成；部分完成的 manifest 標明哪些 shard 已驗。

限速與行程管理（勿殺重啟）等機器專屬觀察不在本檔，見部署機的 run-note。
