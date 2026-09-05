import requests
import re
import os
# ========== 只在这里填写你自己要用的直播源，其余全部删掉 ==========
URL_LIST = [
    "https://raw.githubusercontent.com/Supprise0901/TVBox_live/refs/heads/main/live.txt",
    "https://raw.githubusercontent.com/bj123sd/hycg/refs/heads/main/tv.txt",
    "https://raw.githubusercontent.com/mursor1985/LIVE/refs/heads/main/huyayqk.m3u",
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
MOVIE_KEYWORDS = [
    "电影","影院","影视","热播电影","经典电影",
    "动作电影","喜剧电影","院线","4K电影"
]
MUSIC_KEYWORDS = [
    "怀集音乐台",
    "音乐石榴",
    "秋月剪水",
    "喵喵音乐台",
    "阿七点歌台",
    "音乐喵",
    "下饭音乐",
    "音乐台长",
    "音乐WU歌",
    "音乐快斗",
    "音乐猛抬头",
    "黑糖音乐秀",
    "最久音乐",
    "荒草音乐",
    "蚕豆电台"
]
ORIGINAL_KEYWORDS = [
    "夏夜小妖咪",
"红厂 - 百里老贼",
"暖洋羊洋",
"婧婧丶",
"百变御姐姐 nice",
"新橙記 Orange 丶",
"蜜桃大学生",
"伊太刀",
"夏日幽泉鼠",
"百川公会",
"阿斗归来了",
"江爽【柿柿顺意】",
"瑶摇很 nice",
"晶晶舔奶盖",
"寒露森色宠宠",
"春水不服食",
"Ossi",
"Ziyo",
"怡怡爱喝奶茶",
"午饭有鱼有虾",
"锤子动画",
"夜萝莉宝宝",
"视觉 - 秦 VV",
"冰冰想吃冰棒",
"萌萌小桃子",
"道州万物并",
"大梨 o",
"小桃猪猪",
"永别兵火里",
"得志未断绝",
"小燕子紫薇",
"薄情凉了城",
"偶看见常威在打来福",
"SJ - 倾甜",
"古镇小鹿",
"西京观影",
"一支小桃花",
"麦麦放映",
"快乐 de 小猫",
"梦境幻影雪 8",
"黄口咸阳树",
"叁岁打死牛",
"虎桥路关羽",
"甜甜影院",
"一起看我爱看剧",
"温柔璐琳",
"愤怒的小金花",
"天天影社",
"超甜呦",
"凌婫婫",
"我是娅娅吖",
"双双影剧",
"不吃香菜丫丫",
"欲觉秋千索",
"宸艺艺",
"娇娇影视",
"小璐影视",
"小雏莓莓",
"爽儿影视",
"小满荷塘香色",
"辰辰观影",
"大雅唯白发",
"玉妮啵啵",
"晚安云起",
"静静影视",
"萘萘呐 hh",
"大法师大法师",
"潇洒依旧广哥",
"小希观影",
"樱花布布",
"高光清欢",
"恢恢何团团",
"柔白秋实",
"SJ - 咩咩【来财】",
"娜娜陪看",
"巨鲨婷婷",
"影评专员",
"薇薇观影",
"芸芸看剧",
"七七爱剧",
"青青观影",
"云雨巫山断肠",
"雪女悠悠",
"菲菲爱剧",
"小萝莉爱爱",
"花见羞羞",
"入梦影视",
"年年营",
"我是图图很淘气",
"素素爱哭",
"李一彤彤",
"柔柔微冷",
"周星驰 -- 喜剧之王",
"余小二哦",
"【炊烟大壮】",
"依依依雅",
"九思剧场",
"你同桌依依",
"止戈电影",
"狗哥吃火锅",
"科幻梦工场",
"小迷糊",
"阿光影视",
"唯倜得同行",
"HeungsamsFamily",
"老郭有新番",
"亮哥讲电影",
"雪见",
"小虎爱看剧",
"风中有垛雨做的云",
"电影最 TOP",
"西部影坛",
"南西视频"
]
YIQIKAN_KEYWORDS = [
    "武林萌主唐小姐",
    "周星星",
    "野外生存技巧",
    "小木子先生丶",
    "小虎牙 - QQFbPxwM1A",
    "鯎爺",
    "心疼得抱住胖胖的自己",
    "瞬间爆炸",
    "7 喜先生",
    "古咕咕",
    "草莓肠粉酱",
    "活泼有趣的熊猫",
    "海绵宝宝宝",
    "美少女咸儿",
    "艾莉",
    "我是詹密",
    "四大裁子之首",
    "鱼塘塘主张年年",
    "柯冉冉",
    "大漠李白",
    "會唱歌的小野貓",
    "傻妞",
    "虎牙八点档",
    "领带哥",
    "水晶 awa",
    "傍晚猴",
    "No1 常在心",
    "白菘无人省",
    "全优少年",
    "野原的一家",
    "大侠",
    "陈翔六点半",
    "红茶妹妹",
    "我爱黑科技",
    "兄台明鉴",
    "一川星悬 -",
    "-- 娇妹",
    "个人向",
    "超能力是放 pi",
    "小妖孽",
    "反方向的钟 1874",
    "裸奔的蜗牛╮",
    "浮生没有若梦",
    "Wang - 我的女人",
    "莫小辰",
    "歌声无边界",
    "茱麗葉",
    "港片剧情真好",
    "粉娘",
    "里昂保护的玛蒂达",
    "YJ - 无语凝烟",
    "老司机",
    "尼古拉斯乔丹",
    "我们都爱笑",
    "种瓜得弟弟",
    "Cc",
    "二次元 baby",
    "电视迷痴迷港剧",
    "萌新司机",
    "老问我东西南北",
    "我要在你头上暴扣",
    "四次元先生",
    "小猪猪",
    "春水盈盈细浪翻",
    "摄氏零度",
    "悬疑放映厅",
    "春江花朝吹香夢",
    "千里",
    "幻想拥有 100w",
    "我很忙",
    "好学上进的青年",
    "江天大夫與",
    "港剧日记",
    "逗比宝宝",
    "偷心大盗ヽ龍宝",
    "小爱酱",
    "如意菜头",
    "HelloKitty",
    "落于巧克力",
    "鄉 8 佬",
    "虎牙影院",
    "实力拔萝卜",
    "战争电影放映厅",
    "鸽宝小改改",
    "Yummy",
    "小虎牙 - gj0OAus6Bl",
    "小雅陪你看",
    "奇幻电影放映厅",
    "华视 - 高分好片",
    "多面体想娶冰柠檬",
    "予笙",
    "會稽愚婦数花开",
    "一起来学粤语",
    "地震监视慢直播",
    "天水慢直播",
    "錦丹广明",
    "酒窝储存机",
    "我是一颗小虎牙",
    "带巫婆的黑猫",
    "李大湿",
    "明日香世界第一可爱",
    "一起来埋堆",
    "近藤喜彦",
    "生活技巧",
    "天地間香芒",
    "霸总傲天短剧",
    "望处不是筝",
    "赛博的朋克",
    "夏初冬临",
    "骚年跟我来听歌",
    "哈拉少足球",
    "阿森木木木",
    "神秘小希哟",
    "钱丢丢丢",
    "港片看不停",
    "别和陌生人说话",
    "KuKu 鲨鲨",
    "阿夹",
    "鬼畜娘",
    "埋堆搞搞震",
    "動感 de 地带",
    "小虎牙 - 7kYdWFDMe2",
    "RainyRabbits",
    "屁总是多德",
    "小军迷",
    "奇遇公主",
    "暖阳雪兔",
    "仰望星空慢直播",
    "幻海航行",
    "- 懒猪",
    "明天吃啥好呢",
    "耳里如闻疑忠良",
    "武侠电影放映厅",
    "好汉来也",
    "喜剧电影放映厅",
    "一片青青草原",
    "电音 857",
    "漓江塔景区售票阿姨",
    "核桃姐姐",
    "叉烧饭走饭",
    "电视剧好看",
    "有妖气漫画 - 十冷",
    "黑羽",
    "地狱ヽ妖妖",
    "开心喷火龙",
    "雨落惊鸿人",
    "迎宾桥米莱迪",
    "梁非凡吔 X 啦",
    "哥哥永恒",
    "北岛南城",
    "小虎牙 - pe9TtkpjvO",
    "大懒猫",
    "前无古人 147",
    "港剧慢品汇",
    "来杯摩卡",
    "超人的归来",
    "虎牙放映厅",
    "港片魅力无限",
    "十八里铺大当家",
    "无花果不结果",
    "主播辣眼睛",
    "被窝侠",
    "是西门大官人啊",
    "槽老师",
    "我是翩翩少年郎",
    "痞子帅叔叔",
    "动作大片放映厅",
    "二次元控",
    "简小熙",
    "经典日本动漫速看",
    "崇礼燕平",
    "道长我们私奔吧",
    "经典剧好看",
    "嘤嘤嘤",
    "永艳金铭",
    "人间眩法师",
    "第十门",
    "老王夸我帅",
    "赛文 777",
    "学妹爱学长",
    "北岛的诗",
    "我很怪丶但我不坏",
    "华视 - 动作大片",
    "Edinburgh 南空",
    "华视 - 警匪大片",
    "回忆大马甲",
    "扁豆看电影 2",
    "横而梦里还",
    "家里有只小汤圆",
    "小森林淼淼",
    "力哥影視",
    "忻莹",
    "散步霜华",
    "【蠟筆小新】",
    "君子杉",
    "雪布林",
    "S 哥影视",
    "影小渔",
    "小虎菲菲",
    "DD - 解说",
    "李小哇絮叨叨",
    "荒野求生影探",
    "思思",
    "小丑讲电影",
    "天雷鼓鼓说剧",
    "柚柚",
    "庄升秋",
    "哀是麦子的球迷",
    "非凡武林",
    "baby 丶贝贝",
    "西西姐姐",
    "越式酥麻",
    "月光下",
    "头上在眼前",
    "阿良说美剧",
    "HagnaChannel",
    "辟哥影视",
    "糊了的胡萝卜",
    "斌哥漫说",
    "战士吹沙埃",
    "蒲公英电影",
    "五哥观影团",
    "SJ - 安安【小兔子】",
    "缔爵丶小阿杜",
    "羊羊",
    "惊奇小剧场",
    "一哥爱解说",
    "君陌观影",
    "释小龙 - 少林小子",
    "音乐小石榴",
    "小丰爱追剧",
    "小萌主在看剧",
    "柔式解压",
    "小琪",
    "越哥说电影",
    "小虎牙 - kHRngHaMKk",
    "7 块说故事",
    "乔我说游戏频道",
    "小川侃电影",
    "月月",
    "楚门聊电影",
    "重庆火锅青岚黄麻鸡",
    "婧丶",
    "九叔林正英",
    "熊妹撩电影",
    "良少聊漫威",
    "泱泱看剧",
    "大象放映室",
    "大神影视",
    "韩式酥麻",
    "柒言绝剧",
    "剧能说",
    "电影狂人 A",
    "细品红楼",
    "小若影视",
    "莫西西西西",
    "泛爱心说剧",
    "老微讲故事",
    "港片大赏",
    "诗语墨",
    "YeShi 小哥",
    "冯小刚 - 导演",
    "荒野小屁孩",
    "诡计腰柳中空",
    "鑫鑫影视",
    "蓬蓬带你看剧",
    "涵哥评电影",
    "小马追剧",
    "驴子爱影视",
    "米饭何首乌粉",
    "鱼丸说电影",
    "小兔",
    "吾聊电影",
    "宇宙无敌韩三金",
    "A 皮皮",
    "喜剧大赏",
    "自由进行时",
    "玉女林青霞",
    "如来解说",
    "电影探长官方",
    "大潘影视",
    "狼肉 - 恐怖游戏",
    "荧儿",
    "小宋追剧",
    "灵灵",
    "乔我说动漫频道",
    "青年电影馆",
    "短剧搞笑社",
    "荒爷求生007",
    "灵魂照妖镜",
    "专情于你",
    "短剧无极限",
    "鸳鸯入帘青",
    "心曲长城窟",
    "君知钩看了",
    "岳岳追剧呀",
    "短剧电影院",
    "符文大乱斗的神",
    "Joey - 王祖贤",
    "小师妹说剧",
    "元元",
    "陈年三百零六斤",
    "咔咔一顿玩",
    "蓝翔新三国",
    "短剧小故事",
    "告别烦恼",
    "短剧美好人生",
    "猫眼下的鱼",
    "奇幻冒险家",
    "未来无限可能追寻者",
    "硬汉影探",
    "剧迷大本营",
    "快剧一览",
    "小松说剧",
    "我是三三呀",
    "酱婶儿电影",
    "东方先生 i",
    "搞笑天地",
    "情绪调味料",
    "喵哇塞",
    "短剧荟萃馆",
    "虎虎剧社呀",
    "大鹅观影",
    "荒野大世界",
    "短剧轻松自在",
    "阿森观影团",
    "阿涛影视",
    "光之镇魂曲",
    "自天太行山",
    "电视城打工人"
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
    extinf = re.sub(r' group-title="[^"]+"', '', extinf)
    idx = extinf.rfind(',')
    if idx == -1:
        return extinf
    return extinf[:idx] + f' group-title="{group_name}"' + extinf[idx:]
def main():
    # 按分组存储 {分组名: [(频道名,url),...]}
    group_bucket = {
        "央视频道": [],
        "卫视频道": [],
        "影视直播": [],
        "音乐频道": [],
        "原创": [],
        "一起看": []
    }
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
                elif any(k in ch_name for k in MOVIE_KEYWORDS):
                    group = "影视直播"
                elif any(k in ch_name for k in MUSIC_KEYWORDS):
                    group = "音乐频道"
                elif any(k in ch_name for k in ORIGINAL_KEYWORDS):
                    group = "原创"
                elif any(k in ch_name for k in YIQIKAN_KEYWORDS):
                    group = "一起看"
                if group is not None:
                    item_key = (ch_name, play_url)
                    if item_key not in seen:
                        seen.add(item_key)
                        group_bucket[group].append((ch_name, play_url))
        except Exception as e:
            print(f"⚠️ 拉取 {url} 失败：{e}")
    total_cnt = sum(len(v) for v in group_bucket.values())
    print(f"✅筛选结束，一共保留频道：{total_cnt}")
    out_dir = "./output"
    os.makedirs(out_dir, exist_ok=True)
    # =========输出 m3u（保留group‑title）=========
    output_m3u = ["#EXTM3U"]
    for gname, ch_list in group_bucket.items():
        for cname, curl in ch_list:
            fake_ext = f'#EXTINF:-1 group-title="{gname}",{cname}'
            output_m3u.append(fake_ext)
            output_m3u.append(curl)
    m3u_path = os.path.join(out_dir, "live.m3u")
    with open(m3u_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_m3u))
    print(f"✅已输出 m3u：{m3u_path}")
    # =========输出 TVBox 专用 #genre# 格式txt（就是截图里面那种）=========
    txt_lines = []
    for gname, ch_list in group_bucket.items():
        if len(ch_list) == 0:
            continue
        txt_lines.append(f"{gname},#genre#")
        for cname, curl in ch_list:
            txt_lines.append(f"{cname},{curl}")
    txt_path = os.path.join(out_dir, "live.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))
    print(f"✅已输出带#genre#分组txt：{txt_path}")
if __name__ == "__main__":
    main()
