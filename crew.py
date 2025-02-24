import os

from crewai import Agent, Crew, Process, Task  # type: ignore
from crewai.project import CrewBase, agent, crew, task  # type: ignore
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace

from azure_llms import get_azure_llm

load_dotenv()

# Must precede any llm module imports

langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))

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
            llm=get_azure_llm("gpt4o"),
        )
    
    @agent
    def export_industry_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["export_industry_agent"], # type: ignore
            llm=get_azure_llm("o1"),
        )

    @agent
    def compare_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["compare_agent"], # type: ignore
            llm=get_azure_llm("o1"),

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
            agent=self.compare_agent(),
        )

    @crew
    def summarize_crew(self) -> Crew:
        return Crew(
            agents=[self.macro_summarizer_agent()],
            tasks=[self.summarize_macroeconomics()],
            process=Process.sequential,
            language="svenska", # type: ignore
            output_log_file="logs/summary_crew_log.txt",
        )
    
    @crew
    def summarize_export_crew(self) -> Crew:
        return Crew(
            agents=[self.export_industry_agent()],
            tasks=[self.summarize_export_industry()],
            process=Process.sequential,
            language="svenska", # type: ignore
            output_log_file="logs/export_summary_crew_log.txt",
        )

    @crew
    def compare_crew(self) -> Crew:
        return Crew(
            agents=[self.compare_agent()],
            tasks=[self.compare_summaries_task()],
            process=Process.sequential,
            language="svenska", # type: ignore
            output_log_file="logs/compare_crew_log.txt",
        )



async def summarize_one_pdf(filename: str, pdf_content: str) -> str:
    """
    Create a new summarizer crew instance and kickoff its execution asynchronously.
    Returns the summarized text (crew_output.raw).
    """

    # Instantiate a new summarizer crew for one run
    summ_crew = FullCrew().summarize_crew()
    # Kick off asynchronously with the input key matching the task template (here "pdf_text")
    summary = await summ_crew.kickoff_async(inputs={"pdf_text": pdf_content})

    export_crew = FullCrew().summarize_export_crew()
    export_summary = await export_crew.kickoff_async(inputs={"pdf_text": pdf_content})

    full_summary = summary.raw + "\n\n ---------- \n Konsekvenser för exportindustrin \n\n " + export_summary.raw

    return full_summary


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