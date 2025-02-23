# We import Agent, Crew, Process, and Task from crewai
from crewai import Agent, Crew, Process, Task  # type: ignore

# If you need the CrewOutput class for type hints or advanced usage:
from crewai.project import CrewBase, agent, crew, task  # type: ignore


@CrewBase
class FullCrew:
    """
    A single CrewBase class that combines both agents and tasks.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def macro_summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["macro_summarizer_agent"], # type: ignore
            verbose=True
        )
    
    @agent
    def export_industry_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["export_industry_agent"], # type: ignore
            verbose=True
        )

    @agent
    def compare_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["compare_agent"], # type: ignore
            verbose=True
        )

    @task
    def summarize_macroeconomics(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_macroeconomics"], # type: ignore
            async_execution=True,
            agent=self.macro_summarizer_agent(),
        )
    
    @task
    def summarize_export_industry(self) -> Task:
        return Task(
            config=self.tasks_config["summary_export_impact"], # type: ignore
            async_execution=True,
            agent=self.export_industry_agent(),
        )

    @task
    def compare_summaries_task(self) -> Task:
        return Task(
            config=self.tasks_config["compare_summaries_task"], # type: ignore
        )

    @crew
    def summarize_crew(self) -> Crew:
        return Crew(
            agents=[self.macro_summarizer_agent()],
            tasks=[self.summarize_macroeconomics()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def compare_crew(self) -> Crew:
        return Crew(
            agents=[self.compare_agent()],
            tasks=[self.compare_summaries_task()],
            process=Process.sequential,
            verbose=True,
        )



async def summarize_one_pdf(pdf_content: str) -> str:
    """
    Create a new summarizer crew instance and kickoff its execution asynchronously.
    Returns the summarized text (crew_output.raw).
    """
    # Instantiate a new summarizer crew for one run
    summ_crew = FullCrew().summarize_crew()
    # Kick off asynchronously with the input key matching the task template (here "pdf_text")
    crew_output = await summ_crew.kickoff_async(inputs={"pdf_text": pdf_content})
    return crew_output.raw


async def compare_summaries(summaries: list[str]) -> str:
    """
    Create a new comparison crew instance and kickoff its execution asynchronously.
    Returns the comparison report (crew_output.raw).
    """
    # Instantiate a new comparison crew for one run
    comp_crew = FullCrew().compare_crew()
    # Join all summaries with a separator
    summaries_text = "\n\n".join(summaries)
    # Kick off asynchronously with the input key matching the task template (here "summaries")
    crew_output = await comp_crew.kickoff_async(inputs={"summaries": summaries_text})
    return crew_output.raw