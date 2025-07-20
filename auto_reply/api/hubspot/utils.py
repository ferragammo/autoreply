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