from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, MCPServerAdapter
from mcp import StdioServerParameters
from typing import List
from pydantic.warnings import PydanticDeprecatedSince20
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

@CrewBase
class Mongo_Reccomender:
    
    agents: List[BaseAgent]
    tasks: List[Task]

    # === MCP MongoDB Tools ===
    mongo_stdio_server_params = StdioServerParameters(
        command="node",
        # or to whichever path you have the MCP MongoDB server built
        args=["/home/sneha-ltim/saiKrish/CREWAI/mongo-mcp/mcp-mongo-server/build/index.js"],
        env={
            **os.environ,
            "MCP_MONGODB_URI": "mongodb://localhost:27018/Inventory"
        },
    )
    mongo_adapter = MCPServerAdapter(serverparams=mongo_stdio_server_params)
    mongo_tools = [*mongo_adapter.tools]

    # === Search Tool ===
    search_tool = SerperDevTool()

    @agent
    def supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config['supervisor'],
            allow_delegation=True,
            verbose=True,
            chat=True
        )

    @agent
    def mongo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['mongo_agent'],
            verbose=True,
            tools=self.mongo_tools,
            allow_delegation=False,
        )

    @agent
    def recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_agent'],
            verbose=True,
            tools=[self.search_tool],
        )

    @agent
    def chat_support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chat_support_agent'],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def mongo_task(self) -> Task:
        return Task(
            config=self.tasks_config['mongo_task'],
            tools=self.mongo_tools,
            output_file='output/mongo_data.md',
        )

    @task
    def recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommendation_task'],
            tools=[self.search_tool],
            output_file='output/recommendation.md',
        )

    @task
    def chat_support_task(self) -> Task:
        return Task(
            config=self.tasks_config['chat_support_task']
        )

    @task
    def supervisor_task(self) -> Task:
        return Task(
            config=self.tasks_config['supervisor_task'],
        )

    
    @crew
    def crew(self) -> Crew:
        # 🧠 Get actual supervisor agent from list
        supervisor_agent = next(agent for agent in self.agents if agent.role == "Personalization Supervisor")
        worker_agents = [agent for agent in self.agents if agent.role != "Personalization Supervisor"]
        llm = LLM(
            model="nvidia_nim/meta/llama-3.1-8b-instruct",
        )
        # Remove hashtags and use this if u want to run a crew using planning. Does not work well if not OpenAI
        # nvidia_nim/nvidia/nemotron-4-340b-instruct
        # llm = LLM(
        #     model="groq/llama-3.1-70b-versatile",
        # )
        # llm = ChatGroq(model="llama-3.1-70b-versatile",api_key="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")
        return Crew(
            agents=worker_agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=supervisor_agent,
            # memory=True,
            # planning=True,
            # planning_llm=llm,
            verbose=True,
            max_iter = 3,
        )

