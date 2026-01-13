# Sedori Lens - Google Lens to メルカリ「せどり」効率化ツール

商品の写真を撮るだけで、Google Lensでの解析とGeminiによるキーワード抽出を組み合わせ、メルカリでの売却実績（相場）を瞬時に調査できるツールです。

## 主な機能
- **カメラ撮影 & 解析**: 商品の画像を撮影し、AIがブランド、型番、特徴を自動抽出します。
- **メルカリ相場調査**: 抽出されたキーワードを用いて、メルカリの「売り切れ」「新しい順」の結果を直接開きます。
- **プレミアムUI**: モバイルでの使用に最適化されたダークモード・グラスモーフィズムデザイン。

## セットアップ

### 1. 依存関係のインストール
本プロジェクトは `uv` を使用して管理されています。
```bash
uv sync
```

### 2. 環境変数の設定
`.env` ファイルに以下の API キーを設定してください。
- `SERP_API_KEY`: SerpAPI (Google Lens API) のキー
- `GEMINI_API_KEY`: Google AI Studio の Gemini API キー

### 3. アプリの起動
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 開発・検証用設定

### CSSのビルド (Tailwind CSS)
```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --watch
```

### テストの実行
```bash
# ユニットテスト
uv run pytest tests/unit

# E2Eテスト (ブラウザでの動作確認)
uv run playwright install chromium
uv run pytest tests/e2e
```

## スマホでの検証方法 (ngrok の使用)

カメラ機能 (`getUserMedia`) は、ブラウザのセキュリティ制限により **HTTPS または localhost** での接続が必須です。スマホから PC の IP アドレスへアクセスした場合、カメラが動作しません。

`ngrok` を使用して一時的に HTTPS 公開URLを発行することで、スマホ実機で検証が可能です。

### 手順:
1. **ngrok のインストール**: [ngrok公式サイト](https://ngrok.com/)の指示に従いインストールします。
2. **ローカルサーバーの起動**:
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. **トンネルの作成**: 別ターミナルで実行。
   ```bash
   ngrok http 8000
   ```
4. **スマホでアクセス**: ターミナルに表示される `Forwarding` の `https://xxxx.ngrok-free.app` という URL をスマホのブラウザで開きます。

## Docker での利用

Docker を使用することで、環境に依存せずアプリを実行できます。

### 1. イメージのビルド
```bash
docker build -t sedori-lens .
```

### 2. コンテナの起動
`.env` ファイルがカレントディレクトリにある想定です。
```bash
docker run -p 8080:8080 --env-file .env sedori-lens
```
起動後、`http://localhost:8080` でアクセスできます。

## 本番へのデプロイ (Google Cloud Run)

本アプリはコンテナ化されているため、Google Cloud Run へのデプロイが容易です。

### 1. Google Cloud プロジェクトの設定
```bash
gcloud config set project [PROJECT_ID]
```

### 2. ビルドとデプロイ
`gcloud run deploy` コマンドを使用して、ソースコードから直接デプロイ（Google Cloud Build経由）するのが最も簡単です。

```bash
gcloud run deploy sedori-lens \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars SERP_API_KEY=xxx,GEMINI_API_KEY=xxx
```

> [!IMPORTANT]
> Cloud Run にデプロイすると HTTPS 通信が標準となるため、スマホからのカメラアクセス (`getUserMedia`) もそのまま動作します。
