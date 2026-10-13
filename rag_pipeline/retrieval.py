from rag_pipeline.ingestion import embedding_manager, VectorStoreManager
from rank_bm25 import BM25Okapi 
from config import TOP_K, FINAL_K

def retriever_pipeline(query):
  retrieved_obj= retriever()
  retrieve_docs= retrieved_obj.retrieve(query)
  return retrieve_docs

class retriever:
  def __init__(self):
    self.vector_store= VectorStoreManager()
    self.embeddings= embedding_manager()

  def retrieve(self, query, top_k= TOP_K, score_threshold: float= 0.2):
    query_embeddings= self.embeddings.generate_embeddings([query])[0]

    try:
      results= self.vector_store.collection.query(
          query_embeddings= query_embeddings.tolist(),
          n_results= top_k
      )

      print("raw distances from chroma:", results['distances'])
      print('row docs found', len(results['documents'][0]))
      # process results
      retrieved_docs= []

      if results['documents'] and results['documents'][0]:
        documents= results['documents'][0]
        metadatas= results['metadatas'][0]
        distances= results['distances'][0]
        ids= results['ids'][0]

        for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
          # convert distance to similarity score (ChromaDB uses cosine distance)
          similarity_score = 1-distance

          if similarity_score >= score_threshold:
            retrieved_docs.append({
              "id": doc_id,
              "content": document,
              "metadata": metadata,
              "similarity_score": similarity_score,
              "distance": distance,
              "rank": i+1
            })
        print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
        print("retrieved docs= ", retrieved_docs)

        # retrieved_docs= sorted(retrieved_docs, key= lambda x: x['similarity_score'], reverse= True)

        # retrieved_docs= retrieved_docs[:FINAL_K]

        # print(f"Re-ranked: {len(retrieved_docs)} docs kept from {TOP_K}")
        # for d in retrieved_docs:
        #   print(f"-> Score {d['similarity_score']:.3f}")
        

      else:
        print("No documents found")

      return retrieved_docs

    except Exception as e:
      print(f"Error during retrieval: {e}")
      return []




# class HybridRetriever:
#   def __init__(self, chunks, vector_store):
#     self.chunks= chunks
#     self.vector_store= vector_store
#     tokenized_documents=[
#         chunk["text"].lower().split()
#         for chunk in chunks
#     ]
#     self.bm25= BM25Okapi(tokenized_documents)

#   def keyword_search(self, query, top_k= TOP_K):
#     tokens= query.lower().split()
#     scores= self.bm25.get_scores(tokens)
#     ranked_indices= scores.argsort()[::-1][:top_k]
#     results=[]

#     for index in ranked_indices:
#       results.append({
#           "chunk": self.chunks[index],
#           "score": float(scores[index])
#       })

#     return results

# def build_context(documents):
#   context=""

#   for i, document in enumerate(documents):
#     context += f"""
#     SOURCE {i+1}
#     File: {document["metadata"]["source"]}
#     Page: {document["metadata"]["page"]}
#     Content: {document["page_content"]}

#     {document['text']}
#     """
#   return context  