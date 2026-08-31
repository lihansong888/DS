import requests
import re

# ========== 分组匹配规则【顺序很重要，从上往下匹配，命中就停止】 ==========
GROUP_RULES = [
    ("快手直播", r"快手|kuaishou"),
    ("虎牙直播", r"虎牙|huya"),
    ("YY直播", r"YY|yy直播"),
    ("抖音直播", r"douyin|抖音|pull‑hls|thirdgame"),
    ("央视", r"CCTV|央视|CGTN|央视频|咪咕"),
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

# ========== 仅需要屏蔽的那一条特定频道名称 ==========
BLOCK_CHANNEL_NAME = "☁️官网地址jsnzkpg.com"

# ========== 开关：是否开启源连通检测（GitHub Action环境建议False） ==========
ENABLE_CHECK = False
CHECK_TIMEOUT = 2

def is_url_valid(url):
    """检测链接是否可访问，超时/报错返回False"""
    try:
        headers = {
            "User‑Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.head(url, headers=headers, timeout=CHECK_TIMEOUT, allow_redirects=True)
        return resp.status_code < 400
    except Exception:
        return False

def match_group(channel_name):
    if channel_name in FORCE_MAP:
        return FORCE_MAP[channel_name]
    for g_name, pat in GROUP_RULES:
        # 忽略大小写匹配
        if re.search(pat, channel_name, re.IGNORECASE):
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
                else:
                    name = "未知频道"
            elif line and not line.startswith("#"):
                if name:
                    # 只过滤指定的那一个频道，其他全部放行
                    if name == BLOCK_CHANNEL_NAME:
                        print(f"【已过滤指定广告频道】{name}")
                        name = ""
                        continue

                    # 连通检测开关
                    if ENABLE_CHECK and not is_url_valid(line):
                        print(f"无效/超时源丢弃：{name} → {line}")
                        name = ""
                        continue

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
    REMOTE_URLS = [
        "https://live.445569.xyz/live.m3u",
        "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
    ]
    total_channels = []

    for url in REMOTE_URLS:
        print(f"正在拉取：{url}")
        chs = fetch_remote_m3u(url)
        total_channels.extend(chs) # 不做去重，直接追加全部

    m3u_text = build_m3u(total_channels)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_text)
    print(f"✅ 全部完成，共 {len(total_channels)} 个频道，输出 live.m3u")
