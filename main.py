import os
import warnings
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from crewai import Agent, Task, Crew, LLM
# pyrefly: ignore [missing-import]
import crewai.llms.cache as _crewai_cache
# pyrefly: ignore [missing-import]
import litellm
# pyrefly: ignore [missing-import]
from litellm import completion

# Configure LiteLLM to automatically handle RateLimit errors
litellm.num_retries = 5
litellm.max_backoff = 60

# Monkey-patch to prevent cache_breakpoint injection
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Securely load API keys from the .env file
load_dotenv(override=True)

def main():
    # Initialize the LLM
    ollama_llm = LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434"
    )

    print("Initializing AI Blog Writer Agents...")

    # 1. Define Agents
    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article about the topic: {topic}.",
        allow_delegation=False,
        verbose=True,
        llm=ollama_llm
    )

    writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
        backstory="You're writing a new opinion piece based on the planner's outline.",
        allow_delegation=False,
        verbose=True,
        llm=ollama_llm
    )

    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory="You ensure clarity, consistency, and professional tone.",
        allow_delegation=False,
        verbose=True,
        llm=ollama_llm
    )

    # 2. Define Tasks
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering their interests and pain points.\n"
            "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named in an engaging manner.\n"
            "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=writer
    )

    edit = Task(
        description="Proofread the given blog post for grammatical errors and alignment with the brand's voice.",
        expected_output="A well-edited blog post in markdown format, ready for publication.",
        agent=editor
    )

    # 3. Assemble the Crew
    crew = Crew(
        tasks=[plan, write, edit],
        agents=[planner, writer, editor],
        verbose=True,
        max_rpm=10 # Throttle requests to avoid hitting Gemini Free Tier 15 RPM limit
    )

    # 4. Dynamic Execution
    print("\n" + "="*50)
    topic = input("Enter the topic you want the AI to write a blog about: ")
    print("="*50 + "\n")
    
    result = crew.kickoff(inputs={"topic": topic})

    # 5. Save the output
    output_filename = f"{topic.replace(' ', '_').lower()}_blog.md"
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(str(result))
    
    print(f"\n✅ Success! Your blog post has been generated and saved as: {output_filename}")

if __name__ == "__main__":
    main()