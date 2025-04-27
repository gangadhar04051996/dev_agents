from crewai import LLM
from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Process, Task

@CrewBase
class CodeWriter():
    """CodeWriter Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def code_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_writer'],
            verbose=True,
            llm=LLM(
                model="ollama/granite3.3",
                base_url="http://localhost:11434"
            )
        )

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],
            verbose=True,
            llm=LLM(
                model="ollama/gemma3",
                base_url="http://localhost:11434"
            )
        )

    @agent
    def flow_diagram_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['flow_diagram_creator'],
            verbose=True,
            llm=LLM(
                model="ollama/gemma3",
                base_url="http://localhost:11434"
            )
        )

    @task
    def code_development_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_development_task']
        )

    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task']
        )

    @task
    def flow_diagram_task(self) -> Task:
        return Task(
            config=self.tasks_config['flow_diagram_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CodeWriter crew"""
        agents = [
            self.code_writer(),
            self.code_reviewer(),
            self.flow_diagram_creator()
        ]
        tasks = [
            self.code_development_task(),
            self.code_review_task(),
            self.flow_diagram_task()
        ]
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
