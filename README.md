# Ollama + FastAPI + 双前端聊天机器人

这是一个基于 **Ollama** 本地大语言模型的聊天机器人项目，通过 **FastAPI** 提供统一的后端 API 服务，并同时支持 **Streamlit** 和 **Gradio** 两种前端界面，方便用户选择和使用。

## 项目架构

```
├── Back_api.py          # FastAPI 后端服务，对接 Ollama
├── Front_api.py         # Streamlit 前端界面
├── gradio_api.py        # Gradio 前端界面
└── README.md            # 项目说明文档
```

### 技术栈
- **后端**：FastAPI + Ollama (本地 LLM)
- **前端**：Streamlit + Gradio (双前端可选)
- **通信**：HTTP 请求，支持流式响应
- **LLM 模型**：qwen:4b (可通过配置修改)

## 功能特点

- ✅ **本地部署**：基于 Ollama，无需联网即可使用
- ✅ **流式输出**：支持 SSE 流式响应，提升用户体验
- ✅ **双前端选择**：Streamlit 和 Gradio 两种界面，满足不同偏好
- ✅ **可调参数**：支持调整 temperature、top_p、max_tokens、历史对话长度等
- ✅ **系统提示词**：可自定义助手角色和行为
- ✅ **对话历史**：保留对话上下文，支持多轮交互

## 环境依赖

### 1. 安装 Python 依赖
```bash
pip install fastapi uvicorn openai streamlit gradio requests
```

### 2. 安装 Ollama
访问 [Ollama 官网](https://ollama.ai/) 下载安装包，或使用命令行安装：

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** 从官网下载安装包

### 3. 下载模型
启动 Ollama 服务后，下载所需模型（默认为 qwen:4b）：
```bash
ollama pull qwen:4b
```

也可根据需要选择其他模型，如：
```bash
ollama pull llama2
ollama pull mistral
ollama pull qwen:7b
```

## 使用方法

### 1. 启动后端服务
```bash
python Back_api.py
```
服务将在 `http://0.0.0.0:6066` 启动，提供 `/chat` 接口。

### 2. 启动前端界面（二选一）

#### 选项 A：Streamlit 界面
```bash
streamlit run Front_api.py
```
访问 `http://localhost:8501`

#### 选项 B：Gradio 界面
```bash
python gradio_api.py
```
访问 `http://localhost:7860`

### 3. 开始对话
- 在输入框中输入问题
- 可调整左侧参数（temperature、top_p 等）
- 系统会自动保存对话历史，支持多轮交互
- 点击清空按钮可重置对话

## API 接口说明

### 请求端点
`POST http://localhost:6066/chat`

### 请求参数（JSON Body）
| 参数名      | 类型   | 必填 | 默认值                 | 说明              |
| ----------- | ------ | ---- | ---------------------- | ----------------- |
| query       | string | 是   | -                      | 用户输入的问题    |
| sys_prompt  | string | 否   | "你是一个有用的助手。" | 系统提示词        |
| history     | list   | 否   | []                     | 历史对话记录      |
| history_len | int    | 否   | 1                      | 保留的对话轮数    |
| temperature | float  | 否   | 0.5                    | 采样温度 (0-2)    |
| top_p       | float  | 否   | 0.5                    | 核采样概率 (0-1)  |
| max_tokens  | int    | 否   | None                   | 最大生成 token 数 |

### 响应格式
- **Content-Type**: `text/plain`
- **数据格式**: SSE 流式文本（每个 chunk 为一段文本）
- 支持流式和非流式两种接收方式

### 示例请求
```python
import requests

data = {
    "query": "你好，请介绍一下自己",
    "sys_prompt": "你是一个友好的助手",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2048
}

response = requests.post("http://localhost:6066/chat", json=data, stream=True)

for chunk in response.iter_content(decode_unicode=True):
    print(chunk, end="")
```

## 项目特色

### 1. 后端设计亮点
- **全局消息管理**：使用 `global messages` 动态管理对话上下文
- **历史长度控制**：通过 `history_len` 灵活控制上下文窗口
- **流式响应**：利用 FastAPI 的 `StreamingResponse` 实现 SSE 输出
- **参数透传**：前端参数完整透传到 Ollama API

### 2. 前端设计亮点

**Streamlit 版本**：
- 简洁的侧边栏配置界面
- 支持流式输出的实时渲染
- 一键清空聊天历史

**Gradio 版本**：
- 现代化的聊天界面
- 响应式布局，自动适配屏幕
- 内置 ChatInterface 组件，交互友好

## 配置修改

### 修改模型
在 `Back_api.py` 中修改：
```python
response = await aclient.chat.completions.create(
    model="qwen:4b",  # 改为其他模型名称
    ...
)
```

### 修改服务端口
- **后端**：修改 `uvicorn.run(app, host="0.0.0.0", port=6066)` 中的 port 参数
- **Streamlit**：运行时指定 `streamlit run Front_api.py --server.port 8501`
- **Gradio**：在 `demo.launch(server_port=7860)` 中指定

### 修改后端地址
如需部署在不同服务器，修改前端文件中的 `backend_url` 变量：
```python
backend_url = "http://你的服务器IP:端口/chat"
```

## 常见问题

### 1. Ollama 连接失败
确保 Ollama 服务已启动：
```bash
ollama serve
```
或检查是否安装了所需模型：
```bash
ollama list
```

### 2. 端口被占用
修改启动端口，或使用以下命令查看占用：
```bash
# Linux/Mac
lsof -i:6066

# Windows
netstat -ano | findstr :6066
```

### 3. 流式输出不显示
检查前端代码中的 stream 参数，确保为 True。

### 4. 历史对话不保存
确认前端已正确将 `history` 参数传递给后端，后端会使用 `history_len` 控制长度。

## 扩展建议

- **添加多模型支持**：可在后端实现模型选择功能
- **增加用户认证**：添加 API Key 或 JWT 认证机制
- **数据库持久化**：将对话历史存入数据库
- **WebSocket 支持**：改用 WebSocket 实现双向通信
- **知识库增强**：集成 RAG（检索增强生成）功能
- **部署到云端**：可使用 Docker 容器化部署

## 相关资源

- [Ollama 官方文档](https://github.com/ollama/ollama)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Streamlit 文档](https://docs.streamlit.io/)
- [Gradio 文档](https://www.gradio.app/docs/)

---

**Enjoy your local LLM chatbot! 🤖**