from typing import Any
import httpx

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sandbox")


@mcp.tool()
async def get_country_info(name: str):
    url = f"https://restcountries.com/v3.1/name/{name}"
    headers = {
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
