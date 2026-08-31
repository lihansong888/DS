import requests

def fetch_sources():
    channels = [
        {"name":"Test Stream 1","url":"https://live.445569.xyz/live.m3u"},
        {"name":"Test Stream 2","url":"https://gh-proxy.com/https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt"}
    ]
    return channels

def gen_m3u(channels):
    lines = ["#EXTM3U"]
    for ch in channels:
        lines.append(f"#EXTINF:-1,{ch['name']}")
        lines.append(ch["url"])
    return "\n".join(lines)

if __name__ == "__main__":
    chs = fetch_sources()
    data = gen_m3u(chs)
    with open("live.m3u","w",encoding="utf-8") as f:
        f.write(data)
