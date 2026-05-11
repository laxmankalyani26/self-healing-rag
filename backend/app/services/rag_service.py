from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ollama import Client
from ollama import Client

ollama = Client(
    host="http://host.docker.internal:11434"
)

class RAGService:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = Chroma(
            persist_directory="backend/vectorstore",
            embedding_function=self.embedding_model
        )

    def rewrite_query(self, query: str):

        rewrite_prompt = f"""
        You are a query rewriting assistant.

        Your task is to improve the user's query
        ONLY for better document retrieval.

        Rules:
        - Keep original meaning unchanged
        - Do NOT introduce new topics
        - Do NOT hallucinate information
        - Only clarify vague wording
        - Keep rewritten query concise

        User Query:
        {query}

        Rewritten Query:
        """

        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": rewrite_prompt
                }
            ],
            options={
                "temperature": 0.1
            }
        )

        return response["message"]["content"]

    def ask_question(
        self,
        query: str,
        chat_history: list
    ):

        conversation_context = ""

        for message in chat_history[-4:]:

            conversation_context += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        retrieval_query = f"""
        Conversation History:
        {conversation_context}

        Current User Question:
        {query}
        """

        results = self.vector_db.similarity_search_with_score(
            retrieval_query,
            k=3
        )

        context_parts = []

        sources = []

        for document, score in results:

            context_parts.append(
                document.page_content
            )

            sources.append({
                "source": document.metadata.get("source"),
                "page": document.metadata.get("page"),
                "score": score
            })

        context = "\n\n".join(context_parts)

        best_score = min(
            [score for _, score in results]
        )

        if best_score > 1.0:

            print("\nWeak retrieval detected")
            print("\nRetrying with rewritten query...\n")

            rewritten_query = self.rewrite_query(query)

            print(rewritten_query)

            retry_query = f"""
            Conversation History:
            {conversation_context}

            Rewritten User Question:
            {rewritten_query}
            """

            results = self.vector_db.similarity_search_with_score(
                retry_query,
                k=3
            )

            context_parts = []

            sources = []

            for document, score in results:

                context_parts.append(
                    document.page_content
                )

                sources.append({
                    "source": document.metadata.get("source"),
                    "page": document.metadata.get("page"),
                    "score": score
                })

            context = "\n\n".join(context_parts)

            best_score = min(
                [score for _, score in results]
            )

            if best_score > 1.0:

                return {
                    "answer": (
                        "I could not find relevant "
                        "information in the uploaded documents."
                    ),
                    "sources": sources
                }

        prompt = f"""
        You are a helpful AI assistant.

        Rules:
        - Answer ONLY using the provided context
        - Be conversational and friendly
        - If user greets, respond naturally
        - Do NOT hallucinate facts
        - Keep answers clear and concise

        Conversation History:
        {conversation_context}

        Retrieved Context:
        {context}

        Current Question:
        {query}
        """

        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.2
            }
        )

        return {
            "answer": response["message"]["content"],
            "sources": sources
        }