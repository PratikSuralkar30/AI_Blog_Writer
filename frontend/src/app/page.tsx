"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Send, Bot, Sparkles, Loader2, PenTool } from "lucide-react";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [blogContent, setBlogContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateBlog = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    setBlogContent(null);

    try {
      const res = await fetch("http://localhost:8000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(data.error || data.detail || "Failed to generate blog.");
      }

      setBlogContent(data.blog_content);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || "An unexpected error occurred.");
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 selection:bg-indigo-500/30 font-sans selection:text-indigo-200">
      <div className="relative isolate pt-14">
        {/* Decorative background gradients */}
        <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80" aria-hidden="true">
          <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" />
        </div>

        <div className="mx-auto max-w-4xl px-6 py-12 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center items-center gap-3 mb-6">
              <div className="p-3 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.2)]">
                <PenTool className="w-8 h-8 text-indigo-400" />
              </div>
              <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
                AI Blog Writer
              </h1>
            </div>
            <p className="mt-4 text-lg leading-8 text-slate-400">
              Transform your ideas into publication-ready articles. Our crew of specialized AI agents researches, drafts, and edits comprehensive blogs for you.
            </p>
          </div>

          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-2xl">
            <form onSubmit={generateBlog} className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative flex items-center bg-slate-900 rounded-2xl shadow-xl ring-1 ring-white/10 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500 transition-all">
                <div className="pl-6 flex-shrink-0">
                  <Sparkles className="w-5 h-5 text-indigo-400" />
                </div>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter a topic you want to write about..."
                  className="w-full border-0 bg-transparent py-5 pl-4 pr-4 text-white placeholder:text-slate-500 focus:ring-0 sm:text-lg sm:leading-6 outline-none"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !topic.trim()}
                  className="mr-3 p-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg flex items-center gap-2 font-semibold"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      Generate
                      <Send className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-8 mx-auto max-w-2xl p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-start gap-3">
              <div className="p-1">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="mt-16 text-center">
              <div className="inline-flex items-center justify-center p-6 bg-slate-900/50 backdrop-blur-sm rounded-2xl border border-white/5 shadow-2xl">
                <div className="flex flex-col items-center gap-4">
                  <Bot className="w-12 h-12 text-indigo-400 animate-pulse" />
                  <div className="space-y-2">
                    <h3 className="text-xl font-semibold text-white">Agents are working...</h3>
                    <p className="text-sm text-slate-400 max-w-sm">
                      Our planner, writer, and editor are collaborating to create your masterpiece. This will take few seconds.
                    </p>
                  </div>
                  <div className="flex gap-2 mt-2">
                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                    <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Blog Content Result */}
          {blogContent && (
            <div className="mt-16 relative">
              <div className="absolute inset-0 bg-gradient-to-b from-indigo-500/10 via-purple-500/5 to-transparent rounded-3xl blur-xl" />
              <div className="relative bg-slate-900/80 backdrop-blur-md rounded-3xl shadow-2xl ring-1 ring-white/10 overflow-hidden">
                <div className="px-6 py-4 border-b border-white/10 bg-white/5 flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-indigo-400" />
                    Generated Article
                  </h2>
                </div>
                <div className="p-8 sm:p-12">
                  <article className="prose prose-invert prose-indigo max-w-none 
                                    prose-headings:font-bold prose-h1:text-3xl prose-h2:text-2xl 
                                    prose-a:text-indigo-400 hover:prose-a:text-indigo-300
                                    prose-strong:text-indigo-200">
                    <ReactMarkdown>{blogContent}</ReactMarkdown>
                  </article>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
