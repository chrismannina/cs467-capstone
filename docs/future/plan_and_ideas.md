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

### Roadmap 

1. **Core Functionalities and User Experience**:

   - **docstrings and comments throughout**: Ensuring that your code is well-documented is a foundational step that aids all subsequent developments.
   - **readme**: Essential for users and developers to understand how to use the application.
   - **ability for user to enter their own api key**: Critical for user customization and possibly essential depending on how your application interacts with external services.
   - **document, vectorstore, chat manager classes**: Core architectural improvements that can enhance the application's modularity and expandability.
   - **functionality to upload docx and txt as well**: Expanding file support is crucial for usability.
   - **functions to clean documents and splits**: Improves the quality of input data and can enhance the results.
   - **options for other splitters**: Essential for different types of documents.
   - **options for characters to recursively split by**: Provides flexibility in data processing.
   - **options to change the prompts in UI**: Enhances user experience by allowing customization.
   - **more options for file uploads**: Increases usability for different users.
   - **api key for ui**: ability for user to enter their own api key

2. **Extended Features**:

   - **evaluation suite**: being able to have a list of questions to feed in. having the responses generated. then compare against no doc retrieval. have it save the settings for the run and print it. perhaps havingthe real answer avail and running that again through gpt to compare the real answer vs generated to give a score?
     - Evaluation using a combination of metrics such as retrieval accuracy, string similarity, and model-generated response correctness
   - **functions to clean documents and splits**: function to send the document to chatgpt with a prompt to clean? users can maybe choose or add to settings

3. **Operational and Maintenance Improvements**:

   - **docker?**: Makes deployment and scaling easier.
   - **poetry?**: A dependency management tool that can simplify setting up and maintaining the project environment.
   - **ci/cd**: Ensures continuous testing and deployment, improving the development lifecycle.
   - **cleanup notebook examples**: Important for clarity, especially if sharing with other developers or users.

4. **Future Enhancements**:

   - **function to send the document to chatgpt with a prompt to clean?**
   - **discord bot**: Extending the application's reach to a popular platform.
   - **teams bot**: Useful for internal company usage and collaboration.
