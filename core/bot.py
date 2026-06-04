# core/bot.py
import os
from typing import Dict, Any
from datetime import datetime

from aiocqhttp import CQHttp, Event

from .logger import setup_logger
from .downloader import download_image

logger = setup_logger("BOT")
logger.propagate = False


def create_bot(config: Dict[str, Any]) -> CQHttp:
    bot = CQHttp()

    # 白名单
    group_whitelist = config["whitelist"].get("groups", [])
    private_whitelist = config["whitelist"].get("private", [])
    host = config["bot"].get("host", "127.0.0.1")
    port = config["bot"].get("port", 12345)

    # 保存路径
    paths = config["paths"]

    # 群消息处理
    @bot.on_message("group")
    async def handle_group_message(event: Event):
        group_id = event.group_id
        user_id = event.user_id
        image_ext = config["extension"].get("image", [".jpg", ".png", ".jpeg"])
        video_ext = config["extension"].get("video", [".mp4"])

        if group_id not in group_whitelist:
            logger.debug(f"群 {group_id} 不在白名单，已忽略此次下载任务")
            return

        for msg_seg in event.message:
            seg_type = msg_seg["type"]
            image_path = os.path.join(paths.get("image_folder"), f"{group_id}", datetime.now().strftime("%Y%m%d"))
            video_path = os.path.join(paths.get("video_folder"), f"{group_id}", datetime.now().strftime("%Y%m%d"))
            image_file_path = os.path.join(image_path, "file")
            video_file_path = os.path.join(video_path, "file")


            # 图片消息
            if seg_type == "image":
                summary = msg_seg["data"].get("summary", "")
                if summary == "[动画表情]":
                    logger.info("检测到动画表情，跳过处理")
                    continue
                # 获取文件的拓展名
                _, ext = os.path.splitext(msg_seg["data"]["file"])
                if ext.lower() in image_ext:
                    await download_image(
                        msg_seg["data"].get("url"),
                        group_id,
                        user_id,
                        ext,
                        image_path
                    )

            # 群文件中的图片
            elif seg_type == "file":
                _, ext = os.path.splitext(msg_seg["data"]["file"])
                if ext.lower() in image_ext:
                    # 获取文件url
                    file_url = msg_seg["data"].get("url","")
                    if file_url:
                        await download_image(
                            file_url,
                            group_id,
                            user_id,
                            ext,
                            image_file_path
                        )


    return bot