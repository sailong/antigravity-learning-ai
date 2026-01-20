# Antigravity 进阶使用技巧 16 则

本指南基于 [玩转 Antigravity 的 16 个实用技巧](https://www.cnblogs.com/javastack/p/19396292) 整理，旨在帮助你更高效地使用 Antigravity 进行开发。

## 1. 界面汉化
Antigravity 基于 VS Code 开发，你可以直接在插件市场搜索并安装 **"Chinese (Simplified) (简体中文)"** 语言包。重启后界面即可完成汉化，降低使用门槛。

## 2. 完善 Java 开发环境
Antigravity 不仅仅是一个 AI 助手，它也是一个功能完备的 IDE。对于 Java 开发者，安装 **"Extension Pack for Java"** 等插件后，它几乎可以完全替代 IntelliJ IDEA 进行日常开发，避免频繁切换窗口。

## 3. 设置中文回复规则 (Rules)
为了让 AI 始终以中文交流并遵循特定习惯，你可以在 `Settings -> Rules` 中添加全局或工作区规则：
- **规则示例**：`Please always respond in Simplified Chinese.`
- 这能确保 AI 在思考过程和最终回复中都保持中文逻辑。

## 4. 核心快捷键
熟练使用快捷键能极大提升效率：
- `Command + E` (Mac) / `Ctrl + E` (Win)：打开 **Agent Manager**（任务管理器）。
- `Command + L` (Mac) / `Ctrl + L` (Win)：打开 **AI Chat** 对话框。
- `Command + I` (Mac) / `Ctrl + I` (Win)：对选中的代码进行 **Inline Edit**（内联编辑）。

## 5. 快速对话
利用侧边栏的对话窗口或全局对话框，可以随时随地向 AI 提问，无需跳转至专门的聊天界面。

## 6. 支持发送图片
你可以直接粘贴截图到对话框中。AI 能够识别图片中的 UI 问题、报错截图或视觉设计稿，并给出相应的代码建议。

## 7. 切换任务模式
在对话框底部，你可以根据任务复杂度选择模式：
- **Planning (规划)**：适用于复杂、多步骤的任务，AI 会先进行调研和方案设计。
- **Fast (快速)**：适用于简单指令，响应速度极快。

## 8. 模型自由切换
Antigravity 支持多种顶尖模型（如 Gemini 2.0 Pro/Flash, Claude 3.5 Sonnet/Opus 等）。你可以根据需求随时在界面底部切换，充分利用不同模型的长处。

## 9. 无限制智能补全 (Tab Completion)
Antigravity 提供了类似 Cursor 的 AI 代码补全功能。当你输入代码时，灰色提示会出现，按下 `Tab` 键即可采纳。官方目前提供无限制的补全次数。

## 10. 快速内联编辑 (Inline Edit)
选中一段代码后，按下 `Command + I` 唤起编辑框，输入你的修改要求。AI 会直接在原位置修改，并以差异对比（Diff）模式展示，确认无误后点击 Accept 即可。

## 11. 引用上下文 (@ 符号)
使用 `@` 符号可以将特定的上下文喂给 AI：
- `@Files`：引用特定文件。
- `@Codebase`：对整个项目进行全局搜索分析。
- `@Rules`：引用你定义的开发规则。
- `@MCP`：调用 MCP 工具（如搜索、数据库访问等）。

## 12. 触发工作流 (/ 符号)
使用 `/` 符号可以调用预设的指令序列。例如 `/code-check` 可以快速触发代码审计任务。你也可以自定义自己的工作流。

## 13. 透明的任务清单
当你给出一个复杂指令时，AI 会自动将其拆解为多个 Task。你可以在界面中实时看到每一步的执行进度（打勾状态），清晰掌握 AI 的思考路径。

## 14. MCP 协议支持 (Model Context Protocol)
Antigravity 深度支持 MCP。这意味着你可以通过 MCP Server 连接本地数据库、执行 Google 搜索或操作本地文件系统，极大扩展了 AI 的能力边界。

## 15. Agent Manager 并发处理
在 Agent Manager 中，你可以同时启动并监控多个 Agent 运作。比如可以让一个 Agent 写后端 API，另一个 Agent 同时写前端 UI，真正实现并行开发。

## 16. 浏览器子代理 (Browser Sub-agent)
这是 Antigravity 的杀手锏功能。当 AI 需要查资料或验证网页效果时，它会自动启动一个内置浏览器进行操作。此时浏览器会有明显的**蓝色边框**提示，你可以实时看到 AI 模拟点击和滚动的过程。

---
*更多详细内容请参考：[玩转 Antigravity 的 16 个实用技巧](https://www.cnblogs.com/javastack/p/19396292)*
