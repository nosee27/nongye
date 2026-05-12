# 耘智链 (YunZhiChain)

> 基于多Agent协作的中小农户智慧种植服务平台
> 
> **参赛赛道**：青年红色筑梦之旅（乡村振兴方向）  
> **参赛组别**：本科生创意组  
> **学校**：广西科技大学

## 一句话介绍

针对中小农户"缺技术、缺信息、缺渠道"三大痛点，构建**种植规划Agent、病虫害诊断Agent、市场行情Agent、产销对接Agent**四大智能体协同平台，让农户通过自然对话即可获得专家级种植决策支持。

## 核心创新点

1. **多Agent协作架构**：不是单一问答机器人，而是4个专业Agent分工协作，模拟真实农业专家团队工作流
2. **本地农业知识库驱动**：基于广西本地作物数据构建轻量级知识库，解决大模型"幻觉"问题，回答更精准
3. **低门槛交互**：Web端/微信小程序自适应，农户像发微信一样提问，无需下载APP
4. **数据落库可追溯**：所有对话记录存入数据库，便于后续分析农户需求、优化服务

## 技术栈

- **后端**：Python + Flask + SQLAlchemy
- **AI引擎**：Qwen-plus (OpenAI Compatible API via 阿里云DashScope)
- **数据库**：SQLite（开发）/ MySQL（生产）
- **前端**：原生HTML5 + CSS3 + JS（适配手机端、微信Webview）

## 项目结构

```
YunZhiChain/
├── app.py                 # Flask应用工厂
├── run.py                 # 一键启动脚本
├── config.py              # 配置中心（支持.env）
├── models.py              # 数据库模型（对话记录、反馈）
├── requirements.txt       # Python依赖
├── .env.example           # 环境变量模板
├── agents/                # 多Agent模块
│   ├── __init__.py        # Agent注册与调度
│   ├── base_agent.py      # Agent抽象基类
│   ├── planting_agent.py  # 种植规划Agent
│   ├── pest_agent.py      # 病虫害诊断Agent
│   ├── market_agent.py    # 市场行情Agent
│   └── trade_agent.py     # 产销对接Agent
├── routes/
│   └── api.py             # RESTful API（聊天、历史、反馈）
├── templates/
│   └── index.html         # 前端单页应用
├── knowledge/             # 本地知识库（JSON）
│   ├── crops.json         # 作物种植知识
│   ├── pests.json         # 病虫害防治知识
│   └── prices.json        # 农产品行情数据
└── static/                # 静态资源（预留）
```

## 快速启动（3步跑起来）

### 1. 安装依赖

```bash
# 创建虚拟环境（强烈推荐）
python -m venv venv

# Windows激活
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API Key

复制 `.env.example` 为 `.env`，填入你的DashScope Key：

```bash
cp .env.example .env   # Windows用 copy .env.example .env
```

编辑 `.env`：

```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

> 没有Key？去阿里云DashScope控制台免费领额度。

### 3. 运行

```bash
python run.py
```

浏览器打开 **http://127.0.0.1:5000**

手机访问？把 `127.0.0.1` 换成你电脑局域网IP即可。

## 核心API文档

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 对话接口，`{message, session_id}` |
| `/api/agents` | GET | 获取4个Agent列表 |
| `/api/history/<session_id>` | GET | 查询某会话历史 |
| `/api/feedback` | POST | 提交满意度反馈 |

## 测试问题（直接复制到聊天框）

| 问题 | 预期Agent |
|------|-----------|
| "甘蔗什么时候种？怎么施肥？" | 种植规划Agent |
| "叶子发黄有斑点怎么办？" | 病虫害诊断Agent |
| "柑橘现在什么价？会涨吗？" | 市场行情Agent |
| "怎么找靠谱的收购商？" | 产销对接Agent |

## 后续开发路线

- [ ] 接入微信小程序登录（OpenID）
- [ ] 病虫害图片上传 + Qwen-VL多模态识别
- [ ] 语音输入（适配老年农户）
- [ ] 对接真实农产品价格API（农业农村部数据）
- [ ] 合作社后台管理系统

## 团队与贡献

- 后端/Agent架构：广西科技大学软件工程系
- 指导理念：科技助农、乡村振兴

---
**耘智链 · 让每一块田地都有AI专家相伴**
