# MCP IMPLEMENTATION #

You job is to implement an MCP server based on nobra_calculatior API, wich was wrote in python with FastAPI. In order to do so you will use the fastapi-mcp lib, wich convert every FastAPI route into a MCP tool without the manual work. We will use the same server the serve both the API and the MCP - it is easier this way. We can instance them both in the main.py file without much more code. We already downloaded th fastapi-mcp into the venv. Also, already set the operation_id in each route.
We will use exclude_operations key for excluding the route /api/reload (operation_id=reload_scores) from the MCP tools, in order to avoid abuse.

## GUIDE ##

The nobra_calculator repo implements a typical FastAPI application with routers for health checks (/health, /health/status), an API router for listing and retrieving scores (/api/scores, /api/scores/{score_id}, /api/reload, /api/categories), and individual score endpoints such as /amt_10 and /aims. FastAPI‑MCP can automatically expose these endpoints as Model Context Protocol (MCP) tools with minimal changes.

1 Install fastapi‑mcp
Use pip or uv to install the library:

bash
Copiar
Editar
pip install fastapi-mcp  # or uv add fastapi-mcp
The library is FastAPI‑native and works by introspecting your FastAPI app and converting routes into MCP tools
GitHub
.

2 (Recommended) Define explicit operation IDs
When FastAPI‑MCP exposes your endpoints as tools, it uses the operation ID of each route as the tool name. If you don’t provide an explicit operation_id, FastAPI generates names like read_user_users__user_id__get, which are difficult for AI agents to understand. It’s better to set clear operation IDs in your route decorators:

python
Copiar
Editar
# app/routers/health.py
@router.get("/", response_model=HealthResponse, operation_id="health_check")
async def health_check():
    ...

@router.get("/status", response_model=HealthResponse, operation_id="health_status")
async def get_status():
    ...

# app/routers/api_routes.py
@router.get("/scores", operation_id="list_scores")
async def list_scores(...):
    ...

@router.get("/scores/{score_id}", operation_id="get_score_metadata")
async def get_score_metadata(score_id: str):
    ...

@router.post("/reload", operation_id="reload_scores")
async def reload_scores():
    ...

@router.get("/categories", operation_id="list_categories")
async def list_categories():
    ...

# app/routers/scores/geriatrics/amt_10.py
@router.post("/amt_10", response_model=Amt10Response, operation_id="amt_10")
async def calculate_amt_10(request: Amt10Request):
    ...

# app/routers/scores/psychiatry/aims.py
@router.post("/aims", response_model=AimsResponse, operation_id="aims")
async def calculate_aims(request: AimsRequest):
    ...
Adding operation IDs improves the readability of tool names
apidog.com
 and is optional but recommended.

3 Create and mount the MCP server
Wrap your existing FastAPI app in a FastApiMCP instance. The library generates the tool definitions automatically and mounts a new /mcp endpoint. There are two approaches:

3.1 Mount to the same FastAPI app
If you are comfortable serving your API and MCP server together, import and mount FastApiMCP in main.py:

python
Copiar
Editar
from fastapi_mcp import FastApiMCP

# ... existing FastAPI setup ...

# Create the MCP server from the existing app
mcp = FastApiMCP(
    app,
    name="Nobra Calculator MCP",            # human‑friendly name
    description="MCP server exposing medical scores and calculators",  # description shown to clients
)

# Mount the MCP server onto the same FastAPI app
mcp.mount()

# Optionally refresh the MCP server after adding new endpoints later
# mcp.setup_server()
Mounting the MCP server is enough—FastAPI‑MCP will scan the app and automatically expose each route as an MCP tool
GitHub
. The tools will be available at /mcp (for example, http://localhost:8000/mcp), and MCP clients such as Claude Desktop or Cursor can discover them via server‑sent events
apidog.com
.

3.2 Deploy the MCP server separately (optional)
If you prefer to run the API and the MCP server as separate services, create a second FastAPI app for the MCP endpoints:

python
Copiar
Editar
# main.py
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from nobra_calculator.main import app as api_app  # import your existing API app

api_app = api_app  # your existing FastAPI app
mcp_app = FastAPI()  # a new app to host the MCP server

mcp = FastApiMCP(
    api_app,
    name="Nobra Calculator MCP",
    base_url="http://api-host:8001"  # URL where api_app will run
)

# Mount MCP to the separate mcp_app
mcp.mount(mcp_app)

# run api_app on 8001 and mcp_app on another port
This separation may help when you want to scale or secure the MCP server independently
apidog.com
.

4 Filtering which endpoints become tools
By default, FastAPI‑MCP exposes all endpoints. If you only want to expose certain operations (for example, the public score and health endpoints) or want to hide internal endpoints (like /api/reload), use the include_operations, exclude_operations, include_tags or exclude_tags parameters when constructing FastApiMCP
apidog.com
. For example:

python
Copiar
Editar
# only expose health and score tools
tool_ids = [
    "health_check",
    "health_status",
    "list_scores",
    "get_score_metadata",
    "list_categories",
    "calculate_amt_10",
    "calculate_aims"
]

mcp = FastApiMCP(
    app,
    name="Nobra Calculator MCP",
    base_url="http://localhost:8000",
    include_operations=tool_ids,
    # you can also use include_tags=["scores", "health"] because your routers are tagged
)
Alternatively, use exclude_operations to omit tools such as reload_scores that should not be publicly accessible.

5 Run and connect
Run your FastAPI application with uvicorn main:app --host 0.0.0.0 --port 8000 (or with a separate mcp_app on a different port if using the separate deployment).

Verify the MCP server by visiting /mcp in a browser or by connecting an MCP client. The endpoint will return a JSON describing each tool (name, description, input schema and output schema). Tools will use the operation IDs you defined as names.

Configure your AI client (e.g., Claude Desktop or Cursor IDE) to point to http://localhost:8000/mcp. For clients without built‑in SSE support, use mcp-proxy and configure it as shown in the Apidog article
apidog.com
.

Summary
FastAPI‑MCP makes it straightforward to expose your existing FastAPI endpoints as Model Context Protocol tools. Install the package, optionally assign clear operation_ids to your routes, instantiate FastApiMCP with your existing FastAPI app, and mount the MCP server. With optional filters, you can control which endpoints become tools, and you can mount the MCP server either within your existing API or as a separate service. Once mounted, the /mcp endpoint will serve tool definitions that AI agents can call, enabling your medical calculator API to be used seamlessly by MCP‑enabled clients.