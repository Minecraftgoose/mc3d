#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全景图格式转换器（双击运行）
=============================
规则：
  目录里全是 .png  -> 全部转成 .webp（质量90）
  目录里全是 .webp -> 全部转成 .png
  混合 / 没有图片  -> 提示后退出

转换成功后删除源文件（目录保持单一格式）。
需要 PIL（pillow）。若当前 python 没有 PIL，会自动尝试
用系统 Python 3.11 重新运行本脚本。
"""
import os
import sys
import glob
import subprocess

# 让中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 自动寻找带 PIL 的 python 并重启（双击到的解释器可能没装 pillow）
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

if not HAS_PIL:
    candidates = [
        sys.executable,
        r"C:\Users\BayMax\AppData\Local\Programs\Python\Python311\python.exe",
        r"C:\Program Files\Python311\python.exe",
        r"C:\Python311\python.exe",
    ]
    seen = set()
    for cand in candidates:
        if not cand or cand in seen:
            continue
        seen.add(cand)
        try:
            r = subprocess.run(
                [cand, "-c", "from PIL import Image; print('ok')"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode == 0 and "ok" in r.stdout:
                os.execv(cand, [cand] + sys.argv)
        except Exception:
            continue
    print("[错误] 找不到带 PIL 的 Python。")
    print("请安装 pillow 后重试：pip install pillow")
    input("按回车退出...")
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    pngs = sorted(glob.glob("*.png"))
    webps = sorted(glob.glob("*.webp"))

    if pngs and not webps:
        target = "webp"
        sources = pngs
    elif webps and not pngs:
        target = "png"
        sources = webps
    elif not pngs and not webps:
        print("目录里没有 .png / .webp 图片，无事可做。")
        input("按回车退出...")
        return
    else:
        print(f"目录里混合存在 {len(pngs)} 张 png 和 {len(webps)} 张 webp，")
        print("请先手动统一成一种格式再运行本脚本。")
        input("按回车退出...")
        return

    print(f"检测到 {len(sources)} 张 {target.upper()} 即将转换...")
    ok = 0
    fail = []
    for p in sources:
        stem = os.path.splitext(p)[0]
        out = stem + "." + target
        try:
            img = Image.open(p)
            if target == "webp":
                img.save(out, "WEBP", quality=90, method=4)
            else:
                img.save(out, "PNG")
            img.close()
            os.remove(p)  # 转换成功才删源文件
            ok += 1
            print(f"  已转换: {p} -> {out}")
        except Exception as e:
            fail.append((p, str(e)))
            print(f"  失败: {p} -> {e}")

    print("-" * 40)
    print(f"完成: 成功 {ok} / {len(sources)}")
    if fail:
        print("失败列表:")
        for p, e in fail:
            print(f"  {p}: {e}")
    input("按回车退出...")


if __name__ == "__main__":
    main()
