# Project Plan / Ideas / TODO

**UI**
- Should have ability to add a document
- Document should be saved on a left navigation pane
- Document metadata should be avaiable for viewing so individuals can select between documents 
- Also ability to upload multiple documents and have users query from all documents 
- Ability for new chats to be started, then return to previous chat

**Backend**
- [Context Compression](https://blog.langchain.dev/improving-document-retrieval-with-contextual-compression/)
  - Add a document compressor. Instead of immediately returning retrieved documents as-is, we can compress them using the context of the given query so that only the relevant information is returned.

**TODO**
- Clean up code base and backend
- Allow for multiple documents to be uploaded/ingested
- Allow for user to load a DB, save a DB, or ingest multiple docs
- Add citations for sources / another chat box to see the returned context
- Logging and debugging info
- Improve metadata to have title, description, authors, page #s
- Create docs for llm chains being used
- utils.py for formatting functions, doc adding, etc.
- Issue with how metadata is gathered from the PDF when uploaded through Gradio - I lose page numbers
- Implement chat mode vs single QA mode. There may be benefit to single QA mode. 

To complete capstone:
1. Update UI 
   1. Need settings tab
   2. Add document tab
   3. Create vectorstore and add document etc
   4. Ability to switch between single chat qa and chat with history
   5. place to show citations, etc
   6. place to change prompts etc
   7. 
2. CLI tools for checking
   1. Pass in a JSON (?) file with all questions. Get returned a file with questions, answers, retrieved docs, scores for them, and gpt3.5, gpt4 answers without docs

### improvment ideas for similarity search:
Some common ways to improve on vector similarity search include:

MultiQueryRetriever generates variants of the input question to improve retrieval.
Max marginal relevance selects for relevance and diversity among the retrieved documents.
Documents can be filtered during retrieval using metadata filters.


retrieval:
chains -
1) [RetrievalQA](https://api.python.langchain.com/en/latest/chains/langchain.chains.retrieval_qa.base.RetrievalQA.html#langchain.chains.retrieval_qa.base.RetrievalQA)
2) [ConversationalRetrievalChain](https://api.python.langchain.com/en/latest/chains/langchain.chains.conversational_retrieval.base.ConversationalRetrievalChain.html#langchain.chains.conversational_retrieval.base.ConversationalRetrievalChain)
3) [RetrievalQAWithSourcesChain](https://api.python.langchain.com/en/latest/chains/langchain.chains.qa_with_sources.retrieval.RetrievalQAWithSourcesChain.html#langchain.chains.qa_with_sources.retrieval.RetrievalQAWithSourcesChain)
4) [MultiRetrievalQAChain](https://api.python.langchain.com/en/latest/chains/langchain.chains.router.multi_retrieval_qa.MultiRetrievalQAChain.html#langchain.chains.router.multi_retrieval_qa.MultiRetrievalQAChain)
