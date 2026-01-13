import httpx
import logging
from typing import List
from app.models.config import settings
from app.models.product import LensResult


logger = logging.getLogger(__name__)


class LensService:
    def __init__(self, api_key: str = settings.SERP_API_KEY):
        self.api_key = api_key
        # .json なしのエンドポイントを使用
        self.base_url = "https://serpapi.com/search"

    async def search_by_image_url(self, image_url: str) -> List[LensResult]:
        """
        httpx を使用して、非同期で画像URLからGoogle Lens検索を実行します。
        """
        # ローカルIPチェック
        if (
            "127.0.0.1" in image_url
            or "localhost" in image_url
            or "192.168." in image_url
        ):
            logger.warning(
                f"image_url ({image_url}) is a local address. SerpAPI/Google cannot access this. Please use ngrok or a public domain."
            )

        params = {"engine": "google_lens", "url": image_url, "api_key": self.api_key}

        try:
            logger.info(f"Requesting SerpAPI for: {image_url} (timeout=90s)")
            async with httpx.AsyncClient() as client:
                # タイムアウトを90秒
                response = await client.get(self.base_url, params=params, timeout=90.0)

                if response.status_code != 200:
                    logger.error(
                        f"SerpAPI Status Error ({response.status_code}): {response.text}"
                    )

                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    logger.error(f"SerpAPI Business Error: {data['error']}")
                    return []

                results = self._parse_results(data)
                logger.info(f"SerpAPI success: found {len(results)} visual matches.")
                return results

        except httpx.TimeoutException:
            logger.error(f"SerpAPI TIMEOUT (90s) for URL: {image_url}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(
                f"SerpAPI HTTP Error: {e.response.status_code} - {e.response.text}"
            )
            return []
        except Exception as e:
            logger.error(f"Error in LensService for URL {image_url}: {e}")
            return []

    def _parse_results(self, data: dict) -> List[LensResult]:
        results = []
        visual_matches = data.get("visual_matches", [])

        for match in visual_matches:
            results.append(
                LensResult(
                    title=match.get("title", ""),
                    link=match.get("link", ""),
                    snippet=match.get("snippet"),
                    source=match.get("source"),
                )
            )
        return results
