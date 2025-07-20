from fastapi import Request

from auto_reply.api.hubspot import hubspot_router


@hubspot_router.post("/ticket")
async def add_transcription(
    request: Request,
):
    payload = await request.json()
    print(payload)
