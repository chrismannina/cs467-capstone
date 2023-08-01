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