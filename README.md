# min-agent

`min-agent` 是一个只有 200 行代码的 `LLM Agent`，便于理解 `Agent` 的工作原理。如果你想将 `Agent` 应用到实际项目中，可以试试 [Lagent](https://github.com/InternLM/lagent)。

## 安装

```bash
git clone
cd min-agent
pip install -e . -v
```

## 使用

注册[谷歌搜索 API 账号](https://serper.dev/)（有 2500 次免费调用额度），获取 `API_KEY`。

```bash
export SERPER_API_KEY=your_serper_api_key
```

注册 LLM API 账号，例如 `kimi` 或 `deepseek`。

- kimi chat

  注册 [Kimi API 账号](https://platform.moonshot.cn/console/api-keys)，获取 `API_KEY`。

  ```bash
  export OPENAI_API_KEY=your_api_key
  export MODEL_NAME=moonshot-v1-8k
  export BASE_URL=https://api.moonshot.cn/v1
  ```

- deepseek chat

  注册 [Deepseek API 账号](https://platform.deepseek.com/api_keys)，获取 `API_KEY`。

  ```bash
  export OPENAI_API_KEY=your_api_key
  export MODEL_NAME=deepseek-chat
  export BASE_URL=https://api.deepseek.com/v1
  ```

运行 `min-agent`

```bash
python min_agent/agent.py --message '请你介绍一下 LLM Agent'
```
