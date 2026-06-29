# AI Blog Writer 🤖✍️

An automated multi-agent AI system designed to research, write, and edit comprehensive, SEO-optimized blog articles. Built using **CrewAI**, **LiteLLM**, Google's **Gemini 2.0 Flash**, **FastAPI**, and **Next.js**.

## 🚀 Overview

This project demonstrates the power of AI agent orchestration inside a modern full-stack web application. The backend exposes an API that delegates tasks to a "crew" of specialized AI agents working sequentially. The frontend provides a stunning, user-friendly interface to trigger the process and read the final articles.

### The Agent Architecture
1. **The Content Planner:** Researches the topic, identifies the target audience, compiles SEO keywords, and structures a detailed outline.
2. **The Content Writer:** Takes the planner's outline and drafts a compelling, multi-section article naturally incorporating the provided SEO strategies.
3. **The Editor:** Reviews the draft for clarity, grammatical accuracy, and brand alignment, ensuring a professional final tone.

## 🛠️ Installation & Setup

You will need two terminal windows to run this full-stack application locally.

### 1. Backend Setup (FastAPI)
The backend is built with Python 3.12+ and FastAPI.

1. Ensure your `.env` file contains your API key:
   ```env
   GEMINI_API_KEY="your-api-key"
   ```
2. Install the required backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn api:app --reload
   ```
   *The API will run on `http://localhost:8000`*

### 2. Frontend Setup (Next.js)
The frontend is built with Next.js 15, Tailwind CSS v4, and React Markdown.

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   *The web UI will run on `http://localhost:3000`*

## 🌐 Deployment
- **Frontend**: Best deployed on [Vercel](https://vercel.com). Point the root directory to `frontend/`.
- **Backend**: Deploy the Python API using [Render](https://render.com) or [Railway](https://railway.app). Remember to add your `GEMINI_API_KEY` to the environment variables on your hosting provider. Once the backend is deployed, update the `fetch` URL in `frontend/src/app/page.tsx` to point to your new backend URL.