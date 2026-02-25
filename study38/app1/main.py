from fastapi import FastAPI, Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import httpx 
from settings import settings

app = FastAPI(title=settings.title, docs_url=None)

SERVICE_MAP = {
  settings.app1_path: settings.app1_url,
  settings.app2_path: settings.app2_url,
}

client = httpx.AsyncClient(timeout=10.0)

class ReverseProxyMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    path = request.url.path
    service_url = None

    for prefix, url in sorted(SERVICE_MAP.items(), key=lambda x: -len(x[0])):
      if path.startswith(prefix):
        service_url = url
        path_suffix = path[len(prefix):] or "/"
        if not path_suffix.startswith("/"):
          path_suffix = "/" + path_suffix
        break

    # 프록시 대상이 없으면 404
    if not service_url:
      return await call_next(request)

    # 헤더 필터링
    excluded_headers = [
      "host", "connection", "keep-alive", "proxy-authenticate",
      "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"
    ]
    headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}

    # 요청 바디
    body = await request.body() if request.method in ("POST", "PUT", "PATCH") else None

    try:
      proxy_resp = await client.request(
        method=request.method,
        url=f"{service_url}{path_suffix}",
        headers=headers,
        content=body,
        params=request.query_params,
      )
      #response_headers = {k: v for k, v in proxy_resp.headers.items() if k.lower() not in excluded_headers}
      #return Response(
      #  content=proxy_resp.content,
      #  status_code=proxy_resp.status_code,
      #  headers=response_headers
      #)
      response_headers = [(k.encode("latin-1"), v.encode("latin-1")) for k, v in proxy_resp.headers.multi_items() if k.lower() not in excluded_headers]
      response = Response(
        content=proxy_resp.content,
        status_code=proxy_resp.status_code,
      )
      response.raw_headers = response_headers
      return response
    except httpx.RequestError as exc:
      print(f"Proxy error: {exc}")
      raise HTTPException(status_code=502, detail="Bad Gateway")

# 미들웨어 등록
app.add_middleware(ReverseProxyMiddleware)
