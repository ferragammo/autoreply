import asyncio

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_mongodb import MongoDBChatMessageHistory

from auto_reply.api.agent.prompts import global_agent_prompts
from auto_reply.api.agent.tools import query_semantic_tool
from auto_reply.api.agent.db_requests import save_messages
from auto_reply.core.config import settings



class ReplyAgent:
    def __init__(self, message_history: MongoDBChatMessageHistory):
        self.message_history = message_history
        self.tools = [
            query_semantic_tool,
        ]
        self.LLM = settings.LLM.bind_tools(self.tools)

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=global_agent_prompts.system_prompt),
            ("human", "{content}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_tool_calling_agent(
            llm=self.LLM,
            prompt=self.prompt,
            tools=self.tools,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
        )

    async def run(self, content: str) -> str:
        response = await self.agent_executor.ainvoke({"content": content})
        asyncio.create_task(save_messages(content, response, self.message_history))
        return response["output"][-1]["text"]

