from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

standalone_question_system_prompt = "Given the latest user question, formulate a standalone question. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
standalone_question_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", standalone_question_system_prompt),
        ("human", "{question}"),
    ]
)

multiquery_generation_system_prompt = "Given a original question and a standalone, generate five different versions of this question to retrieve relevant documents from a vector database. By generating multiple perspectives on this question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions separated by newlines. Do NOT answer the question, just generate queries. Your queries should only be related to - water level scenario, hydrogeological scenario, water quality, available reports for an area,comprehensive report of the Aol on - Ground Water Resource Assessment, Categorization of the area, ground water management practices to be adopted, Conditions for obtaining NOC for ground water extraction, guidance on how to obtain NOC, definition of groundwater terms, training opportunities related to ground water etc."
multiquery_generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", multiquery_generation_system_prompt),
        ("human", "Original question: {question}"),
        ("human", "Standalone question: {standalone_question}"),
    ]
)

answer_system_prompt = (
    "You are chatbot which provides information about ground water scenario. Use the following pieces of retrieved context, original question and message history to answer the question. If you don't know the answer, say that you don't know and apologize. DO NOT make the answer by yourself if it is not available in the context. You must have to give the answer in a structured markdown format. When you are asked to generate the report, you have to make it like a report with all the information in a structured way."
    "\n\n"
    "context: {context}"
)
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", answer_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)