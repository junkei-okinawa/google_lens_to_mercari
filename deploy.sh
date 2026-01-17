#!/bin/bash

# .envファイルから環境変数を読み込む
if [ -f .env ]; then
  # すべての変数を自動的にexportする
  set -a
  source .env
  set +a
else
  echo "Error: .env file not found."
  exit 1
fi

# 必須変数のチェック
if [ -z "$GCP_PROJECT_ID" ] || [ -z "$REGION" ]; then
  echo "Error: GCP_PROJECT_ID or REGION is not set in .env"
  exit 1
fi

if [ -z "$SERP_API_KEY" ] || [ -z "$GEMINI_API_KEY" ]; then
  echo "Error: SERP_API_KEY or GEMINI_API_KEY is not set in .env"
  exit 1
fi

echo "🚀 Deploying to Cloud Run..."
echo "Project: $GCP_PROJECT_ID"
echo "Region: $REGION"

# gcloudの設定
gcloud config set project $GCP_PROJECT_ID

# 環境変数のフォーマット (KEY=VALUE,KEY2=VALUE2...)
# USE_SECRET_MANAGER=true が設定されている場合は Secret Manager を使用
if [ "$USE_SECRET_MANAGER" = "true" ]; then
  echo "🔐 Using Secret Manager for API keys..."
  # Secret Manager を使用する場合、環境変数名はシークレット名と一致させる必要があります
  # --set-secrets="ENV_VAR_NAME=SECRET_NAME:VERSION"
  SECRETS_SETTING="SERP_API_KEY=SERP_API_KEY:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest"
  
  # デプロイ実行 (Secret Manager版)
  if gcloud run deploy sedori-lens \
    --source . \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-secrets "$SECRETS_SETTING"; then
    echo "✅ Deployment complete!"
  else
    echo "❌ Deployment failed! Check the logs above for details."
    echo "Tip: Make sure secrets 'SERP_API_KEY' and 'GEMINI_API_KEY' are created in Secret Manager."
    exit 1
  fi
else
  echo "⚠️ Warning: Passing API keys via environment variables is less secure."
  echo "Consider using Secret Manager by setting USE_SECRET_MANAGER=true in .env"
  
  ENV_VARS_STRING="SERP_API_KEY=\"${SERP_API_KEY}\",GEMINI_API_KEY=\"${GEMINI_API_KEY}\""

  # デプロイ実行 (環境変数版)
  if gcloud run deploy sedori-lens \
    --source . \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars "$ENV_VARS_STRING"; then
    echo "✅ Deployment complete!"
  else
    echo "❌ Deployment failed! Check the logs above for details."
    exit 1
  fi
fi
