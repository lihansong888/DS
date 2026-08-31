import requests

def fetch_remote_m3u(url):
    """拉取远程m3u/txt，解析全部频道"""
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        channels = []
        name = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                parts = line.split(",", 1)
                if len(parts)>=2:
                    name = parts[1].strip()
            elif line and not line.startswith("#"):
                if name:
                    channels.append({"name": name, "url": line})
                    name = ""
        return channels
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return []

def gen_m3u(channels):
    lines = ["#EXTM3U"]
    for ch in channels:
        lines.append(f"#EXTINF:-1,{ch['name']}")
        lines.append(ch["url"])
    return "\n".join(lines)

if __name__ == "__main__":
    # 这里放你全部3个源地址，你可以自行增删
    source_urls = [
        "https://live.445569.xyz/live.m3u",
        "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
    ]

    all_channels = []
    for u in source_urls:
        chs = fetch_remote_m3u(u)
        all_channels.extend(chs)

    data = gen_m3u(all_channels)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(data)
    print(f"总共抓取合并 {len(all_channels)} 个频道")
