---
description: Cloud Run へのデプロイ手順
---

このワークフローでは、Google Cloud Run へアプリケーションをデプロイします。

Requirements:
- Google Cloud SDK (`gcloud`) がインストール・認証済みであること。
- プロジェクトIDとリージョンが決定していること。

Steps:

1. **環境変数の確認**
   `.env` ファイルに `GCP_PROJECT_ID` と `REGION` が設定されていることを確認してください。

2. **gcloud 設定**
   プロジェクトを設定します。
   ```bash
   export $(grep -v '^#' .env | xargs)
   gcloud config set project $GCP_PROJECT_ID
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
