#!/usr/bin/env python3
"""一键启动脚本"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  耘智链 - 多Agent智慧种植服务平台")
    print("  访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
