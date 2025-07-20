import pydash

from langchain_core.messages import HumanMessage, AIMessage
from langchain_mongodb import MongoDBChatMessageHistory

from auto_reply.core.config import settings


async def save_messages(
        query: str, response: dict, message_history: MongoDBChatMessageHistory
) -> None:
    await message_history.aadd_messages(
        [
            HumanMessage(content=query),
            AIMessage(
                content=response["output"],
                additional_kwargs={"moduleResponse": pydash.get(response, "intermediate_steps[-1][-1]", None)},
            ),
        ]
    )


async def get_message_history(ticket_id: str) -> MongoDBChatMessageHistory:
    return MongoDBChatMessageHistory(
        session_id=ticket_id,
        client=settings.MONGO_CLIENT,
        connection_string=None,
        session_id_key="sessionId",
        database_name="reply",
        collection_name="messages",
    )
