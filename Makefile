-include .env

run:
	DANGEROUSLY_OMIT_AUTH=true uv run python mcp_server/bmi_srv.py

srv:
	DANGEROUSLY_OMIT_AUTH=true uv run mcp dev mcp_server/srv.py

client:
	GOOGLE_API_KEY=$(GOOGLE_API_KEY) uv run python mcp_client/app.py
