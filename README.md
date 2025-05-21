# 📝 Project Report: Financial Q&A Agent with RAG

## ✅ 1. Overview
This is an Agentic Retrieval-Augmented Generation (RAG) pipeline designed to answer financial questions using semi-structured data sources.
Questions are routed via LangGraph to an Agentic RAG Inference Pipeline that handles retrieval and response generation.

![](images\arch.png)

**The pipeline utilizes:**

- A Retriever Tool and Prompt Manager to prepare context.

- A code writer and executor Agentic Tool for calculation needed.

- A multi query retrieval for query reconstruction to improve retrieval.

- A State Client for managing session data (short- and long-term memory).

- A LLM Gateway that interfaces with OpenAI LLM APIs.

- Underlying memory and vector data are stored in MongoDB Atlas.

- An Observability Pipeline powered by Opik logs and evaluates prompt performance and model output.

- Periodic evaluation datasets are generated from live data and used for benchmarking the system.

**Examples:**

## 🧠 2. Reasoning Behind the Solution Design
RAG Approach: Chosen for its balance between up-to-date factuality and the generative power of LLMs. This is particularly critical in the financial domain where accuracy and explainability are vital.

**LLM API (OpenAI -gpt-4o & gpt-4o-mini):** Chosen to keep infrastructure lightweight while leveraging state-of-the-art LLM capabilities. Running large models locally would increase latency and setup complexity.

**LangGraph:** Enables orchestrating flexible conversational flows, retries, and multi-agent collaboration within the app.

**Vector Indexing with MongoDB:** Offers a cost-effective and scalable way to manage hybrid search (metadata + semantic vectors).

**Retrieval Evaluation Scores with 20 samples**

| **Index Type**            | **Score** |
|---------------------------|-----------|
| qrant_eval                | 9         |
| qrant_mq_eval             | 10        |
| chroma_eval               | 9         |
| chroma_mq_eval            | 10        |
| mango_eval                | 9         |
| mango_mq_eval             | 10        |
| qdrant_hybrid_eval        | 9         |
| qdrant_hybrid_mq_eval     | 9         |
| mongo_hybrid_eval         | 10        |
| mongo_hybrid_mq_eval      | 13        |

**Observability with Opik:** Ensures production-grade monitoring and continuous evaluation, necessary for high-stakes domains like finance.
![](images\observability.png)

## 🧱 3. Code Design & Good Practices

### ✅ Modularity and DRY Principles
- Code is split into reusable modules:

```bash
financeragagent/
    ├── dataset/               # Data files
    ├── notebooks/             # Notebooks
    ├── src/ragagent/          # Main package directory
    │   ├── application/       # Application layer
    │   ├── domain/            # Domain layer
    │   ├── infrastructure/    # Infrastructure layer
    │   └── config.py          # Configuration settings
    ├── run/                   # Entrypoint scripts that use the Python package
    ├── .env.example           # Environment variables template
    ├── .python-version        # Python version specification
    ├── Dockerfile             # API Docker image definition
    ├── docker-compose.yml     # to run the api application
    └── pyproject.toml         # Project dependencies
```

- Agent logic is abstracted in the AgenticLayer class, allowing plug-and-play model or retriever replacement.

### 📁 Organization
- src/ directory contains well-organized logic layers.

- run/ contains bootstrapping 

- app startup logic using FastAPI.

## 📄 Documentation
A comprehensive README.md guides:

- [Environment setup](Install_and_Usage.MD)

- Dockerized deployment

- .env configuration

- Testing & logs

## 🧠 4. Demonstration of Expertise in LLM Ecosystem
- LangGraph orchestration for managing dynamic, stateful interactions.

- Knowledge of modern vector store integration (MongoDB Atlas) with vector embedding and text search support.

- Use of Uvicorn + FastAPI for scalable, async APIs.

- Prompt monitoring & evaluation pipeline, showcasing understanding of RAG observability and hallucination mitigation.

- Decoupling core components with clear interfaces, supporting future migration to other LLMs or retrievers.

## 🧪 5. Evaluation Metrics (RAG)

⏱️ Total Time: 00:03:10 
🔢 Number of Samples: 5  

| **Metric**                   | **Value (avg)** |
|----------------------------   |-----------------|
| 🚫 Hallucination Metric      | 0.0000          |
| ✅ Answer Relevance Metric   | 0.9500          |
| 🔍 Context Recall Metric     | 0.2900          |
| 🎯 Context Precision Metric  | 0.3600          |
| ⚖️ Moderation Metric         | 0.0000          |

![](images\evluation.png)


## 🚀 6. Future Improvements

| **Area**                     | **Idea**                                                                                   |
|------------------------------|--------------------------------------------------------------------------------------------|
| **Embedding Optimization**   | Different emebddings are trained with different data and format. It is crucial to experiment with embeddings especially for domain such as finance. |
| **LLM Optimization**         | Introduce latency-aware routing: switch between Groq, OpenAI, or local GGUF models based on SLA. |
| **Data Freshness**           | Add auto-retraining or re-indexing on content changes.   |
| **Data Preprocessing**       | The data can be improved with further preprocessing Especially contextual information can improve the retrieval performance. |
| **Retrieval**                | I believe the retrieval can be improve with better metadata extraction and with contextual information with hybrid search approach. |
| **Evaluation**               | Integrate Deepeval or TruLens for deeper RAG performance scoring.                             |
| **Security**                 | Add authentication & authorization for internal and external API use.                      |
| **Cost Optimization**        | Cache answers and re-use retrieved contexts to reduce token usage.                          |
| **Guardrails and Hullusination**        | Add Guardrails and hullusination checks at agentic layer.                          |


## ⚖️ 7. Strengths and Limitations
💪 Strengths
- Highly modular, scalable, and cloud-ready design.

- Supports observability and evaluation—rare in most POCs.

- Balanced between performance and cost.

- Well-suited for semi-structured and factual domains like finance.

## ⚠️ 8. Limitations
- Latency depends on the external LLM API (OpenAI) — less optimal without mitigating ratelimits for real-time use at scale.

- No active learning yet — improvements to retriever/model require manual iteration.

- Vector store scalability beyond MongoDB may require QRANT/Weaviate/Pinecone migration.

- Data Preprocessing is needed to identify out of context letters.

- Embeddings selection can improve based on experimentation on data format (tables) and content ($ signs etc.). 

## ✅ 9. Assumptions

- Task is to design an end-to-end agentic system. 
- Accuracy of the system is not the priority, but designing an agentic system is.
- Data provided is already preprocessed for ingestion. 


## ✅ 10. Conclusion
This Agentic RAG-based financial Q&A system showcases a production-grade approach using modern, modular tools. It's cloud-ready, testable, and built with clear separation of concerns—demonstrating sound engineering and a deep understanding of LLM-driven systems. With a few enhancements (like user feedback loops, latency optimization, and retraining), it can scale to support high-volume, enterprise-grade applications.







