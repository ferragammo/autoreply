from fastapi import Request

from auto_reply.api.hubspot import hubspot_router
from auto_reply.api.hubspot.utils import get_ticket_content


@hubspot_router.post("/ticket")
async def add_transcription(
    request: Request,
):
    payload = await request.json()
    print(payload)
    ticket_id = payload[0].get('objectId')
    content = await get_ticket_content(ticket_id)
    print(content)
