import os
import json
import requests
from duckduckgo_search import search_duckduckgo
from messenger import send_message, read_messages
from website_builder import create_web_project
from learner import save_knowledge, get_knowledge

class Agent:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.model = "llama-3.1-70b-versatile" # Groq 70b
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # تحديد المسار الأساسي للمشروع بشكل ديناميكي
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.agent_dir = os.path.join(self.base_dir, 'agents', name)
        self.memory_path = os.path.join(self.agent_dir, 'memory.json')
        
        # التأكد من وجود مجلد الوكيل
        os.makedirs(self.agent_dir, exist_ok=True)
        self.history = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_memory(self):
        with open(self.memory_path, "w", encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def call_llm(self, prompt, system_prompt="You are a powerful AI agent with self-learning and self-healing capabilities."):
        if not self.api_key:
            return "Error: API Key is missing. Please set the environment variable."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error calling LLM: {str(e)}"

    def perform_task(self, task_description):
        print(f"[{self.name}] Performing task: {task_description}")
        
        past_knowledge = get_knowledge(task_description)
        knowledge_context = ""
        if past_knowledge:
            knowledge_context = "Past relevant knowledge: " + json.dumps(past_knowledge, ensure_ascii=False)

        system_prompt = f"""
        You are {self.name}, a powerful AI agent in a swarm. 
        Tools available: search_duckduckgo, send_message, read_messages, create_web_project, save_knowledge.
        Task: {task_description}
        {knowledge_context}
        If you encounter errors, use self-healing: search for the error and fix your logic.
        """
        
        response = self.call_llm(task_description, system_prompt)
        
        if "error" in response.lower() or "fail" in response.lower():
            print(f"[{self.name}] Self-healing triggered...")
            search_results = search_duckduckgo(f"how to fix {task_description} error")
            healing_prompt = f"I failed the task: {task_description}. Search results: {search_results}. Provide a fix."
            response = self.call_llm(healing_prompt, system_prompt)
            save_knowledge(self.name, task_description, "Failure -> Self-Healed", response)
        else:
            save_knowledge(self.name, task_description, "Success", response)
            
        self.history.append({"task": task_description, "response": response})
        self.save_memory()
        return response
