# ImgDownQQ

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

一个简洁高效的 QQ 群聊图片消息下载工具，支持自动分类和即时下载。

## 功能简介

1. 🚀 **实时下载**：在接收到图片消息后会立刻执行下载。
2. 📂 **自动分类**：按照群聊、日期自动分类，图片根据时间和发送者命名。
3. ⚡ **稳定高速**：基于asyncio构建，高频图片消息不阻塞
4. ✨ **简洁输出**：标准化log输出，简洁直观

## 快速开始

### 安装

1. 克隆本仓库或直接下载源代码：

    ```bash
    git clone https://github.com/168SDTH/ImgDownQQ.git
    ```

2. 进入项目目录：

    ```bash
    cd ImgDownQQ
    ```

3. 安装所需的依赖：

    ```bash
    pip install -r requirements.txt
    ```

### 配置

1. **配置文件简介**：

- **`bot`**：bot启动配置，`host`为 **WebSocket Server地址**，默认为`127.0.0.1`，`port`为 **WebSocket Server端口**。

- **`whitelist`**：图片下载白名单，`groups` 为**群聊**白名单，填写群号，`private` 为**私聊**白名单，填写QQ号（coming soon），不在白名单内的下载任务会被忽略。

- **`paths`**：保存路径，`image_folder` 为图片保存路径，`video_folder` 为视频保存路径（coming soon x2）。

- **`extension`**：要保存的文件扩展名。

2. **修改配置文件**：

    首次运行会自动生成配置文件，编辑 **`config.json`** ，根据上述内容修改配置，或使用默认配置。
    
    > [!NOTE]
    > 必须修改 `whitelist` ，在 `groups` 内填入群号，否则不会执行下载。

3. **修改bot框架配置信息**：

    在NapCat中添加 **`WebSocket Client`** ，填入地址 `ws://{host}:{port}/ws/` ，`host` 和 `port` 为上一步填写的 **WebSocket Server地址和端口**，例如`ws://127.0.0.1:12345/ws/`。

    > [!NOTE]
    > 本程序基于`NapCat`框架开发，其他Onebot框架未进行测试，可能无法正常使用。

### 启动

运行 `main.py`，等待bot连接。
