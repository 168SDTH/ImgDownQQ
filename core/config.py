# core/config.py
import json
import os
from typing import Any, Dict, List

from .logger import setup_logger

logger = setup_logger("CONFIG")

# 默认配置信息
DEFAULT_CONFIG: Dict[str, Any] = {
    "bot": {
        "host": "127.0.0.1",
        "port": 12345
    },
    "whitelist": {
        "groups": [
            1234,
            5678
        ],
        "private": [
            1234,
            5678
        ]
    },
    "paths": {
        "image_folder": "images",
        "video_folder": "videos"
    },
    "extension":{
        "image":[".jpg", ".png", ".jpeg"],
        "video":[".mp4", ".mkv", ".avi"]
    }
}

DEFAULT_FILE = "config.json"


def load_config(config_file = DEFAULT_FILE) -> Dict[str, Any]:

    config = None
    used_default = False

    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info(f"成功从 {config_file} 加载配置")
            # 基础校验
            _basic_validate(config)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"读取配置文件失败：{e}，将使用默认配置")
            used_default = True
        except ValueError as e:
            logger.warning(f"配置校验发现问题：{e}，请检查 config.json，将使用默认配置")
            config = None
    else:
        logger.warning(f"配置文件 {config_file} 不存在，将使用默认配置")
        used_default = True

    if config is None:
        config = DEFAULT_CONFIG.copy()
        used_default = True

    if used_default:
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            logger.info(f"已将默认配置写入 {config_file}")
        except IOError as e:
            logger.error(f"无法写入默认配置文件 {config_file}：{e}")

    return config


def _basic_validate(config: Dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ValueError("配置根类型必须是字典")

    # 检查必要一级键
    for key in ("bot", "whitelist", "paths","extension"):
        if key not in config:
            raise ValueError(f"缺少关键配置项：{key}")

    # bot 配置
    bot = config["bot"]
    if not isinstance(bot.get("host"), str):
        raise ValueError("bot.host 必须为字符串")
    if not isinstance(bot.get("port"), int) or not (1 <= bot["port"] <= 65535):
        raise ValueError("bot.port 必须是 1-65535 的整数")

    # whitelist 配置
    whitelist = config["whitelist"]
    if not isinstance(whitelist, dict):
        raise ValueError("whitelist 必须为一个字典，包含 groups 和 private 字段")
    
    groups_list = whitelist.get("groups")
    private_list = whitelist.get("private")
    if not isinstance(groups_list, list):
        raise ValueError("whitelist.groups 必须为列表")
    if not isinstance(private_list, list):
        raise ValueError("whitelist.private 必须为列表")
    
    for gid in groups_list:
        if not isinstance(gid, int):
            raise ValueError(f"群号必须为整数，当前值：{gid}")
    for uid in private_list:
        if not isinstance(uid, int):
            raise ValueError(f"QQ号必须为整数，当前值：{uid}")

    # paths 配置
    paths = config["paths"]
    for path_key in ("image_folder", "video_folder"):
        if path_key not in paths:
            raise ValueError(f"paths 缺少 {path_key}")
        if not isinstance(paths[path_key], str) or not paths[path_key].strip():
            raise ValueError(f"paths.{path_key} 必须为非空字符串")
    
    extension= config["extension"]
    image_ext = extension.get("image")
    video_ext = extension.get("video")
    if not isinstance(image_ext, list):
        raise ValueError("extension.image 必须为列表")
    if not isinstance(video_ext, list):
        raise ValueError("extension.video 必须为列表")
    
    for ext in image_ext:
        if not isinstance(ext, str):
            raise ValueError(f"文件扩展名必须为字符串，当前值：{ext}")
    for ext in video_ext:
        if not isinstance(uid, int):
            raise ValueError(f"文件扩展名必须为字符串，当前值：{ext}")