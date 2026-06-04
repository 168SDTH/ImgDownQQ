# core/downloader.py
import io
import os
import ssl
from datetime import datetime
from typing import Optional, Dict, Any

import aiohttp
from PIL import Image

from .logger import setup_logger

logger = setup_logger("DOWNLOADER")
logger.propagate = False

# SSL 配置
ssl_ctx = ssl.create_default_context()
ssl_ctx.set_ciphers("DEFAULT")


def is_gif(file_bytes: io.BytesIO) -> bool:
    try:
        file_bytes.seek(0)
        with Image.open(file_bytes) as img:
            return img.format == "GIF" and img.n_frames > 1
    except Exception as e:
        logger.error(f"判断 GIF 失败: {e}")
        return False
    finally:
        file_bytes.seek(0)

async def download(url: str) -> Optional[bytes]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=ssl_ctx) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    logger.warning(f"下载失败 {url[:60]}... 状态码: {resp.status}")
        except Exception as e:
            logger.error(f"下载异常 {url[:60]}...: {e}")
    return None


async def download_image(
    url: str,
    group_id: int,
    user_id: int,
    extension: str,
    paths: str,
) -> None:

    data = await download(url)
    if data is None:
        return

    pic_bytes = io.BytesIO(data)
    if is_gif(pic_bytes):
        logger.info("检测到 GIF 动图，跳过下载")
        return

    time_str = datetime.now().strftime("%H-%M-%S-%f")
    file_name = f"{time_str}_{user_id}{extension}"

    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isabs(paths):
        paths = paths
    else:
        paths = os.path.join(main_dir, paths)

    save_path = os.path.join(paths, file_name)


    os.makedirs(paths, exist_ok=True)

    
    with open(save_path, "wb") as f:
        f.write(data)
    logger.info(f"原始图片已保存: {save_path}")

