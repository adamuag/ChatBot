from openai import OpenAI
from ES_helper import retrieve_documents


def build_context(documents):
    context = ""

    for doc in documents:
        doc_str = f"Section: {doc['section']}\nQuestion: {doc['question']}\nAnswer: {doc['text']}\n\n"
        context += doc_str
    
    context = context.strip()
    return context


def build_prompt(user_question, documents):
    context = build_context(documents)
    return f"""
                You're a course teaching assistant.
                Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
                Don't use other information outside of the provided CONTEXT.  

                QUESTION: {user_question}

                CONTEXT:

                {context}
                """.strip()

def ask_openai(prompt):

    client = OpenAI()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    return answer

def qa_bot(user_question):
    context_docs = retrieve_documents(query=user_question)
    prompt = build_prompt(user_question, context_docs)
    answer = ask_openai(prompt)
    return answer

