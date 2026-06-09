# 🤖 Weekend Research Assistant

A professional, conversational AI agent built with the **Google Agent Development Kit (ADK)** that autonomously researches topics, extracts content from the web, and synthesizes comprehensive summaries.

## ✨ Features

-   **Autonomous Discovery**: Uses `google_search` to find relevant sources when no URLs are provided.
-   **High-Fidelity Extraction**: Leverages **MarkItDown** to convert webpages, PDFs, and documents into clean Markdown for LLM consumption.
-   **Conversational Memory**: Powered by ADK's session management and `PreloadMemoryTool` to maintain context across a research session.
-   **Advanced Synthesis**: Uses **Gemini 2.5 Flash** to create professional summaries, identify themes, and contrast viewpoints.

## 🛠️ Tech Stack

-   **Framework**: [Google ADK](https://adk.dev/) (Agent Development Kit)
-   **LLM**: Google Gemini 2.5 Flash
-   **Content Conversion**: [MarkItDown](https://github.com/microsoft/markitdown)
-   **Package Management**: [uv](https://github.com/astral-sh/uv)
-   **Language**: Python 3.12+

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) installed on your system.
- A Google Gemini API Key.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nischal390/weekend-research-assistant.git
   cd weekend-research-assistant
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

### Running the Agent

Start the conversational interface:
```bash
uv run main.py
```

## 📖 Example Usage

**Scenario 1: Autonomous Research**
> **You**: "Research the current state of nuclear fusion energy."
> **Agent**: *(Searches Google $\rightarrow$ Extracts top 3 articles $\rightarrow$ Synthesizes summary)*

**Scenario 2: Targeted Extraction**
> **You**: "Read this paper and summarize the methodology: https://arxiv.org/pdf/xxxx.pdf"
> **Agent**: *(Extracts PDF via MarkItDown $\rightarrow$ Summarizes methodology)*

**Scenario 3: Follow-up Memory**
> **You**: "Based on the fusion research, what are the main technical hurdles?"
> **Agent**: *(Recalls previous context $\rightarrow$ Answers specific question)*

---
*Built as a PoC for high-fidelity research automation.*
