'''
Desenvolvido por: Guilherme Mileib
Cógido baseado no artigo: https://medium.com/pythoneers/building-a-multi-agent-system-using-crewai-a7305450253e

Esse código 1 é um scrape que busca informações web usando o framework, usamos a ferramenta que seria o wikipedia

libs usadas:
pip install crewai-tools crewai langchain_openai python-dotenv
pip intall pandas
'''

from crewai_tools import ScrapeWebsiteTool, FileWriterTool, TXTSearchTool
from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

tool = ScrapeWebsiteTool(website_url='https://en.wikipedia.org/wiki/Artificial_intelligence')  

text = tool.run()
print(text)

file_writer_tool = FileWriterTool()
text = text.encode("ascii", "ignore").decode()

result = file_writer_tool._run(filename='ai.txt', content = text, overwrite="True")
print(result)

tool = TXTSearchTool(txt='ai.txt')

context = tool.run('What is natural language processing?')

data_analyst = Agent(
    role='Educator',
    goal=f'Based on the context provided, answer the question - What is Natural Language Processing? Context - {context}',
    backstory='You are a data expert',
    verbose=True,
    allow_delegation=False,
    tools=[tool]
)

test_task = Task(
    description="Understand the topic and give the correct response",
    tools=[tool],
    agent=data_analyst,
    expected_output='Give a correct response'
)

crew = Crew(
    agents=[data_analyst],
    tasks=[test_task]
)

output = crew.kickoff()
print(output)