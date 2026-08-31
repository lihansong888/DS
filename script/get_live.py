import requests
import re

# ========== 分组匹配规则 ==========
GROUP_RULES = [
    ("央视", r"CCTV|央视|CGTN|央视频"),
    ("卫视频道", r"卫视"),
    ("地方台", r"省|市|本地|都市"),
    ("港澳台", r"香港|台湾|澳门|中视|大亚|港台"),
    ("电影直播", r"电影|影院|影视轮播|院线"),
    ("剧集直播", r"剧集|电视剧|连续剧"),
    ("综艺直播", r"综艺|娱乐|秀场"),
    ("体育直播", r"体育|足球|篮球|球赛|赛事"),
    ("卡通少儿", r"卡通|少儿|动画|儿童"),
    ("戏曲直播", r"戏曲|京剧|越剧|豫剧|黄梅戏"),
    ("音乐直播", r"音乐|DJ|老歌|热歌|MV"),
    ("舞蹈直播", r"舞蹈|跳舞"),
    ("资讯新闻", r"新闻|资讯|时事"),
    ("纪实科教", r"纪实|科教|纪录片|历史"),
    ("生活财经", r"财经|生活|美食|健康"),
    ("怀旧轮播", r"怀旧|老电视|老节目"),
    ("其他直播", r".*")
]

# 强制例外映射，优先级最高
FORCE_MAP = {
    "舞蹈直播1": "卫视频道",
    "舞蹈直播2": "卫视频道"
}

def match_group(channel_name):
    if channel_name in FORCE_MAP:
        return FORCE_MAP[channel_name]
    for g_name, pat in GROUP_RULES:
        if re.search(pat, channel_name):
            return g_name
    return "其他直播"

def fetch_remote_m3u(url):
    """拉取单个远程m3u，返回频道列表"""
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
                if len(parts) >= 2:
                    name = parts[1].strip()
            elif line and not line.startswith("#"):
                if name:
                    g = match_group(name)
                    channels.append({
                        "name": name,
                        "url": line,
                        "group": g
                    })
                    name = ""
        return channels
    except Exception as e:
        print(f"【警告】拉取 {url} 失败: {e}")
        return []

def build_m3u(all_channels):
    out = ["#EXTM3U"]
    for ch in all_channels:
        out.append(f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}')
        out.append(ch["url"])
    return "\n".join(out)

if __name__ == "__main__":
    # ========== 这里填入你的3个远程源地址 ==========
    REMOTE_URLS = [
        "https://live.445569.xyz/live.m3u",
        "https://gh-proxy.com/https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
    ]

    total_channels = []
    for url in REMOTE_URLS:
        print(f"正在拉取：{url}")
        chs = fetch_remote_m3u(url)
        total_channels.extend(chs)

    m3u_text = build_m3u(total_channels)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_text)
    print(f"✅ 全部完成，共合并 {len(total_channels)} 个频道，输出 live.m3u")
        
