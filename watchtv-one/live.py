import requests
import re
import os
# ========== 只在这里填写你自己要用的直播源，其余全部删掉 ==========
URL_LIST = [
    "https://gh-proxy.com/https://github.com/mursor1985/LIVE/blob/main/huyayqk.m3u"
]

# ========== 要屏蔽的频道（不读取、不录入）==========
EXCLUDE_CHANNELS = [
    "4K60PSDR-H264-AAC测试",
    "4K60PHLG-HEVC-EAC3测试"
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

def main():
    # 只有一个分组：一起看
    group_bucket = {
        "影视一起看": []
    }
    seen = set()
    for url in URL_LIST:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            channels = parse_any(resp.text)
            for extinf, play_url in channels:
                ch_name = get_channel_name(extinf)
                # 屏蔽指定频道
                if ch_name in EXCLUDE_CHANNELS:
                    continue
                # 所有频道直接放进一起看，不做关键词筛选
                item_key = (ch_name, play_url)
                if item_key not in seen:
                    seen.add(item_key)
                    group_bucket["一起看"].append((ch_name, play_url))
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}")
    total_cnt = sum(len(v) for v in group_bucket.values())
    print(f"✅筛选结束，一共保留频道：{total_cnt}")
    # 输出到脚本所在目录（即 watchtv-one 文件夹）
    out_dir = os.path.dirname(os.path.abspath(__file__))
    output_m3u = ["#EXTM3U"]
    for gname, ch_list in group_bucket.items():
        for cname, curl in ch_list:
            fake_ext = f'#EXTINF:-1 group-title="{gname}",{cname}'
            output_m3u.append(fake_ext)
            output_m3u.append(curl)
    m3u8_path = os.path.join(out_dir, "live.m3u8")
    with open(m3u8_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_m3u))
    print(f"✅已输出 m3u8：{m3u8_path}")

if __name__ == "__main__":
    main()

