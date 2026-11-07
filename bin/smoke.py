"""在随机本地端口短暂启动服务，检查 HTTP 后停止本次子进程。"""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, build_opener


def main():
    root = Path(__file__).resolve().parents[1]
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, XQQJ_HOST="127.0.0.1", XQQJ_PORT=str(port), PYTHONIOENCODING="utf-8")
    process = subprocess.Popen(
        [sys.executable, "app_server.py"], cwd=root, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    # 本机自检直接连接 loopback，避免用户的系统 HTTP 代理转发本地请求。
    opener = build_opener(ProxyHandler({}))
    base = f"http://127.0.0.1:{port}"
    failure = None
    try:
        last_error = None
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("Server exited before ready")
            try:
                with opener.open(base + "/api/health", timeout=1) as response:
                    health = json.load(response)
                break
            except HTTPError:
                raise
            except (URLError, TimeoutError) as error:
                last_error = error
                time.sleep(0.1)
        else:
            raise RuntimeError(f"Server not ready: {last_error}")
        assert health["ok"] and health["data"]["schema_version"] == 1
        for path, status, code in [
            ("/api/food/items", 501, "NOT_IMPLEMENTED"),
            ("/api/missing", 404, "NOT_FOUND"),
        ]:
            try:
                opener.open(base + path, timeout=2)
                raise AssertionError("Unexpected success")
            except HTTPError as error:
                body = json.load(error)
                assert error.code == status and body["error"]["error_code"] == code
        print("HTTP smoke passed: health 200, business placeholder 501, missing route 404.")
    except BaseException as error:
        failure = error
        raise
    finally:
        process.terminate()
        try:
            output, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate(timeout=5)
        if failure:
            print(output.decode("utf-8", errors="replace"), file=sys.stderr)
        print("Smoke server stopped.")


if __name__ == "__main__":
    main()
