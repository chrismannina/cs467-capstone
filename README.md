# File Q&A Using Embeddings + ChatGPT

## How it works
When a file is uploaded, text is extracted from the file. This text is then split into shorter text chunks, and an embedding is created for each text chunk. When the user asks a question, an embedding is created for the question, and a similarity search is performed to find the file chunk embeddings that are most similar to the question (i.e. have highest cosine similarities with the question embedding). An API call is then made to the completions endpoint, with the question and the most relevant file chunks are included in the prompt. The generative model then gives the answer to the question found in the file chunks, if the answer can be found in the extracts.

## Limitations
The app may sometimes generate answers that are not in the files, or hallucinate about the existence of files that are not uploaded.