from ..database import PineconeEngine, chat_store
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.vector_stores.pinecone import PineconeVectorStore
from ..userProfile import update_userProfile, fetch_userProfile
from ..chatAnalyzer import openai_chatAnalyzer
from ..utils import parse_chat_store
from llama_index.core.memory import ChatMemoryBuffer
from fastapi import APIRouter, Depends
from .. import schemas, oauth2
from ..config import settings

router = APIRouter(tags=["chat"])

## Temp block: Below persist_dir & profile is used only when block 1 is uncommented for usage of in-memory vector index - starts
PERSIST_DIR = "C:\\Users\\skhan\\Documents\\GITHUB\\LLAMAINDEX\\productRecommender\\app\\routers\\sample_vectordb"

profile = {
    "user_id": "user_1",
    "preferences": {
        "categories": ["Powerful Laptop", "bluetooth"],
        "brands": ["Apple Mac Book", "HP"],
    },
    "past_interactions": ["Bose QuietComfort 35 II", "Sony WH-1000XM4"],
    "past_purchase": ["Apple Mac Book"],
}

## Temp block - ends


def chat_engine(index, user_profile, user_name):
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key=user_name,
    )

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=chat_memory,
        system_prompt=(
            f"You are a chatbot that provides personalized responses based on the provided context and below user profile, "
            f"{user_profile}"
            f"Please ask user to rate your recommendation to understand whether user liked it or not"
        ),
    )

    return chat_engine


@router.post("/chat", response_model=schemas.ChatResponse)
async def product_recommender(
    query: schemas.ChatQuery, current_user: int = Depends(oauth2.get_current_user)
):
    user_query = query.model_dump()

    ## Block 1: Uncomment the below block to use the vector index from in-memory - starts
    # storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    # index = load_index_from_storage(storage_context)
    ## Block 1: ends

    ## Block 2: Uncomment the below block to used the vector index from pincone database - starts
    pinecone_index = PineconeEngine.client.Index(settings.pinecone_index)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    ## Block 2: ends

    user_name = current_user.user_name
    profile = fetch_userProfile(user_name)
    chat_agent = chat_engine(index, profile, user_name)
    if user_query["query"] == "reset":

        # Retrieve the conversation for analysis loop before chat engine reset
        conversation_hist = parse_chat_store(chat_store.get_messages(user_name))

        # Send conversation for analysis and update user profile if anything new is discovered
        chat_analysis = openai_chatAnalyzer(conversation_hist)
        print(chat_analysis)
        update_userProfile(user_name, chat_analysis)

        # Reset the chat engine
        chat_agent.reset()
        return {"response": "This conversation is successfully reset"}
    else:
        response = chat_agent.chat(user_query["query"])
        return {"response": str(response)}
