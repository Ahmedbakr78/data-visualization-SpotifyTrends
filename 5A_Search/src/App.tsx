import { useState, useEffect, useCallback } from "react";
import SearchHome from "./components/SearchHome";
import ResultsPage from "./components/ResultsPage";
import AIChat from "./components/AIChat";
import { sanitizeQuery, secureConsole, getShellCommandCount, incrementShellCommandCount, checkSecurityHeaders } from "./utils/security";

type Page = "home" | "results" | "assistant";

export default function App() {
  const [page, setPage] = useState<Page>("home");
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState("all");
  const [isDark, setIsDark] = useState(false);
  const [shellCount, setShellCount] = useState(0);
  const [assistantPrompt, setAssistantPrompt] = useState("");

  // Load preferences
  useEffect(() => {
    try {
      const savedDark = localStorage.getItem("5*A-dark-mode");
      if (savedDark === "true") setIsDark(true);
    } catch {}

    // Initialize security
    secureConsole();

    // Load shell command counter
    const count = getShellCommandCount();
    setShellCount(count);
    incrementShellCommandCount();
    console.log(`[5*A] Shell session #${count + 1} | Security initialized`);

    // Check security headers in development
    if (import.meta.env.DEV) {
      const score = checkSecurityHeaders();
      console.log(`[5*A] Security Score: ${score.score}/${score.maxScore}`);
    }
  }, []);

  // Handle URL params for bookmarkability
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const q = params.get("q") || params.get("search") || "";
    const assistant = params.get("assistant");
    if (assistant === "1" || assistant === "true") {
      setAssistantPrompt(q);
      setPage("assistant");
      document.title = "5*A Assistant";
    } else if (q) {
      setQuery(q);
      setPage("results");
    }
  }, []);

  // Save dark mode preference
  useEffect(() => {
    try {
      localStorage.setItem("5*A-dark-mode", String(isDark));
    } catch {}
  }, [isDark]);

  const handleSearch = useCallback((searchQuery: string) => {
    // Sanitize query before processing
    const sanitized = sanitizeQuery(searchQuery);
    if (!sanitized) return;

    setQuery(sanitized);
    setPage("results");
    setActiveTab("all");
    window.history.pushState({}, "", `?q=${encodeURIComponent(sanitized)}`);
    document.title = `${sanitized} — 5*A Search`;
  }, []);

  const handleGoHome = useCallback(() => {
    setPage("home");
    setQuery("");
    setAssistantPrompt("");
    setActiveTab("all");
    window.history.pushState({}, "", "/");
    document.title = "5*A — Search Engine";
  }, []);

  const handleTabChange = useCallback((tab: string) => {
    setActiveTab(tab);
  }, []);

  const handleToggleDark = useCallback((dark: boolean) => {
    setIsDark(dark);
  }, []);

  const handleOpenAssistant = useCallback(() => {
    setAssistantPrompt(query || "");
    setPage("assistant");
    window.history.pushState({}, "", query ? `?assistant=1&q=${encodeURIComponent(query)}` : "?assistant=1");
    document.title = "5*A Assistant";
  }, [query]);

  return (
    <div
      className={`min-h-screen transition-colors duration-500 ${
        isDark ? "bg-[#0a0a0a] text-white" : "bg-white text-[#111]"
      }`}
    >
      {page === "home" ? (
        <SearchHome
          onSearch={handleSearch}
          isDark={isDark}
          onToggleDark={handleToggleDark}
          shellCount={shellCount}
        />
      ) : page === "assistant" ? (
        <div className="min-h-screen px-4 py-6">
          <div className="mx-auto mb-6 flex max-w-5xl items-center justify-between gap-4">
            <button
              onClick={handleGoHome}
              className={`border px-4 py-2 text-xs font-medium uppercase tracking-[0.15em] transition-colors ${
                isDark ? "border-[#333] text-[#aaa] hover:border-white hover:text-white" : "border-[#111] text-[#111] hover:bg-[#111] hover:text-white"
              }`}
            >
              Back to Search
            </button>
            <button
              onClick={() => handleToggleDark(!isDark)}
              className={`border px-4 py-2 text-xs font-medium uppercase tracking-[0.15em] transition-colors ${
                isDark ? "border-[#333] text-[#aaa] hover:border-white hover:text-white" : "border-[#111] text-[#111] hover:bg-[#111] hover:text-white"
              }`}
            >
              {isDark ? "Light" : "Dark"}
            </button>
          </div>
          <AIChat isDark={isDark} initialPrompt={assistantPrompt} />
        </div>
      ) : (
        <ResultsPage
          query={query}
          activeTab={activeTab}
          onTabChange={handleTabChange}
          onSearch={handleSearch}
          onGoHome={handleGoHome}
          isDark={isDark}
          onToggleDark={handleToggleDark}
        />
      )}
      {page !== "assistant" && (
        <button
          onClick={handleOpenAssistant}
          className={`fixed bottom-5 right-5 z-50 border px-4 py-3 text-xs font-semibold uppercase tracking-[0.14em] shadow-lg transition-colors ${
            isDark ? "border-white bg-white text-black hover:bg-[#ddd]" : "border-[#111] bg-[#111] text-white hover:bg-[#333]"
          }`}
        >
          5*A Assistant
        </button>
      )}
    </div>
  );
}
