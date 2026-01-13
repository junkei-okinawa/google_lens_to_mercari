from fastapi import APIRouter, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.lens_service import LensService
from app.services.extraction_service import ExtractionService
from app.services.mercari_service import MercariService
from typing import Optional
import uuid
from pathlib import Path
import asyncio

import logging

# Logger setup
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

lens_service = LensService()
extraction_service = ExtractionService()
mercari_service = MercariService()


async def delete_file_after_delay(path: Path, delay: int = 60):
    """指定された時間後にファイルを削除する非同期バックグラウンドタスク"""
    await asyncio.sleep(delay)
    if path.exists():
        try:
            path.unlink()
            logger.info(f"Delayed deletion success: {path}")
        except Exception as e:
            logger.error(f"Delayed deletion failed: {path}, {e}")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    background_tasks: BackgroundTasks,
    image_file: Optional[UploadFile] = File(None),
):
    """
    画像を保存し、解析を行うエンドポイント。
    """
    if image_file is None:
        logger.error("No 'image_file' received in the request.")
        # 受信したフォームデータの中身を確認（デバッグ用）
        try:
            form = await request.form()
            logger.debug(f"Received form keys: {form.keys()}")
        except Exception as e:
            logger.debug(f"Could not parse form data: {e}")

        return HTMLResponse(content="Error: No image file received.", status_code=400)

    # 1. Read binary image from UploadFile
    try:
        image_bytes = await image_file.read()
        logger.info(f"Received binary image size: {len(image_bytes)} bytes")

        if len(image_bytes) < 1000:
            logger.warning(
                f"Received image data is very small ({len(image_bytes)} bytes)."
            )
            # 16バイト(ダミー)の場合は警告しつつ通す、0バイトはエラー
            if len(image_bytes) == 0:
                return HTMLResponse(content="Error: Empty image file.", status_code=400)

    except Exception as e:
        logger.error(f"Error reading uploaded file: {e}")
        return HTMLResponse(content=f"Invalid image file: {str(e)}", status_code=400)

    # 2. Save image locally
    img_path = None
    try:
        filename = f"{uuid.uuid4()}.jpg"
        img_dir = Path("static/img")
        img_dir.mkdir(parents=True, exist_ok=True)
        img_path = img_dir / filename

        with open(img_path, "wb") as f:
            f.write(image_bytes)

        # 実際に保存されたファイルサイズを確認
        actual_size = img_path.stat().st_size
        logger.info(f"Image saved successfully: {img_path} ({actual_size} bytes)")

        # Construct public URL
        base_url = str(request.base_url).rstrip("/")
        image_url = f"{base_url}/static/img/{filename}"
        logger.debug(f"Image is accessible at: {image_url}")

        # 3. Lens API with URL (Async call)
        lens_results = await lens_service.search_by_image_url(image_url)

        # ローカルファイルの削除処理をバックグラウンドタスクに登録（1秒後）
        background_tasks.add_task(delete_file_after_delay, img_path, 1)

        # 4. Extract Info with Gemini
        product_info = extraction_service.extract_product_info(lens_results)

        # 5. Generate Mercari URL
        mercari_url = None
        if product_info:
            mercari_url = mercari_service.generate_search_url(product_info)

        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "product_info": product_info,
                "mercari_url": mercari_url,
            },
        )

    except Exception as e:
        logger.error(f"Error in analyze process: {e}")
        return HTMLResponse(
            content=f"Error processing image: {str(e)}", status_code=500
        )
