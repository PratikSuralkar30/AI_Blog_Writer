import os
import warnings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
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

app = FastAPI(title="AI Blog Writer API")

# Configure CORS for Next.js frontend (assuming it runs on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    topic: str

class GenerateResponse(BaseModel):
    success: bool
    blog_content: Optional[str] = None
    error: Optional[str] = None

def verify_api_key():
    try:
        # A tiny test completion to verify Ollama is running
        response = completion(
            model="ollama/llama3",
            messages=[{"role": "user", "content": "test"}],
            base_url="http://localhost:11434"
        )
        if not response or 'choices' not in response:
            raise HTTPException(status_code=500, detail="Ollama service unavailable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama validation failed: {str(e)}")

@app.get("/api/health")
def health_check():
    verify_api_key()
    return {"status": "ok", "message": "API is running and Ollama is active."}

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_blog(request: GenerateRequest):
    topic = request.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    # Initialize the LLM using CrewAI's native LLM class
    try:
        ollama_llm = LLM(
            model="ollama/llama3",
            base_url="http://localhost:11434"
        )
        
        planner = Agent(
            role="Content Planner",
            goal=f"Plan engaging and factually accurate content on {topic}",
            backstory=f"You're working on planning a blog article about the topic: {topic}.",
            allow_delegation=False,
            verbose=True,
            llm=ollama_llm
        )

        writer = Agent(
            role="Content Writer",
            goal=f"Write insightful and factually accurate opinion piece about the topic: {topic}",
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

        plan = Task(
            description=(
                f"1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering their interests and pain points.\n"
                "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
            agent=planner,
        )

        write = Task(
            description=(
                f"1. Use the content plan to craft a compelling blog post on {topic}.\n"
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

        crew = Crew(
            tasks=[plan, write, edit],
            agents=[planner, writer, editor],
            verbose=True,
            max_rpm=10 # Throttle requests to avoid hitting Gemini Free Tier 15 RPM limit
        )

        result = await crew.kickoff_async(inputs={"topic": topic})
        return GenerateResponse(success=True, blog_content=str(result))
    
    except Exception as e:
        return GenerateResponse(success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
