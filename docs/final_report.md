### Medical Document Querying Using Language Models and Vector Stores
#### Final Report
- **Project Name**: Medical Document Querying Using Language Models and Vector Stores
- **Team Member**: Chris Mannina
- **Course**: CS467 Capstone, Oregon State University
- **Date**: August 15th, 2023

---

**Introduction**:
In recent years, Large Language Models (LLMs) have revolutionized the world of artificial intelligence, proving their mettle across various domains. As these models burgeon in capabilities and adoption, their integration into the intricate world of healthcare is inevitable, albeit gradual. Medical guidelines, known for their vastness and complexity, are quintessential examples of documents that demand significant time and expertise for comprehension. The project's genesis lies in the aspiration to harness the prowess of LLMs to decipher such medical documents. By creating a system that allows users to pose direct questions about extensive guidelines, the project aims to bridge the gap between voluminous medical literature and concise, relevant information.

---

**Software Description (User's Perspective)**:
The software offers a streamlined platform where users can upload medical documents. Once ingested, the document's text undergoes segmentation into bite-sized sections, making it ready for queries. Users can then direct questions, with the system harnessing a powerful language model in conjunction with the segmented document to deliver insightful answers.

---

**Development Efforts vs. Project Plan**:
The project's conception revolved around a simple Q&A system. However, the intricate nature of medical guidelines and inherent limitations of language models, such as token constraints, necessitated numerous adjustments. The incorporation of vector stores and modular prompts emerged as solutions, enhancing the system's efficiency and fidelity.

---

**Software Libraries & Tools**:
- **Languages**: Python
- **Libraries**: Streamlit, FAISS, Chroma, LangChain
- **APIs**: OpenAI
- **Development Tools**: [Specific IDEs/tools can be inserted here]
- **Servers**: [If applicable]

---

**Team Contributions**:
- **Chris Mannina**: Spearheaded the project's conceptualization, design, and execution. Managed the intricate integration of vector stores, crafted the user interface, and was pivotal in testing and optimizing the solution.

---

**Project Continuance**:
- **Current Release Challenges**: Extracted text from PDFs often contains noise and lacks structure, leading to suboptimal embeddings and potential semantic loss. This dirty data can also strain ChatGPT's interpretation capabilities.
- **Next Phase Priorities**: Implementing an evaluation framework for optimizing text splitting and prompt configurations, refining the text extraction process, and potentially transitioning away from LangChain for a more bespoke solution.

---

**Limitations & Future Directions**:
The project, while groundbreaking, faces challenges. The unstructured nature of PDF text extraction occasionally hinders the accuracy of responses. Furthermore, the plethora of combinations related to chunk size, overlap, and text splitting methods necessitates a robust evaluation mechanism. An envisaged solution involves pre-defined questions and answers, testing the system's accuracy across various configurations. Additionally, the dynamic nature of prompts requires rigorous tuning. A potential avenue is the development of an LLM-based accuracy judgment system. Despite using LangChain for certain functionalities, a production-ready application might benefit from a homegrown solution, given the rapid evolution of the LangChain package.

---

**Conclusion**:
The endeavor to synergize LLMs with medical documents marks a significant stride in healthcare and AI integration. While challenges persist, the project's foundation promises a future where medical professionals can swiftly glean insights from extensive guidelines. With continued refinement and iteration, this system can serve as a beacon for AI-driven medical literature interpretation.

---

**Installation Document**:
1. **Access**: [Website link or software download link]
2. **Test Credentials**: Username: [Test Username], Password: [Test Password]

---

**Instructions Document**:
1. **Accessing the System**: Navigate to [Website link] or initiate the installed software.
2. **Uploading a Document**: [Screenshot highlighting upload] Select the 'Upload' option and choose your medical document.
3. **Posing a Question**: [Screenshot of query interface] Input your question in the dedicated space.
4. **Retrieving the Answer**: The system will promptly display an answer derived from the document's content.

---

This comprehensive report encapsulates the essence, challenges, innovations, and aspirations of your project. Should any sections require further elaboration or modifications, please let me know!