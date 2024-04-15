import argparse
import json
from string import Template
from typing import List, Dict


from min_agent.tool import Tool, GoogleSearch, CurrentTime
from min_agent.llm import LLMAPI


_PLANNER = '''你是一位出色的AI助手，擅长解决用户的问题，你的做法是将用户的问题分解为更小的子问题，
每个子问题都可以通过一个工具调用解决，每个工具需要提供工具名称、调用该工具的原因以及接受的参数，你的输出格式形如 [{"tool_name": "工具名称", "reason": "调用工具的原因", "params": {"param1": 1}]。
注意，输出不要包含额外的信息，只需要提供工具调用的信息。

你可以调用的工具列表及其描述如下：

$tool_desc

注意，你只能从上面给出的工具中选择合适的工具。

下面是示例：

用户的问题：如何快速掌握一个领域的知识？
输出：[{"tool_name": "GoogleSearch", "reason": "搜索领域知识", "params": {"query": "如何快速掌握一个领域的知识"}}]

接下来是用户的问题：$question
输出：
'''

_SOLVER = '''你是一位出色的AI助手，你可以基于用户的问题以及参考信息来回答用户的问题。

用户的问题：$question
参考信息：$reference

请基于用户的问题以及参考信息输出回答：
'''

PLANNER_TEMPLATE = Template(_PLANNER)
SOLVER_TEMPLATE = Template(_SOLVER)

class Agent:

    def __init__(self, llm: LLMAPI, tools: List[Tool], retry: int = 3, verbose: bool = False):
        self.llm = llm
        self.name2tools = {tool.name: tool for tool in tools}
        self.retry = retry
        self.verbose = verbose

    def chat(self, message: str):
        parsed_tools = self._plan(message)
        action_res = self._action(parsed_tools)
        output = self._gen_output(message, action_res)
        return output
    
    def _plan(self, message: str) -> List[dict]:
        """规划工具调用"""
        tool_desc = '\n'.join([f'- {name}: {tool.description}' for name, tool in self.name2tools.items()])
        content = PLANNER_TEMPLATE.substitute(tool_desc=tool_desc, question=message)
        if self.verbose:
            print(f'\nllm input: {content}')

        for _ in range(self.retry):
            response = self.llm.chat([{'role': 'user', 'content': content}])
            if self.verbose:
                print(f'\nllm output: {response}')

            parsed_tools = json.loads(response.strip().lstrip('```json').rstrip('```'))
            if isinstance(parsed_tools, list) and all(isinstance(tool, dict) for tool in parsed_tools):
                return parsed_tools
        else:
            assert False, 'Failed to parse tools from llm response.'

    def _action(self, tools: List[dict]) -> Dict[str, str]:
        """调用工具"""
        res = {}
        for tool_info in tools:
            name = tool_info['tool_name']
            res[name] = self.name2tools[name](**tool_info['params'])

        if self.verbose:
            print(f'\naction_res: {res}')

        return res
    
    def _gen_output(self, message: str, action_res: Dict[str, str]) -> str:
        """根据用户输入和工具调用结果生成回答"""
        content = SOLVER_TEMPLATE.substitute(question=message, reference=json.dumps(action_res, ensure_ascii=False))
        if self.verbose:
            print(f'\ncontent: {content}')

        output = self.llm.chat([{'role': 'user', 'content': content}])
        return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agent')
    parser.add_argument('--message', type=str, default='请你介绍一下 LLM Agent', help='user input')
    parser.add_argument('--model-name', type=str, help='model name')
    parser.add_argument('--base-url', type=str, help='base url')
    parser.add_argument('--verbose', action='store_true', help='verbose')
    args = parser.parse_args()

    llm = LLMAPI(model=args.model_name, base_url=args.base_url)
    agent = Agent(llm, tools=[GoogleSearch(), CurrentTime()], verbose=args.verbose)
    print(f'agent output: {agent.chat(args.message)}')
