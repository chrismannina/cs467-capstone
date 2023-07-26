from config import Config
from document import Document
from vectorstore import Vectorstore

def main():
    # Load configuration
    config = Config("config.yaml")
    
    # Load and split document
    doc = Document(
        document_path=config.filepath, 
        split_method=config.split_method, 
        chunk_size=int(config.chunk_size),
        chunk_overlap=int(config.chunk_overlap)
        )
    # chunks = doc.get_split_document()
    # print("True") if chunks is not None else print("False")
    # chunks_ids = doc.get_ids()
    # print(chunks_ids)
    # Create vectorstore
    db = Vectorstore()
    # db.create_from_docs(doc.get_split_document())
    # db.save()
    db.load()
    # print(db.add_docs(chunks))
    query_search = db.similarity_search_with_score("Cost of metoprolol", 10)
    print("*******")
    for idx, res in enumerate(query_search):
        print("Num: ", idx)
        print("Result: ", res[0])
        print("Score: ", res[1])
        print("*******")
    # print(db.similarity_search_with_score("Cost of atenolol", 10))
 


if __name__ == "__main__":
    main()
