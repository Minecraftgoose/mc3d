#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键本地服务器启动器
========================
把本脚本 和 template.html + 全景图(1.jpg~6.jpg) 放在同一个文件夹，
然后双击本脚本：
  - 在脚本所在文件夹启动一个静态服务器
  - 自动打开浏览器访问 http://localhost:XXXX/template.html
  - 关闭窗口即停止服务器
纯 Python 标准库实现，不需要安装任何东西。
"""
import http.server
import socketserver
import webbrowser
import threading
import socket
import os
import sys
import time

# 用脚本所在目录作为服务器根目录（这样脚本拷到哪就 serve 哪）
ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8123


def find_free_port(start):
    """从 start 开始找空闲端口"""
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start  # 全被占用就用起始端口，反正 http.server 会报错


def main():
    port = find_free_port(PORT)

    # 多线程静态服务器，允许并发
    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = dict(
            http.server.SimpleHTTPRequestHandler.extensions_map,
            **{".webp": "image/webp"},
        )
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=ROOT, **kw)
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), Handler) as httpd:
        url = f"http://localhost:{port}/index.html"
        print("=" * 50)
        print("  本地服务器已启动")
        print(f"  根目录: {ROOT}")
        print(f"  访问地址: {url}")
        print("  关闭本窗口即可停止服务器")
        print("=" * 50)

        # 延迟一下，确保服务器就绪再开浏览器
        threading.Timer(0.5, webbrowser.open, args=[url]).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
            print("\n服务器已停止")


if __name__ == "__main__":
    # Windows 下双击运行时，避免控制台中文乱码（若系统是 GBK 编码）
    try:
        main()
    except Exception as e:
        # 出错时保留窗口，方便看报错
        print(f"\n[错误] {e}")
        print("按回车键退出...")
        input()
