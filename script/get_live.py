import requests

def fetch_remote_m3u(url, group_name):
    """拉取远程m3u，强制给该来源全部频道打上指定分组"""
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
                    channels.append({
                        "name": name,
                        "url": line,
                        "group": group_name
                    })
                    name = ""
        return channels
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return []

def gen_m3u(channels):
    lines = ["#EXTM3U"]
    for ch in channels:
        lines.append(f"#EXTGRP:{ch['group']}")
        lines.append(f"#EXTINF:-1,{ch['name']}")
        lines.append(ch["url"])
    return "\n".join(lines)

if __name__ == "__main__":
    # 格式：(源地址, 分组名称)
    source_list = [
        ("https://live.445569.xyz/live.m3u", "央卫视直播1"),
        ("https://gh-proxy.com/https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt", "央卫视直播2"),
        ("https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u")
    ]

    all_channels = []
    for url, group in source_list:
        chs = fetch_remote_m3u(url, group)
        all_channels.extend(chs)

    data = gen_m3u(all_channels)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(data)
    print(f"完成！一共合并 {len(all_channels)} 个频道，已按来源划分分组")
