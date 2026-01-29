from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash")

system_message = SystemMessage("Você é um assistente que se preocupa com o bem-estar do usuário.")

human_message = HumanMessage("Olá tudo bem?")

messages = [system_message, human_message]

response = llm.invoke(messages)

print(response.content)