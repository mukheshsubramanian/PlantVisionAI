import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.agent_service import PlantHealthAgent
agent = PlantHealthAgent()
queries = [
    "chatbot is not working",
    "How do I take care of a tomato plant?",
    "What plants can I grow in shade?",
    "Can I use dish soap on leaves?",
    "How to treat powdery mildew on squash?",
    "What is black spot on roses?",
    "Is copper fungicide safe for vegetables?",
    "How do I get rid of caterpillars?",
    "What causes blossom end rot?",
    "How often should I fertilize indoor plants?",
    "Can plants recover from root rot?",
    "How do I treat rust on beans?",
    "What is companion planting for corn?",
    "How to test soil pH naturally?",
    "Why is my plant dropping leaves?",
    "How do I prune indeterminate tomatoes?",
    "What fungicide should I use for anthracnose?",
    "Can I eat tomatoes with early blight?",
    "How do I propagate cuttings in water?"
]
for q in queries:
    res = agent.generate_response(q)
    print(f"Q: {q}")
    ans_first = res["answer"].split("\n")[0]
    print(f"A: {ans_first}")
    print(f"Context: {res.get('disease_context')}")
    print("-" * 50)
