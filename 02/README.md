# 🇨🇳 Project 02: AI 中国旅游规划师 (China Travel Planner)

> **当前阶段**: 进阶实战
> **前提**: 你已经掌握了 MCP 基础 (Client/Server) 和 Agent 基础 (Function Calling)。
> **目标**: 构建一个能够处理**复杂上下文**、**多步骤推理**且**具备领域知识**的垂直 AI 专家。

---

## 1. 项目愿景 (Project Vision)
我们要打造一个懂中国、懂旅行、更懂“坑”的智能规划师。
用户输入：“我想带父母去西安玩 4 天，不用太累，喜欢看历史。”
系统输出：
1.  **每日行程**: 安排合理的时间线（考虑老人体力）。
2.  **避坑指南**: 比如“不要在兵马俑门口买玉”、“回民街和洒金桥的区别”。
3.  **实时/周边信息**: 天气预测、推荐的美食店。

---

## 2. 核心架构设计的演进 (From Shallow to Deep)

我们将分四个层级来完成这个项目，每一层级都对应一个具体的**技术难点**。

### 🌱 Level 1: 基础咨询 (Information Retrieval)
*   **功能**: 回答“西安有什么好玩的？”
*   **MCP Server**: 
    *   `search_attractions(city: str)`: 返回景点列表。
    *   `get_city_weather(city: str)`: 返回天气。
*   **学习点**: 
    *   如何设计清晰的 Tool Description 避免 LLM 乱填参数。
    *   **规避错误**: 不要让 LLM 自己编造天气，必须强制它调用工具。

### 🌿 Level 2: 约束规划 (Constraint Solving)
*   **功能**: “4天时间，主要看历史。”
*   **Agent 逻辑**:
    *   需要理解“时间”的概念（4天 = 4个单位）。
    *   需要理解“距离”的概念（不要上午在东郊，下午去西郊）。
*   **学习点**: 
    *   **Context Management**: 所有的景点介绍加在一起可能会撑爆 Context Window，学会如何“只取摘要”。
    *   **Reasoning**: 让 Agent 先思考路线 (Plan)，再填充细节 (Fill)。

### 🌳 Level 3: 领域专家 (Domain Expertise - "避坑")
*   **功能**: 主动提示注意事项。
*   **MCP Server**:
    *   增加 `get_travel_warnings(city: str)` 工具。
*   **Agent 逻辑**:
    *   在规划完成后，触发一个“Review 步骤”。
    *   Agent 自我反思：“这个行程里有没有涉及高风险景区？如果有，插入警告。”
*   **学习点**: 
    *   **Post-processing**: 我们可以用两个 Agent。一个负责画大饼（规划），一个负责挑刺（风控）。

### 🌲 Level 4: 终极形态 (Structured Output)
*   **功能**: 输出一份完美的 Markdown/PDF 攻略。
*   **学习点**: 
    *   **Pydantic 输出**: 强制 Agent 输出特定的 JSON 结构（如 `{ "day1": [...], "tips": [...] }`），然后用 Python 代码渲染成好看的 Markdown 表格。

---

## 3. 详细实施计划 (Step-by-Step Plan)

### Step 1: 数据层 (The "World" Knowledge)
我们不需要真的去爬携程的数据（太复杂），我们用 **Mock Data** 来模拟一个“完美的数据库”。

**任务**: 创建 `02/travel_server.py`
*   不必联网，直接用一个巨大的 Python Dictionary 存储几个热门城市（北京、西安、成都）的数据。
*   实现工具：`get_attractions`, `get_food`, `get_warnings`。
*   **专家建议**: 把“避坑指南”作为单独的数据字段，不要混在景点介绍里，方便 Agent 单独提取。

### Step 2: 逻辑层 (The Agent Brain)
**任务**: 创建 `02/planner_agent.py`
*   继承 `01` 中的 ReAct 循环。
*   **关键升级**: 引入 `System Prompt v2.0`。
    *   你需要教会 AI：“考虑到体力消耗，每天景点不能超过 3 个”。
    *   你需要教会 AI：“如果是老人出行，尽量避开爬山”。

### Step 3: 交互层 (The Interface)
纯命令行有点枯燥。
**任务**:
*   让 Agent 第一步先输出一个“思考大纲” (Plan Outline)。
*   最后一步生成 `itinerary.md` 文件。

---

## 4. 专家级避坑指南 (Common Pitfalls)

### 🔴 陷阱 1: 上下文污染 (Context Pollution)
*   **问题**: 把所有景点的详细介绍（几千字）都发给 LLM。
*   **后果**: LLM 记不住重点，或者 Tokens 耗尽。
*   **解决方案**: 工具只返回 **Metadata** (名称、耗时、标签、评分)。只有当 Agent 决定“我要去兵马俑”时，再调用 `get_attraction_details('兵马俑')` 获取详情。这就是“Lazy Loading”（懒加载）思维。

### 🔴 陷阱 2: 幻觉 (Hallucination)
*   **问题**: Agent 编造了一个不存在的高铁班次。
*   **解决方案**: 
    *   在 System Prompt 里严厉禁止编造数据。
    *   或者提供一个 `check_transport(from, to)` 工具，强制校验。

### 🔴 陷阱 3: 死循环
*   **问题**: Agent 觉得规划不完美，反复调用搜索工具。
*   **解决方案**: 
    *   设置 `max_steps = 10`。
    *   强制 Agent 在最后一步必须调用 `finish_planning` 工具。

---

## 5. 项目启动清单

1.  [ ] 创建 `02` 目录。
2.  [ ] 在 `02` 下复用 `01` 的环境（或者创建新的虚拟环境，推荐复用）。
3.  [ ] 开始编写 `travel_server.py` (先写死数据)。

祝你好运！这个项目完成后，你将拥有一个能真正辅助人类决策的高级 AI 助手。
