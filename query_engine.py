from groq import Groq
import config

class QueryEngine:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.GROQ_MODEL
    
    def answer(self, query, context_chunks):
        """Generate answer using Groq"""
        if not context_chunks:
            return {"answer": "No relevant documents found.", "sources": []}
        
        # Format context
        context = "\n\n".join([
            f"[{i+1}] Ministry: {c['metadata']['ministry']}\n"
            f"Document: {c['metadata']['document']}\n"
            f"Content: {c['text']}"
            for i, c in enumerate(context_chunks)
        ])
        
        prompt = f"""Based on these policy documents, answer the question.

DOCUMENTS:
{context}

QUESTION: {query}

Provide a clear, concise answer with citations to specific documents. Reference document numbers like [1], [2] when citing sources."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.3,  # Lower = more factual
                max_tokens=2000
            )
            
            # Extract sources
            sources = []
            seen = set()
            for chunk in context_chunks:
                key = chunk['metadata']['document']
                if key not in seen:
                    sources.append({
                        "ministry": chunk['metadata']['ministry'],
                        "document": chunk['metadata']['document'],
                        "date": chunk['metadata'].get('date', 'N/A')
                    })
                    seen.add(key)
            
            return {
                "answer": response.choices[0].message.content,
                "sources": sources,
                "model": self.model
            }
            
        except Exception as e:
            print(f"Groq API error: {e}")
            # Fallback to simple retrieval
            return self._simple_answer(query, context_chunks)
    
    def _simple_answer(self, query, context_chunks):
        """Fallback when API fails"""
        sources = []
        seen = set()
        for chunk in context_chunks:
            key = chunk['metadata']['document']
            if key not in seen:
                sources.append({
                    "ministry": chunk['metadata']['ministry'],
                    "document": chunk['metadata']['document']
                })
                seen.add(key)
        
        answer_parts = [
            f"**Query:** {query}\n",
            f"**Found {len(context_chunks)} relevant sections:**\n"
        ]
        
        for i, chunk in enumerate(context_chunks[:3]):
            answer_parts.append(
                f"\n**[{i+1}] {chunk['metadata']['document']}**\n"
                f"{chunk['text'][:400]}...\n"
            )
        
        return {
            "answer": "\n".join(answer_parts),
            "sources": sources
        }