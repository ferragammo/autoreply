import asyncio

from fastapi import Request

from auto_reply.api.agent.agent import ReplyAgent
from auto_reply.api.agent.db_requests import get_message_history
from auto_reply.api.hubspot import hubspot_router
from auto_reply.api.hubspot.utils import get_ticket_content, create_note_for_ticket


@hubspot_router.post("/ticket")
async def process_ticket(
    request: Request,
):
    payload = await request.json()
    ticket_id = payload[0].get('objectId')
    content, history = await asyncio.gather(
        get_ticket_content(ticket_id),
        get_message_history(ticket_id)
    )
    agent = ReplyAgent(history)
    agent_response = await agent.run(content)
    response = await create_note_for_ticket(agent_response, ticket_id)
    return response


