from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.5-flash")


system_message = SystemMessage(
    "Você é um guia de estudos que ajuda estudantes a aprenderem novos tópicos. \n\n"
    "Seu trabalho é guiar as ideias do estudante para que ele consiga entender o "
    "tópico escolhido sem receber respostas prontas da sua parte. \n\n"
    "Evite conversar sobre assuntos paralelos ao tópico escolhido. Se o estudante "
    "não fornecer um tópico inicialmente, seu primeiro trabalho será solicitar um "
    "tópico até que o estudante o informe. \n\n"
    "Você pode ser amigável, descolado e tratar o estudante como adolescente. Queremos "
    "evitar a fadiga de um estudo rígido e mantê-lo engajado no que estiver "
    "estudando. \n\n"
    "As próximas mensagens serão de um estudante. "
)

human_message = HumanMessage("Olá, meu nome é Murilo")


messages = [system_message, human_message]
response = llm.invoke(messages)
print(f"{'AI':-^80}")
print(response.content) 



messages.append(response)
while True:
    # Pega a mensagem do usuário
    print(f"{'Human':-^80}")
    user_input = input("Digite sua mensagem: ")
    human_message = HumanMessage(user_input)

    # Qualquer uma dessas palavras termina o loop
    if user_input.lower() in ["exit", "quit", "bye", "q"]:
        break

    # Adiciona a mensagem do usuário em messages
    messages.append(human_message)

    # Manda as mensagens com o histórico de volta para o modelo
    response = llm.invoke(messages)

    # Exibe a mensagem do modelo
    print(f"{'AI':-^80}")
    print(response.content)
    print()

    # Adiciona a resposta do modelo em messages
    messages.append(response)

# Isso é só para vermos como ficou nosso histórico de conversas
print()
print(f"{'Histórico':-^80}")
print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep="", end="")
print()