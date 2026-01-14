import difflib

package_name_map = {
    "天气": "com.coloros.weather2",
    "家人守护": "com.coloros.familyguard",
    "美柚": "com.lingan.seeyou",
    "百度极速版": "com.baidu.searchbox.lite",
    "58同城": "com.wuba",
    "知乎": "com.zhihu.android",
    "滴滴出行": "com.sdu.didi.psnger",
    "计算器": "com.coloros.calculator",
    "掌上生活": "com.cmbchina.ccd.pluto.cmbActivity",
    "飞猪旅行": "com.taobao.trip",
    "网易有道词典": "com.youdao.dict",
    "百度贴吧": "com.baidu.tieba",
    "腾讯新闻": "com.tencent.news",
    "饿了么": "me.ele",
    "百度输入法": "com.baidu.input",
    "优酷视频": "com.youku.phone",
    "抖音": "com.ss.android.ugc.aweme",
    "今日头条": "com.ss.android.article.news",
    "酷我音乐": "cn.kuwo.player",
    "oppo社区": "com.oppo.community",
    "夸克": "com.quark.browser",
    "邮件": "com.android.email",
    "美团": "com.sankuai.meituan",
    "剪映": "com.lemon.lv",
    "酷狗概念版": "com.kugou.android.lite",
    "酷狗音乐": "com.kugou.android",
    "网易邮箱大师": "com.netease.mail",
    "番茄免费小说": "com.dragon.read",
    "yy": "com.duowan.mobile",
    "qq": "com.tencent.mobileqq",
    "小宇宙": "app.podcast.cosmos",
    "指南针": "com.coloros.compass2",
    "oppo视频": "com.heytap.yoli",
    "天猫": "com.tmall.wireless",
    "抖音商城": "com.ss.android.ugc.livelite",
    "点淘": "com.taobao.live",
    "录音": "com.coloros.soundrecorder",
    "哔哩哔哩": "tv.danmaku.bili",
    "B站": "tv.danmaku.bili",
    "soul": "cn.soulapp.android",
    "高德地图": "com.autonavi.minimap",
    "懂车帝": "com.ss.android.auto",
    "小红书": "com.xingin.xhs",
    "咪咕视频": "com.cmcc.cmvideo",
    "拼多多": "com.xunmeng.pinduoduo",
    "微信读书": "com.tencent.weread",
    "蘑菇街": "com.mogujie",
    "大众点评": "com.dianping.v1",
    "云闪付": "com.unionpay",
    "好看视频": "com.baidu.haokan",
    "AIAgentDemo": "com.stepfun.aiagent.demo",
    "qq浏览器": "com.tencent.mtt",
    "文件管理": "com.coloros.filemanager",
    "豆瓣": "com.douban.frodo",
    "日历": "com.coloros.calendar",
    "游戏助手": "com.oplus.games",
    "网易云音乐": "com.netease.cloudmusic",
    "中国联通": "com.sinovatech.unicom.ui",
    "喜马拉雅": "com.ximalaya.ting.android",
    # "美团外卖": "com.sankuai.meituan.takeoutnew",
    "主题商店": "com.heytap.themestore",
    "飞书": "com.ss.android.lark",
    "红袖读书": "com.hongxiu.app",
    "全民K歌": "com.tencent.karaoke",
    "抖音火山版": "com.ss.android.ugc.live",
    "美图秀秀": "com.mt.mtxx.mtxx",
    "拾程旅行": "com.hnjw.shichengtravel",
    "中国电信": "com.ct.client",
    "时钟": "com.coloros.alarmclock",
    "快对": "com.kuaiduizuoye.scan",
    "钱包": "com.finshell.wallet",
    "快手极速版": "com.kuaishou.nebula",
    "文件随心开": "andes.oplus.documentsreader",
    "微博": "com.sina.weibo",
    "墨迹天气": "com.moji.mjweather",
    "kimi 智能助手": "com.moonshot.kimichat",
    "起点读书": "com.qidian.QDReader",
    "逍遥游": "com.redteamobile.roaming",
    "豆包": "com.larus.nova",
    "平安好车主": "com.pingan.carowner",
    "去哪儿旅行": "com.Qunar",
    "银联可信服务安全组件": "com.unionpay.tsmservice",
    "腾讯微视": "com.tencent.weishi",
    "网上国网": "com.sgcc.wsgw.cn",
    "作业帮": "com.baidu.homework",
    "阅读": "com.heytap.reader",
    "keep": "com.gotokeep.keep",
    "蜻蜓FM": "fm.qingting.qtradio",
    "禅定空间": "com.oneplus.brickmode",
    "腾讯地图": "com.tencent.map",
    "虎牙直播": "com.duowan.kiwi",
    "番茄畅听音乐版": "com.xs.fm.lite",
    "今日头条极速版": "com.ss.android.article.lite",
    "转转": "com.wuba.zhuanzhuan",
    "芒果TV": "com.hunantv.imgo.activity",
    "便签": "com.coloros.note",
    "UC浏览器": "com.UCMobile",
    "百度文库": "com.baidu.wenku",
    "小猿搜题": "com.fenbi.android.solar",
    "腾讯文档": "com.tencent.docs",
    "携程旅行": "ctrip.android.view",
    "wpsoffice": "cn.wps.moffice_eng",
    "哈啰": "com.jingyao.easybike",
    "中国移动": "com.greenpoint.android.mc10086.activity",
    "唯品会": "com.achievo.vipshop",
    "手机 搬家": "com.coloros.backuprestore",
    "安逸花": "com.msxf.ayh",
    "汽水音乐": "com.luna.music",
    "音乐": "com.heytap.music",
    "小猿口算": "com.fenbi.android.leo",
    "MOMO陌陌": "com.immomo.momo",
    "支付宝": "com.eg.android.AlipayGphone",
    "爱奇艺": "com.qiyi.video",
    "DataCollection": "com.example.datacollection",
    "番茄畅听": "com.xs.fm",
    "语音翻译": "com.coloros.translate",
    "文件随心开": "cn.wps.moffice.lite",
    "无线耳机": "com.oplus.melody",
    "得物": "com.shizhuang.duapp",
    "西瓜视频": "com.ss.android.article.video",
    "网易新闻": "com.netease.newsreader.activity",
    "腾讯视频": "com.tencent.qqlive",
    "淘宝特价版": "com.taobao.litetao",
    "七猫免费小说": "com.kmxs.reader",
    "自如": "com.ziroom.ziroomcustomer",
    "爱奇艺极速版": "com.qiyi.video.lite",
    "淘宝": "com.taobao.taobao",
    "斗鱼": "air.tv.douyu.android",
    "快手": "com.smile.gifmaker",
    "扫描全能王": "com.intsig.camscanner",
    "买单吧": "com.bankcomm.maidanba",
    "飞连": "com.volcengine.corplink",
    "菜鸟": "com.cainiao.wireless",
    "盒马": "com.wudaokou.hippo",
    "阿里巴巴": "com.alibaba.wireless",
    "智能家居": "com.heytap.smarthome",
    "小布指令": "com.coloros.shortcuts",
    "闲鱼": "com.taobao.idlefish",
    "游戏中心": "com.nearme.gamecenter",
    "搜狗输入法": "com.sohu.inputmethod.sogou",
    "QQ邮箱": "com.tencent.androidqqmail",
    "百度网盘": "com.baidu.netdisk",
    "QC浏览器": "com.fjhkf.gxdsmls",
    "酷安": "com.coolapk.market",
    "QQ音乐": "com.tencent.qqmusic",
    "百度": "com.baidu.searchbox",
    "抖音极速版": "com.ss.android.ugc.aweme.lite",
    "铁路12306": "com.MobileTicket",
    "OPPO商城": "com.oppo.store",
    "自由收藏": "com.coloros.favorite",
    "我的OPPO": "com.oplus.member",
    "掌阅": "com.chaozh.iReaderFree",
    "腾讯会议": "com.tencent.wemeet.app",
    "企业微信": "com.tencent.wework",
    "健康": "com.heytap.health",
    "微信": "com.tencent.mm",
    "京东": "com.jingdong.app.mall",
    "肯德基": "com.yek.android.kfc.activitys",
    "搜狐视频": "com.sohu.sohuvideo",
    "百度地图": "com.baidu.BaiduMap",
    "山姆会员商店": "cn.samsclub.app",
    "大麦": "cn.damai",
    "醒图": "com.ss.android.picshow",
    "设置": "com.android.settings",
    "王者荣耀": "com.tencent.tmgp.sgame",
    "随手记": "com.mymoney",
    "钢琴块二": "com.cmplay.tiles2_cn",
    "麦当劳": "com.mcdonalds.gma.cn",
    "寻艺": "com.vlinkage.xunyee",
    "京东到家": "com.jingdong.pdj",
    "小象超市": "com.meituan.retail.v.android",
    "京东金融": "com.jd.jrapp",
    "猫眼": "com.sankuai.movie",
    "红果免费短剧": "com.phoenix.read",
    "三角洲行动": "com.tencent.tmgp.dfm",
    "航旅纵横": "com.umetrip.android.msky.app",
    "淘票票": "com.taobao.movie.android",
    "学习强国": "cn.xuexi.android",
    "小米商城": "com.xiaomi.shop",
    "浏览器": "com.android.browser",
    "look": "com.vision.haokan",
    "什么值得买": "com.smzdm.client.android",
    "妙兜": "com.agent.miaodou",
    "瑞幸咖啡": "com.lucky.luckyclient",
    "豆瓣阅读": "com.douban.book.reader",
    "钉钉": "com.alibaba.android.rimet",
    "达美乐披萨": "com.android.permissioncontroller",
    "同程旅行": "com.tongcheng.android",
    "opentracks": "de.dennisguse.opentracks",
    "simple sms messenger": "com.simplemobiletools.smsmessenger",
    "joplin": "net.cozic.joplin",
    "miniwob": "com.google.androidenv.miniwob",
    "simple gallery pro": "com.simplemobiletools.gallery.pro",
    "simple gallery": "com.simplemobiletools.gallery.pro",
    "gallery": "com.simplemobiletools.gallery.pro",
    "audio recorder": "com.dimowner.audiorecorder",
    "broccoli": "com.flauschcode.broccoli",
    "simple calendar pro": "com.simplemobiletools.calendar.pro",   
    "simple draw pro": "com.simplemobiletools.draw.pro",
    "draw": "com.simplemobiletools.draw.pro",
    "clipper": "ca.zgrs.clipper",
    "retro music": "code.name.monkey.retromusic",
    "arduia pro expense": "com.arduia.expense",
    "markor": "net.gsantner.markor",
    "tasks": "org.tasks",
    "osmAnd": "net.osmand",
    "给到": "com.guanaitong",
    "百词斩": "com.jiongji.andriod.card",
    "企查查": "com.android.icredit",
    "应用宝": "com.tencent.android.qqdownloader",
}

import difflib 

def find_package_name(app_name):
    app_name_lowered = app_name.lower()
    package_name = package_name_map.get(app_name_lowered, None)
    
    max_match = {
        "name": None,
        "score": 0
    }
    
    if package_name is None:
        # to search a similar app name
        for key in package_name_map.keys():
            # Use the lowercase input for comparison
            score = difflib.SequenceMatcher(None, app_name_lowered, key.lower()).ratio() 
            
            if score > max_match["score"]:
                max_match["name"] = key
                max_match["score"] = score
        
        # Check if a match was found with a score > 0 (or some threshold, though the assert below only checks if name is not None)
        assert max_match['name'] is not None, f"Cannot find package name for app {app_name}"
        
        # We retrieve the actual package name using the original (correctly cased) key from the map
        package_name = package_name_map[max_match['name']]

    return package_name


def get_list_of_package_names():
    """
    Return a list of all package names.
    """
    applications = [{"app_name": app_name, "package_name": package_name} for app_name, package_name in package_name_map.items()]
    return applications


def find_LAUNCH_SINGLE_TOP_activity(adb_id, package_name):
    """
    Find LAUNCH_SINGLE_TOP activity name for each package
    
    Args:
        package_name: The package name to find the activity for (e.g., com.taobao.taobao)
    
    Returns:
        The activity name extracted from the logcat, or None if not found
    """
    import subprocess
    import re
    import time
    
    try:
        # Step 1: Stop the package
        stop_cmd = f'adb -s {adb_id} shell am force-stop {package_name}'
        subprocess.run(stop_cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"Stopped package: {package_name}")
        
        # Wait a moment for the package to fully stop
        time.sleep(1)
        
        # Step 2: Clear logcat buffer to avoid old logs
        subprocess.run('adb logcat -c', shell=True, check=True, capture_output=True, text=True)
        
        # Step 3: Start the package (open to home/default interface)
        # Using monkey command to launch the main activity
        open_cmd = f'adb -s {adb_id} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
        subprocess.run(open_cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"Opened package: {package_name}")
        
        # Wait for the app to launch and generate logs
        time.sleep(5)
        
        # Step 4: Get logcat and filter for LAUNCH_SINGLE_TOP
        logcat_cmd = f'adb -s {adb_id} shell "logcat -d -b all | grep LAUNCH_SINGLE_TOP"'
        result = subprocess.run(logcat_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Failed to get logcat: {result.stderr}")
            return None
        
        logcat_output = result.stdout
        
        # Step 5: Find the line containing both package_name and LAUNCH_SINGLE_TOP
        # and extract the activity name after "cmp="
        lines = logcat_output.split('\n')
        for line in lines:
            if package_name in line and 'LAUNCH_SINGLE_TOP' in line:
                # Look for cmp= pattern
                # Pattern: cmp=package_name/activity_name
                match = re.search(r'cmp=([^\s]+)}', line)
                if match:
                    cmp_value = match.group(1)
                    # The cmp value is in format: package_name/activity_name
                    # We want to return the full cmp value or just the activity name
                    print(f"Found activity: {cmp_value}")
                    return cmp_value
        
        print(f"No LAUNCH_SINGLE_TOP activity found for package: {package_name}")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


if __name__ == "__main__":
    print(find_LAUNCH_SINGLE_TOP_activity(adb_id="9deb5ba5", package_name=find_package_name(app_name="点评")))