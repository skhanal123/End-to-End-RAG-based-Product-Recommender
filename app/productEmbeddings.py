from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from .database import PineconeEngine
from .config import settings


def create_embeddings(product_details: dict):

    new_doc = [Document(text=str(v)) for _, v in product_details.items()]

    try:
        pinconeClient = PineconeEngine(api_key=settings.pinecone_api_key)
        pinecone_index = pinconeClient.Index(settings.pinecone_index)

        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        pinecone_index = VectorStoreIndex.from_documents(
            new_doc, storage_context=storage_context
        )

        return {"message": "Product embeddings created and stored successfully!"}

    except Exception as e:
        return {"message": "Product embeddings creation and upload failed!"}
