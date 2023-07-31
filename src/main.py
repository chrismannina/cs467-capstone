import os 

from config import Config
from document import Document
from vectorstore import Vectorstore

        
# def main():
#     # Load configuration
#     config = Config("config.yaml")
    
#     # Load and split document
#     doc = Document(
#         document_path=config.filepath, 
#         split_method=config.split_method, 
#         chunk_size=int(config.chunk_size),
#         chunk_overlap=int(config.chunk_overlap)
#         )
    
#     # Create vectorstore
#     db = Vectorstore()
#     if check_if_files_exist():
#         db.load()
#     else: 
#         db.create_from_docs(doc.get_split_document())
#         db.save()

def check_if_files_exist():
    directory = "db"
    files = ["index.faiss", "index.pkl"]
    # Check if directory exists
    if os.path.isdir(directory):
        # Check if all files exist
        if all(os.path.isfile(os.path.join(directory, file)) for file in files):
            return True
    return False

def example1():
    # Load configuration
    config = Config("config.yaml")
    
    # Load and split document
    doc = Document(
        document_path=config.filepath, 
        split_method=config.split_method, 
        chunk_size=int(config.chunk_size),
        chunk_overlap=int(config.chunk_overlap)
        )
    
    # Create vectorstore
    db = Vectorstore()
    if check_if_files_exist():
        db.load()
    else: 
        db.create_from_docs(doc.get_split_document())
        db.save()
    
    query_search = db.similarity_search_with_score("Cost of metoprolol", 10)
    print("*******")
    for idx, res in enumerate(query_search):
        print("Num: ", idx)
        print("Result: ", res[0])
        print("Score: ", res[1])
        print("*******")
    # print(db.similarity_search_with_score("Cost of atenolol", 10))
    
def example2():
    # Load configuration
    config = Config("config.yaml")
    
    # Load and split document
    doc = Document(
        document_path=config.filepath, 
        split_method=config.split_method, 
        chunk_size=int(config.chunk_size),
        chunk_overlap=int(config.chunk_overlap)
        )
    chunks = doc.get_split_document()
    chunks_ids = doc.get_ids()
    print("*******")
    for i in range(len(chunks_ids)):
        print("Chunk ID: ", chunks_ids[i])
        print("Chunk Document: ", chunks[i])
        print("*******")
    
    # Create vectorstore
    db = Vectorstore()
    if check_if_files_exist():
        db.load()
    else: 
        db.create_from_docs(doc.get_split_document())
        db.save()
    # print(db.add_docs(chunks))
 
if __name__ == "__main__":
    while True:
        example = input("Enter the # example you want to try. Enter 0 to exit.\n")
        if example == '1':
            example1()
        elif example == '2':
            example2()
        elif example == '0':
            break
