from src.graphs.workflow import workflow



while True:
    query = input("You: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = workflow.invoke(
    {
        "query": query,
        "retrieved_docs": [],
        "answer": "",
        "route": ""
    }
)

    print("\nAssistant:", result["answer"])