# 使用 LM Studio 本地部署 Qwen (通义千问) 模型指南

本指南详细介绍了如何使用 LM Studio 在本地部署 Qwen 系列模型，并将其作为兼容 OpenAI API 的后端供 Antigravity 项目使用。

## 1. 下载与安装 LM Studio

- **官方地址**：访问 [lmstudio.ai](https://lmstudio.ai)。
- **安装**：根据您的操作系统（macOS / Windows / Linux）下载对应的安装包并完成安装。

## 2. 初始化配置 (推荐)

由于大语言模型文件通常较大，建议修改默认存储路径：
1. 打开 LM Studio。
2. 点击左下角的 **Settings (齿轮图标)**。
3. 找到 **Server Settings** 或 **Paths**，将模型存储路径更改为空间充足的磁盘目录。

## 3. 搜索与下载 Qwen 模型

1. 点击左侧工具栏的 **Search (放大镜图标)**。
2. 在搜索框输入 `Qwen`。
3. 在结果列表中选择 `Qwen2.5` (或最新的 Qwen 版本)。
4. 在右侧版本列表中，LM Studio 会根据您的硬件（如视频内存）自动标记兼容性：
   - 绿色标记：可完全运行。
   - 蓝色标记：可部分运行（可能较慢）。
5. 点击 **Download** 按钮进行下载。

## 4. 启动本地 API 服务

1. 点击左侧工具栏的 **Local Server (天线图标)**。
2. 在顶部下拉框选择刚才下载的 `Qwen` 模型。
3. 在右侧面板配置：
   - **Cross-Origin Resource Sharing (CORS)**: 开启 (ON)。
   - **Port**: 默认 `1234`。
4. 点击 **Start Server** 按钮。
5. 成功后，控制台会显示 API 基础地址：`http://localhost:1234/v1`。

## 5. 在 Antigravity 中配置

在运行项目前，设置以下环境变量：

```bash
# 在终端中运行或添加到 .env 文件
export OPENAI_API_KEY="lm-studio"  # 本地服务通常不需要真实的 Key，但需填写占位符
export OPENAI_BASE_URL="http://localhost:1234/v1"
```

## 6. 验证服务

启动服务器后，你可以在浏览器访问以下地址验证模型是否加载成功：
`http://localhost:1234/v1/models`

---
*参考资料: [LM Studio本地部署Qwen2.5详细教程](https://www.cnblogs.com/xiao987334176/p/18855424)*
