import requests

URL_LIST = [
        "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
        "https://raw.githubusercontent.com/bj123sd/hycg/refs/heads/main/tv.txt",
        "https://raw.githubusercontent.com/lihansong888/collect-tv-txt/refs/heads/main/bbxx_lite.txt",
        "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u",
        "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/global.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u"
]

# 同时兼容 CCTV‑1 和 CCTV1 两种写法
WHITELIST_KEYWORDS = [
    "CCTV-1", "CCTV-2", "CCTV-3", "CCTV-4", "CCTV-5",
    "CCTV-5+", "CCTV-6", "CCTV-7", "CCTV-8", "CCTV-9",
    "CCTV-10", "CCTV-11", "CCTV-12", "CCTV-13", "CCTV-14",
    "CCTV-15", "CCTV-16", "CCTV-17",
    "CCTV1","CCTV2","CCTV3","CCTV4","CCTV5","CCTV5+",
    "CCTV6","CCTV7","CCTV8","CCTV9","CCTV10",
    "CCTV11","CCTV12","CCTV13","CCTV14","CCTV15","CCTV16","CCTV17"
]

def parse_any(text: str):
    """同时解析标准m3u(#EXTINF) 和 简易txt(名称,url)格式"""
    res = []
    extinf_line = None
    for raw_line in text.splitlines():
        ln = raw_line.strip()
        if not ln:
            continue
        # 处理标准M3U格式
        if ln.startswith("#EXTINF:"):
            extinf_line = ln
            continue
        if extinf_line is not None and not ln.startswith("#"):
            res.append((extinf_line, ln))
            extinf_line = None
            continue
        # 处理 txt：频道名,地址
        if ',' in ln and not ln.startswith("#"):
            sp = ln.split(',',1)
            name_part = sp[0].strip()
            url_part = sp[1].strip()
            fake_ext = f'#EXTINF:-1,{name_part}'
            res.append((fake_ext, url_part))
    return res

def get_channel_name(extinf):
    if "," in extinf:
        return extinf.split(",")[-1].strip()
    return ""

def main():
    keep_list = []
    seen = set()
    for url in URL_LIST:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            channels = parse_any(resp.text)
            for extinf, play_url in channels:
                ch_name = get_channel_name(extinf)
                if any(key in ch_name for key in WHITELIST_KEYWORDS):
                    item_key = (extinf, play_url)
                    if item_key not in seen:
                        seen.add(item_key)
                        keep_list.append((extinf, play_url))
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}")

    print(f"✅筛选结束，去重后一共保留频道数量：{len(keep_list)}")
    output = ["#EXTM3U"]
    for ext, u in keep_list:
        output.append(ext)
        output.append(u)
    final_text = "\n".join(output)
    print("-----【输出预览前20行】-----")
    print("\n".join(output[:20]))

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(final_text)
    print("✅已写入仓库根目录 live.m3u")

if __name__ == "__main__":
    main()
