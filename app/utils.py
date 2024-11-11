from passlib.context import CryptContext
import ast

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    This function is used to created the hashed form of the password
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """
    This fuction is used to validated the password entered during login
    """
    return pwd_context.verify(plain_password, hashed_password)


def parse_chat_store(store_message):
    """
    This function is used to parse the conversation from chat store after every session and return the conversation in format required my chat analyzer
    """
    conversation_hist = """"""
    for i in store_message:
        j = ast.literal_eval(i.json())
        conversation_hist = conversation_hist + f'\n{j["role"]}:{j["content"]}'
    return conversation_hist
