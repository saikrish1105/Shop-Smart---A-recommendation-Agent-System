Here’s your polished and professional `README.md` for your CrewAI project:

---

# 🧠 Personalized AI Crew with MongoDB + Recommendations

This project is a **CrewAI-powered multi-agent system** that:

* 🧍‍♂️ Accepts a **user’s name**
* 🔎 **Queries MongoDB** collections related to that user (orders, feedback, info, etc.)
* 🤖 Uses a **supervisor agent** to coordinate task-specific agents:

  * 🧠 A **MongoDB agent** that retrieves and compiles structured user data
  * 🛒 A **Recommendation agent** that analyzes that data and searches the web for smarter product alternatives
* 📄 Outputs a full personalized report

---

## 🚀 Features

* ✅ **MCP integration** with MongoDB using [`mcp-mongo-server`](https://github.com/kiliczsh/mcp-mongo-server)
* 🔍 **Web search agent** using Serper (DuckDuckGo/Google-style results)
* 🤖 Built entirely with [CrewAI](https://github.com/joaomdmoura/crewai) and modular YAML config
* 📊 Extensible — you can plug in analytics, visualizations, and chart tools later

---

## 🧩 Installation

### 1. Clone the project

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv crew_venv
source crew_venv/bin/activate
pip install -r requirements.txt
```

> Or manually install:

```bash
pip install crewai crewai-tools langchain-community python-dotenv
```

---

## 🔑 Configure Your Environment

Create a `.env` file with the following keys:

```env
SERPER_API_KEY=your-serper-api-key
NVIDIA_API_KEY=your-nvidia-api-key  # or GROQ_API_KEY if using Groq
MODEL=nvidia_nim/meta/llama-3.1-8b-instruct  # or appropriate model for your LLM
```

---

## 🔌 Integrate Serper (Web Search)

This project uses `SerperDevTool` from `crewai_tools`. To enable it:

1. Sign up at [Serper.dev](https://serper.dev/) and get your API key
2. Add `SERPER_API_KEY` to your `.env`
3. The `recommendation_agent` will now use Serper to search for better products online

---

## 🍃 Integrate MongoDB MCP Tool

### Step-by-step:

#### 1. Clone and install the MCP server

```bash
git clone https://github.com/kiliczsh/mcp-mongo-server.git
cd mcp-mongo-server
npm install
```

> ⚠️ Do not delete this folder — your CrewAI project launches it from `build/index.js` via `stdio`.

#### 2. Compile the TypeScript server

```bash
npx tsc
```

This will generate:

```
build/index.js
```

> This is the file your CrewAI agent uses.

#### 3. Update `crew.py`

In `crew.py`, configure the Mongo MCP tool:

```python
mongo_stdio_server_params = StdioServerParameters(
    command="node",
    args=["path/to/mcp-mongo-server/build/index.js"],
    env={
        **os.environ,
        "MCP_MONGODB_URI": "mongodb://localhost:27018/Inventory"
    },
)
```

---

## 🧠 How It Works

1. Run the crew:

```bash
python src/agents_structure/main.py
```

2. The Supervisor agent will:

   * Delegate to the Mongo agent → fetch and summarize all user-related data
   * Delegate to the Recommendation agent → search the web for better product suggestions
   * Return a final markdown report

---

## 📁 Output Files

All outputs are saved to:

* `output/mongo_data.md` — user data summary from MongoDB
* `output/recommendation.md` — product recommendations based on their feedback/purchases

You can customize these paths via the `output_file=` setting in each task.

---

## ✅ Example User Flow

```python
result = crew.kickoff(inputs={"user_name": "Sai Krish"})
```

Returns a full user profile and 3 curated product recommendations.

---

## 📦 Future Additions

* Visual analytics using Python MCP servers (charts, feedback sentiment, etc.)
* PDF report generation
* Slack integration for delivery

---

## 🙏 Credits

* [CrewAI](https://github.com/joaomdmoura/crewai)
* [Serper.dev](https://serper.dev/)
* [Mongo MCP Server by kiliczsh](https://github.com/kiliczsh/mcp-mongo-server)
* MIT

