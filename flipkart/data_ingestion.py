from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:
    def __init__(self):
        self.embeddings = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vector_store = AstraDBVectorStore(
            embedding=self.embeddings,
            api_endpoint=Config.ASTRA_DB_ENDPOINT,
            collection_name="flipkart_database",
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE)
    def ingest(self,load_existing: bool = True):
        if load_existing:
            return self.vector_store
        
        documents = DataConverter("data/flipkart_product_review.csv").convert()
        self.vector_store.add_documents(documents)
        return self.vector_store
