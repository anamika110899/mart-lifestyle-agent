import os
from dotenv import load_dotenv
import google.generativeai as genai

from memory.memory_store import TaskMemory

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-flash-latest")

task_memory = TaskMemory()


def ask_llm(system_prompt: str, user_message: str) -> str:
    prompt = f"{system_prompt}\n\nUser: {user_message}"
    try:
        response = model.generate_content(prompt)
        return response.text or "⚠️ Empty response from Gemini."
    except Exception as e:
        return f"⚠️ Gemini API error: {str(e)}"


# ---------------- AGENTS ----------------

class PlannerAgent:
    name = "planner"

    def handle(self, message: str) -> str:
        system = (
            "You are a helpful lifestyle planner for an Indian working professional. "
            "Create structured plans with time blocks: Morning, Work/Study, Evening, Self-care."
        )
        return ask_llm(system, message)


class MealAgent:
    name = "meals"

    def handle(self, message: str) -> str:
        system = (
            "You are an Indian meal planner. Suggest healthy veg/non-veg meals and simple recipes."
        )
        return ask_llm(system, message)


class ShoppingAgent:
    name = "shopping"

    def handle(self, message: str) -> str:
        system = (
            "Create a categorized grocery list: Vegetables, Fruits, Pantry, Dairy, Toiletries."
        )
        return ask_llm(system, message)


class TaskAgent:
    name = "tasks"

    def handle(self, message: str) -> str:
        text = message.strip().lower()

        # Add task
        if text.startswith("add") or "add task" in text or "todo" in text:
            task = message.split("add task")[-1].strip(" :-") if "add task" in text else message[4:].strip()

            if not task:
                return "Tell me what to add. Example: Add task: renew gym membership."

            task_memory.add_task(task)
            tasks = task_memory.get_tasks()
            bullet = "\n".join(f"- {t}" for t in tasks)

            return f"✅ Task added: **{task}**\n\nYour task list:\n{bullet}"

        # List tasks
        tasks = task_memory.get_tasks()
        if not tasks:
            return "You have no saved tasks. Try: Add task: apply for frontend jobs."

        bullet = "\n".join(f"- {t}" for t in tasks)
        return f"Here are your tasks:\n{bullet}"


# ---------------- ORCHESTRATOR ----------------

class OrchestratorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.meals = MealAgent()
        self.shopping = ShoppingAgent()
        self.tasks = TaskAgent()

    def route(self, message: str):
        msg = message.lower()

        if any(w in msg for w in ["meal", "diet", "lunch", "dinner", "breakfast", "recipe"]):
            return self.meals.name, self.meals.handle(message)

        if any(w in msg for w in ["shop", "shopping", "grocery", "buy"]):
            return self.shopping.name, self.shopping.handle(message)

        if any(w in msg for w in ["task", "todo", "remind", "to-do"]):
            return self.tasks.name, self.tasks.handle(message)

        return self.planner.name, self.planner.handle(message)


# ---------------- PUBLIC API ----------------

class ProductivityAgent:

    def llm_answer(self, prompt):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"LLM Error: {str(e)}"

    def chat(self, message: str):
        reply = self.llm_answer(message)
        return {
            "agent": "productivity_agent",
            "reply": reply
        }

    def ai_plan_day(self):
        return self.llm_answer("Create a productive and healthy day plan.")

    def ai_meal_suggestions(self):
        return self.llm_answer("Suggest healthy Indian meals.")

    def ai_shopping_list(self):
        return self.llm_answer("Generate a weekly Indian household shopping list.")

