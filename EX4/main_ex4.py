from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash")


#Defino o state
class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


#Defino os nodes do grafo
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}

builder = StateGraph(AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState)

#Adicionar nodes ao grafo
builder.add_node("call_llm", call_llm)

#Adicionar edges ao grafo
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

#Compilar o grafo
graph = builder.compile()


current_messages: Sequence[BaseMessage] = []

while True:

    user_input = input("Digite sua mensagem: ")
    

    if user_input.lower() == "sair":
        print("Encerrando...")
        break


    human_message = HumanMessage(user_input)
    current_messages = [*current_messages, human_message]

    #Usar o grafo
    result = graph.invoke({"messages": current_messages})
    current_messages = result["messages"]
    print(str(result["messages"][-1].content))