import os
import sys

# إضافة المسار الرئيسي للمشروع
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from shared_tools.agent_engine import Agent

# المفتاح الخاص بالوكيل EPSILON
api_key = os.getenv("EPSILON_GROQ")

class AgentEpsilon(Agent):
    def __init__(self):
        super().__init__("agent_epsilon", api_key)

if __name__ == "__main__":
    agent = AgentEpsilon()
    print(f"--- {agent.name} is online ---")
    
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        agent.perform_task(task)
    else:
        # المهمة الافتراضية: التعلم الذاتي وبناء المواقع
        agent.perform_task("تحقق من سجل الرسائل، تعلم شيئاً جديداً عن تطوير الويب، وقم بتحسين موقعك الحالي أو ابدأ واحداً جديداً.")
