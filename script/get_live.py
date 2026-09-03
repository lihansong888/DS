import requests
import re

# ========== 只在这里填写你自己要用的直播源，其余全部删掉 ==========
URL_LIST = [
    "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
    "https://raw.githubusercontent.com/bj123sd/hycg/refs/heads/main/tv.txt",
    "https://raw.githubusercontent.com/lihansong888/collect-tv-txt/refs/heads/main/bbxx_lite.txt",
    "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/refs/heads/main/best_sorted.m3u"
]

CCTV_KEYWORDS = [
    "CCTV-1", "CCTV-2", "CCTV-3", "CCTV-4", "CCTV-5",
    "CCTV-5+", "CCTV-6", "CCTV-7", "CCTV-8", "CCTV-9",
    "CCTV-10", "CCTV-11", "CCTV-12", "CCTV-13", "CCTV-14",
    "CCTV-15", "CCTV-16", "CCTV-17",
    "CCTV1","CCTV2","CCTV3","CCTV4","CCTV5","CCTV5+",
    "CCTV6","CCTV7","CCTV8","CCTV9","CCTV10",
    "CCTV11","CCTV12","CCTV13","CCTV14","CCTV15","CCTV16","CCTV17"
]
SATELLITE_KEYWORDS = [
    "江苏卫视","浙江卫视","湖南卫视","东方卫视","上海卫视",
    "北京卫视","广东卫视","深圳卫视","安徽卫视","山东卫视",
    "天津卫视","重庆卫视","四川卫视","湖北卫视","河南卫视",
    "河北卫视","山西卫视","辽宁卫视","吉林卫视","黑龙江卫视",
    "福建卫视","东南卫视","江西卫视","广西卫视","云南卫视",
    "贵州卫视","陕西卫视","甘肃卫视","宁夏卫视","新疆卫视"
]


def parse_any(text: str):
    res = []
    extinf_line = None
    for raw_line in text.splitlines():
        ln = raw_line.strip()
        if not ln:
            continue
        if ln.startswith("#EXTINF:"):
            extinf_line = ln
            continue
        if extinf_line is not None and not ln.startswith("#"):
            res.append((extinf_line, ln))
            extinf_line = None
            continue
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

def add_group_tag(extinf: str, group_name:str):
    # 清除所有原有的 group-title
    extinf = re.sub(r' group-title="[^"]+"', '', extinf)
    idx = extinf.rfind(',')
    if idx == -1:
        return extinf
    return extinf[:idx] + f' group-title="{group_name}"' + extinf[idx:]

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
                group = None
                if any(k in ch_name for k in CCTV_KEYWORDS):
                    group = "央视频道"
                elif any(k in ch_name for k in SATELLITE_KEYWORDS):
                    group = "卫视频道"
                

                if group is not None:
                    item_key = (extinf, play_url)
                    if item_key not in seen:
                        seen.add(item_key)
                        new_ext = add_group_tag(extinf, group)
                        keep_list.append((new_ext, play_url))
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}")

    print(f"✅筛选结束，一共保留频道：{len(keep_list)}")
    output = ["#EXTM3U"]
    for ext, u in keep_list:
        output.append(ext)
        output.append(u)
    final_text = "\n".join(output)

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(final_text)
    print("✅已输出 live.m3u")

if __name__ == "__main__":
    main()

