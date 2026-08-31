import requests

def fetch_sources():
    # 👉这里替换成你真实可用的直播源
    channels = [
        {"name":"测试频道1","url":"http://example.com/stream.m3u8"},
        {"name":"测试频道2","url":"http://example.com/stream2.m3u8"}
    ]
    return channels

def gen_m3u(channels):
    lines = ["#EXTM3U"]
    for ch in channels:
        lines.append(f'#EXTINF:-1,{ch["name"]}')
        lines.append(ch["url"])
    return "\n".join(lines)

if __name__ == "__main__":
    chs = fetch_sources()
    m3u_text = gen_m3u(chs)
    with open("../live.m3u","w",encoding="utf-8") as f:
        f.write(m3u_text)
