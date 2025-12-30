# BrainfogCLI 🧠☁️

**BrainfogCLI** is a support project designed to run, test, and develop the core
*engine behind **Brainfog**, an upcoming online personal memory assistant.

While the main Brainfog project will be a full-featured online service, this CLI tool serves as a local testbed for the semantic retrieval architecture. It allows you to interact directly with the memory engine to test natural language memorization, context-aware recall, and the multi-agent system in a terminal environment.

## ✨ Engine Features

- **Natural Language Memorization:** Just type what you want to remember. No
forms or strict syntax.
- **Smart Recall:** Ask questions naturally. The engine uses an LLM to refine
your query, search your memories, and synthesize an answer.
- **Noise Filtering:** Intelligently ignores irrelevant memories (e.g.,
distinguishing between "Sarah's Birthday" and "Project Phoenix").
- **Perspective Awareness:** Automatically shifts perspective from "I have a
meeting" (stored memory) to "You have a meeting" (assistant response).
- **Temporal Awareness:** Understands relative time (resolves "tomorrow" based
on the current date).
- **Local-First:** Runs efficiently with a local SQLite database and lightweight
FAISS vector search.

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* An OpenAI API Key

### Installation

Clone the repository and install the package. You can install it in standard
mode or editable mode if you plan to modify the code or test engine changes.

1.  **Clone the repository**
    ```bash
    git clone https://github.com/cipherdragon/BrainFogCLI.git
    cd brainfog-cli
    ```

2.  **Install the package**
    This will automatically install all required dependencies (LangChain, FAISS,
    SQLAlchemy, etc.). I suggest you to use a virtual environment as this installs
    quite a few packages.

    * **Standard Install:**
        ```bash
        pip install .
        ```
    * **For Development (Editable):**
        ```bash
        pip install -e .
        ```

3.  **Configuration**
    Create a `.env` file in the root directory with your credentials:

    ```env
    OPENAI_API_KEY="openai_api_key_here"
    DATABASE_URL="sqlite:///fog.db"
    ```

## 📖 Usage

Once installed, simply run the `brainfog` command to launch the interactive CLI.

```bash
brainfog
```