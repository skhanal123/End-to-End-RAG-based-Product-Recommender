from openai import OpenAI
from .config import settings
import ast


def openai_chatAnalyzer(conversation_hist):
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """
                You are a helpful assistant that analyse the conversation history provided by user and answer below questions in one sentence. Start your response with "Yes," or "No,"
                Answer format:
                {
                "Feedback": "Response to question 1",
                "Response": "Response to question 2"
                }
                
                Questions:
                Question 1: Did customer provide any feedback on recommendation?
                Question 2: Did customer mention any preference on product attribute?
            """,
                    }
                ],
            },
            {"role": "user", "content": [{"type": "text", "text": conversation_hist}]},
        ],
    )

    string_res = response.choices[0].message.content

    res = ast.literal_eval(string_res)

    return res
