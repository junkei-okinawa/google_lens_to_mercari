---
description: Cloud Run へのデプロイ手順
---

このワークフローでは、Google Cloud Run へアプリケーションをデプロイします。

Requirements:
- Google Cloud SDK (`gcloud`) がインストール・認証済みであること。
- プロジェクトIDとリージョン、および使用する API キー（`SERP_API_KEY`, `GEMINI_API_KEY`）が決定していること。

Steps:

1. **環境変数の確認**
   `.env` ファイルに `GCP_PROJECT_ID`, `REGION`, `SERP_API_KEY`, `GEMINI_API_KEY` が設定されていることを確認してください。

2. **gcloud 設定**
   プロジェクトを設定します。
   ```bash
   set -a
   # . .env または source .env
   . .env
   set +a
   
   if ! gcloud config set project "$GCP_PROJECT_ID"; then
     echo "Error: Failed to set project. Check your .env file."
     exit 1
   fi
   ```

3. **デプロイ実行**
   ソースコードからビルド・デプロイを行います。
   ```bash
   # APIキーのみを環境変数として設定
   ENV_VARS="SERP_API_KEY=${SERP_API_KEY},GEMINI_API_KEY=${GEMINI_API_KEY}"
   
   gcloud run deploy sedori-lens \
     --source . \
     --region $REGION \
     --allow-unauthenticated \
     --set-env-vars "$ENV_VARS"
   ```

4. **確認**
   出力された URL にアクセスして動作を確認してください。
