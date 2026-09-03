import requests

# 在这里添加你的所有源，一行一个，末尾加逗号
URL_LIST = [
        "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/bj123sd/hycg/refs/heads/main/tv.txt",
        "https://raw.githubusercontent.com/lihansong888/collect-tv-txt/refs/heads/main/bbxx_lite.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
]
# CCTV白名单关键字，包含即保留
WHITELIST_KEYWORDS = [
    "CCTV-1", "CCTV-2", "CCTV-3", "CCTV-4", "CCTV-5",
    "CCTV-5+", "CCTV-6", "CCTV-7", "CCTV-8", "CCTV-9",
    "CCTV-10", "CCTV-11", "CCTV-12", "CCTV-13", "CCTV-14",
    "CCTV-15", "CCTV-16", "CCTV-17"
]

def parse_m3u(text: str):
    """解析m3u/txt直播源，返回 [(extinf行,播放地址)]"""
    result = []
    extinf_line = None
    for line in text.splitlines():
        ln = line.rstrip("\r\n")
        if ln.startswith("#EXTINF:"):
            extinf_line = ln
        elif extinf_line is not None and ln.strip() and not ln.startswith("#"):
            result.append((extinf_line, ln.strip()))
            extinf_line = None
    return result

def get_channel_name(extinf):
    if "," in extinf:
        return extinf.split(",")[-1].strip()
    return ""

def main():
    keep_list = []
    seen = set() # 用于去重，记录已经存过的(ext,url)
    for url in URL_LIST:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            channels = parse_m3u(resp.text)
            for extinf, play_url in channels:
                ch_name = get_channel_name(extinf)
                # 包含匹配，只要名字带关键字就留下
                if any(key in ch_name for key in WHITELIST_KEYWORDS):
                    item_key = (extinf, play_url)
                    if item_key not in seen:
                        seen.add(item_key)
                        keep_list.append((extinf, play_url))
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}，跳过该源")

    print(f"✅筛选结束，去重后一共保留频道数量：{len(keep_list)}")
    # 组装输出m3u文件
    output = ["#EXTM3U"]
    for ext, u in keep_list:
        output.append(ext)
        output.append(u)
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("✅已写入仓库根目录 live.m3u")

if __name__ == "__main__":
    main()
