import requests

# 在这里添加你的所有源，一行一个，末尾加逗号
URL_LIST = [
        "https://live.445569.xyz/live.m3u",
        "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/bj123sd/hycg/refs/heads/main/tv.txt",
        "https://raw.githubusercontent.com/lihansong888/collect-tv-txt/refs/heads/main/bbxx_lite.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
]

def main():
    all_lines = ["#EXTM3U"]
    for url in URL_LIST:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            text = resp.text
            # 移除每个源自带的 #EXTM3U，避免重复
            content = text.replace("#EXTM3U", "").strip()
            if content:
                all_lines.append(content)
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}，跳过该源")

    final_text = "\n".join(all_lines)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(final_text)
    print("✅ 全部合并完成，已生成live.m3u")

if __name__ == "__main__":
    main()
