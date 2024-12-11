from langchain.load import dumps, loads

def reciprocal_rank_fusion(results: list[list], k=60):
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        loads(doc) for doc, _ in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_results

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)