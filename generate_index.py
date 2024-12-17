from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

# Load documents and build index
# documents = SimpleDirectoryReader(
#     "docs"
# ).load_data()
# index = VectorStoreIndex.from_documents(documents)
# index.storage_context.persist(persist_dir="vectorstorage")

# Load index from Storage
storage_context = StorageContext.from_defaults(persist_dir="vectorstorage")
index = load_index_from_storage(storage_context)

# Simple retriever test
retriever = index.as_retriever()
nodes = retriever.retrieve('Assessoria Especial de Desenvolvimento Econômico')
print(nodes)