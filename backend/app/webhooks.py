import httpx

WEBHOOK_URL = "http://host.docker.internal:3000/webhook"
REPO_URL = "https://github.com/Tsedevdorj94/fastapi-example.git"
async def send_webhook(traceback, repo_url = REPO_URL, repo_branch="dev", context=None):
    payload = {
        "traceback": traceback,
        "repo_url": repo_url,
        "repo_branch": repo_branch,
        "context": context
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(WEBHOOK_URL, json=payload, timeout=10)
    # Optionally handle/log response or errors
    return resp.status_code, resp.text