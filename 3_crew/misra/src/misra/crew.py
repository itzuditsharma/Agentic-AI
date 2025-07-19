from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
import faiss
import numpy as np
import json
import openai


@CrewBase
class Coder():
    """MISRA-aware Coder Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def retrieve_misra_rules(self, query, k=5):
        with open("data/misra_texts.json", "r") as f:
            rule_texts = json.load(f)

        index = faiss.read_index("misra_openai.faiss")
        embedding = openai.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding

        D, I = index.search(np.array([embedding]), k)
        return "\n\n".join([rule_texts[i] for i in I[0]])

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=150,
            max_retry_limit=5
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
