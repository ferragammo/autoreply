import httpx

from auto_reply.core.config import settings


async def get_ticket_content(ticket_id: str) -> str:
    url = f'https://api.hubapi.com/crm/v3/objects/tickets/{ticket_id}'

    headers = {
        'Authorization': f'Bearer {settings.HUBSPOT_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            ticket_details = response.json()
            content = ticket_details['properties'].get('content', 'No content available')
            return content
        else:
            return f"Error: {response.status_code} - {response.text}"

    except httpx.RequestError as e:
        return f"Request error: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"


async def create_note_for_ticket(note_content: str, ticket_id: str) -> str:
    data = {
        "engagement": {
            "active": True,
            "type": "NOTE",
        },
        "metadata": {
            "body": note_content,
            "subject": f"Response to ticket (ID: {ticket_id})"
        },
        "associations": {
            "ticketIds": [int(ticket_id)],
        },
        "ownerId": settings.HUBSPOT_OWNER_ID
    }

    url = "https://api.hubapi.com/engagements/v1/engagements"

    headers = {
        'Authorization': f'Bearer {settings.HUBSPOT_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return "The note has been successfully created for ticket review"
    else:
        return "Error: {response.status_code} {response.text}"
