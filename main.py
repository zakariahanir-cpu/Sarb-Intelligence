import os
import argparse
import json
from pathlib import Path

from agent_engine import Agent

class AgentEpsilon(Agent):
    def __init__(self):
        super().__init__("agent_epsilon", os.getenv("EPSILON_GROQ"))


def health_check():
    """Return a deterministic local health report without an API key."""
    root = Path(__file__).resolve().parent
    expected = ["agent_engine.py", "learner.py", "messenger.py", "website_builder.py"]
    return {
        "status": "ok",
        "project": root.name,
        "python_files": len(list(root.glob("*.py"))),
        "helpers_present": {name: (root / name).is_file() for name in expected},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the Sarb intelligence agent.")
    parser.add_argument("task", nargs="*", help="task for the agent")
    parser.add_argument("--check", action="store_true", help="run a local health check")
    args = parser.parse_args(argv)

    if args.check:
        print(json.dumps(health_check(), ensure_ascii=False, sort_keys=True))
        return 0

    agent = AgentEpsilon()
    print(f"--- {agent.name} is online ---")
    task = " ".join(args.task) or "تحقق من سجل الرسائل وتعلم شيئاً جديداً عن تطوير الويب."
    if not agent.api_key:
        print("EPSILON_GROQ is not configured; use --check for a local smoke test.")
        return 2
    print(agent.perform_task(task))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
