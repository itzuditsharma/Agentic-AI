from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description= "Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """List of multiple companies that are in the news"""
    companies : List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    "Detailed research on a company"
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outloo: str = Field(description="Future outlook and growth prospects")
    investment_potential : str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research on all the companies"""
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all the trending companies")

@CrewBase
class StockPicker():
    """StockPicker crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config = self.agents_config['trending_company_finder'], tools = [SerperDevTool()])
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config = self.agents_config['financial_researcher'], tools = [SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config = self.agents_config['stock_picker'])
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['find_trending_companies'],
            output_pydantic = TrendingCompanyList
        )
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config = self.tasks_config['research_trending_companies'],
            output_pydantic = TrendingCompanyResearchList
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config = self.tasks_config['pick_best_company'],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(
            config = self.agents_config['manager'],
            allow_delegation = True
        )

        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.hierarchical,
            verbose = True,
            manager_agent = manager,
        )
    
    
