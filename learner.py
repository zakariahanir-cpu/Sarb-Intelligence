import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
KNOWLEDGE_BASE_FILE = os.path.join(KB_DIR, "learned_knowledge.json")

def save_knowledge(agent_name, task, outcome, solution):
    """
    يحفظ المعرفة وينشئ المجلد والملف تلقائياً.
    """
    os.makedirs(KB_DIR, exist_ok=True)
    knowledge = []
    if os.path.exists(KNOWLEDGE_BASE_FILE):
        with open(KNOWLEDGE_BASE_FILE, "r", encoding='utf-8') as f:
            try:
                knowledge = json.load(f)
            except json.JSONDecodeError:
                knowledge = []
    
    knowledge.append({
        "agent": agent_name,
        "task": task,
        "outcome": outcome,
        "solution": solution
    })
    
    with open(KNOWLEDGE_BASE_FILE, "w", encoding='utf-8') as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)
    return f"Knowledge saved by {agent_name}"

def get_knowledge(query):
    """
    يبحث في قاعدة المعرفة.
    """
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        return []
    
    with open(KNOWLEDGE_BASE_FILE, "r", encoding='utf-8') as f:
        try:
            knowledge = json.load(f)
        except json.JSONDecodeError:
            return []
    
    matches = [k for k in knowledge if query.lower() in k['task'].lower() or query.lower() in k['solution'].lower()]
    return matches
