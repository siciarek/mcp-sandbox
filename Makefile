-include .env

setup:
	uv sync --frozen

bmi_srv:
	DANGEROUSLY_OMIT_AUTH=true uv run python mcp_server/bmi_srv.py

client:
	GOOGLE_API_KEY=$(GOOGLE_API_KEY) uv run python mcp_client/app.py
