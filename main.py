# main.py
from core.bot import create_bot
from core.logger import setup_logger

def load_config():
    from core.config import load_config as _load_config
    return _load_config()

if __name__ == "__main__":
    # 初始化全局日志
    logger = setup_logger("START")
    
    try:
        config = load_config()
        logger.info("配置加载成功")
    except Exception as e:
        logger.critical(f"配置加载失败: {e}")
        exit(1)

    bot = create_bot(config)

    bot_cfg = config.get("bot", {})
    host = bot_cfg.get("host", "127.0.0.1")
    port = bot_cfg.get("port", 12346)

    logger.info(f"Bot 启动 -> {host}:{port}")
    bot.run(host=host, port=port)