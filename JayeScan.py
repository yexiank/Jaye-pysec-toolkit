"""
Jaye家烨
这是一个端口扫描器，很快，速度(线程越高速度越快)由你来定
要多快有多快，但前提是电脑顶的住
为什么有英文?
我觉得帅
个人使用，亦是我的作业
还可以吧，一共也就6个函数

Enjoy hacking, play safe, have fun!
"""
import socket
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

RESET = "\x1b[0m"      # 重置（恢复默认颜色、样式）
BOLD = "\x1b[1m"       # 加粗
COLOR_CYAN = "\x1b[36m"     # 青色
COLOR_GREEN = "\x1b[32m"    # 绿色
COLOR_RED = "\x1b[31m"      # 红色
COLOR_BLUE = "\x1b[34m"     # 蓝色
COLOR_YELLOW = "\x1b[33m"   # 黄色
COLOR_WHITE = "\x1b[37m"    # 白色


# Top 1000端口列表
TOP_1000_PORTS = [
    1, 3, 4, 6, 7, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 33, 37,
    42, 43, 49, 53, 67, 68, 69, 70, 79, 80, 81, 82, 83, 84, 85, 88, 89, 90, 91, 99,
    100, 106, 109, 110, 111, 113, 119, 125, 135, 139, 143, 144, 146, 161, 162, 163, 179, 199, 211, 212,
    222, 254, 255, 256, 259, 264, 280, 311, 318, 330, 337, 345, 349, 366, 369, 370, 371, 372, 383, 389,
    399, 406, 407, 416, 417, 425, 427, 434, 443, 444, 445, 458, 464, 465, 481, 497, 500, 512, 513, 514,
    515, 524, 541, 543, 544, 548, 554, 555, 563, 587, 593, 616, 617, 625, 631, 636, 646, 648, 666, 667,
    668, 683, 687, 691, 700, 705, 711, 714, 720, 722, 726, 749, 765, 777, 783, 787, 800, 801, 808, 843,
    873, 888, 901, 902, 903, 911, 912, 981, 987, 990, 992, 993, 995, 999, 1000, 1001, 1002, 1007, 1009, 1010,
    1011, 1012, 1013, 1014, 1015, 1016, 1017, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033,
    1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053,
    1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073,
    1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093,
    1094, 1095, 1096, 1097, 1098, 1099, 1100, 1102, 1104, 1105, 1106, 1107, 1108, 1110, 1111, 1112, 1113, 1114, 1117, 1119,
    1121, 1122, 1123, 1124, 1126, 1130, 1131, 1132, 1137, 1138, 1141, 1145, 1147, 1148, 1149, 1151, 1152, 1154, 1164, 1165,
    1166, 1169, 1174, 1175, 1183, 1185, 1186, 1187, 1192, 1198, 1199, 1201, 1213, 1216, 1217, 1218, 1233, 1234, 1236, 1244,
    1247, 1248, 1259, 1271, 1272, 1277, 1287, 1296, 1300, 1301, 1309, 1310, 1311, 1322, 1328, 1334, 1352, 1417, 1433, 1434,
    1443, 1455, 1461, 1494, 1500, 1501, 1503, 1521, 1524, 1533, 1556, 1580, 1583, 1594, 1600, 1641, 1658, 1666, 1687, 1688,
    1717, 1718, 1719, 1720, 1721, 1723, 1755, 1761, 1782, 1783, 1801, 1807, 1812, 1839, 1840, 1862, 1863, 1864, 1875, 1900,
    1914, 1935, 1947, 1971, 1972, 1974, 1984, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    2013, 2020, 2021, 2022, 2030, 2049, 2065, 2068, 2099, 2100, 2103, 2105, 2106, 2107, 2111, 2119, 2121, 2126, 2135, 2144,
    2160, 2161, 2170, 2179, 2190, 2191, 2196, 2200, 2202, 2222, 2251, 2260, 2288, 2301, 2323, 2366, 2381, 2399, 2401, 2492,
    2500, 2522, 2525, 2557, 2601, 2602, 2604, 2605, 2607, 2608, 2638, 2701, 2702, 2710, 2717, 2718, 2725, 2800, 2809, 2811,
    2869, 2909, 2910, 2920, 2967, 2968, 2998, 3000, 3001, 3003, 3005, 3006, 3007, 3011, 3013, 3017, 3030, 3031, 3052, 3071,
    3077, 3128, 3168, 3211, 3221, 3260, 3261, 3268, 3269, 3283, 3300, 3301, 3306, 3322, 3323, 3324, 3325, 3333, 3351, 3367,
    3369, 3370, 3371, 3372, 3375, 3389, 3390, 3404, 3476, 3493, 3517, 3527, 3535, 3546, 3551, 3580, 3659, 3689, 3690, 3703,
    3737, 3766, 3784, 3800, 3801, 3809, 3814, 3826, 3827, 3828, 3829, 3851, 3869, 3871, 3878, 3880, 3889, 3905, 3914, 3918,
    3986, 3995, 3998, 4000, 4001, 4002, 4003, 4004, 4005, 4006, 4045, 4111, 4125, 4126, 4129, 4224, 4242, 4279, 4321, 4343,
    4443, 4444, 4445, 4446, 4449, 4550, 4567, 4569, 4662, 4664, 4672, 4711, 4725, 4728, 4741, 4750, 4840, 4843, 4899, 4900,
    4998, 5000, 5001, 5002, 5003, 5004, 5009, 5030, 5033, 5050, 5051, 5054, 5060, 5061, 5080, 5087, 5100, 5101, 5102, 5120,
    5145, 5150, 5151, 5154, 5190, 5200, 5222, 5225, 5226, 5269, 5280, 5298, 5357, 5405, 5414, 5431, 5432, 5440, 5443, 5450,
    5500, 5510, 5544, 5550, 5555, 5560, 5566, 5631, 5633, 5666, 5668, 5669, 5678, 5679, 5718, 5730, 5800, 5801, 5802, 5810,
    5811, 5815, 5822, 5825, 5850, 5859, 5862, 5877, 5900, 5901, 5902, 5903, 5904, 5906, 5907, 5910, 5911, 5915, 5922, 5925,
    5950, 5952, 5959, 5960, 5961, 5962, 5963, 5987, 5988, 5989, 5998, 5999, 6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007,
    6009, 6025, 6059, 6100, 6101, 6106, 6112, 6123, 6129, 6156, 6346, 6389, 6480, 6502, 6514, 6515, 6543, 6547, 6565, 6566,
    6567, 6580, 6646, 6666, 6667, 6668, 6669, 6689, 6692, 6699, 6779, 6788, 6789, 6790, 6831, 6841, 6842, 6888, 6901, 6969,
    7000, 7001, 7002, 7004, 7007, 7019, 7025, 7070, 7100, 7103, 7106, 7200, 7201, 7402, 7435, 7443, 7496, 7511, 7625, 7626,
    7777, 7778, 7779, 7785, 7786, 7800, 7911, 7920, 7921, 7937, 7938, 7999, 8000, 8001, 8002, 8007, 8008, 8009, 8010, 8021,
    8022, 8031, 8042, 8045, 8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090, 8091, 8093, 8099, 8100, 8180,
    8181, 8192, 8193, 8194, 8200, 8222, 8254, 8290, 8291, 8292, 8300, 8333, 8383, 8400, 8402, 8443, 8500, 8600, 8649, 8651,
    8652, 8654, 8701, 8767, 8769, 8800, 8873, 8880, 8883, 8888, 8899, 8900, 8994, 8999, 9000, 9001, 9002, 9003, 9009, 9010,
    9011, 9020, 9021, 9022, 9050, 9071, 9080, 9081, 9090, 9091, 9099, 9100, 9101, 9102, 9103, 9110, 9111, 9200, 9207, 9220,
    9290, 9300, 9306, 9321, 9343, 9344, 9346, 9374, 9380, 9390, 9391, 9392, 9418, 9419, 9420, 9443, 9500, 9502, 9503, 9535,
    9575, 9593, 9594, 9595, 9618, 9666, 9800, 9876, 9877, 9878, 9898, 9900, 9917, 9943, 9944, 9968, 9998, 9999, 10000, 10001,
    10002, 10003, 10004, 10009, 10010, 10012, 10024, 10025, 10082, 10180, 10288, 11110, 11111, 11967, 12000, 12174, 12265, 12345,
    13456, 13722, 13724, 13782, 13783, 14000, 14238, 14441, 14442, 15000, 15002, 15003, 15004, 15742, 16001, 16002, 16003, 16012,
    16016, 16018, 16080, 16992, 16993, 17877, 17988, 18040, 18101, 18988, 19101, 19283, 19315, 19350, 19780, 19801, 19842, 20000,
    20005, 20031, 20221, 20222, 20828, 21571, 22939, 23472, 24800, 25734, 25735, 26214, 27352, 27353, 27355, 27356, 30000, 30718,
    31038, 31337, 32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779, 32780, 32781, 32782, 32783,
    32784, 32785, 33354, 33899, 34571, 34572, 34573, 35500, 38292, 40193, 40911, 41511, 44176, 44442, 44443, 44501, 45000, 49152,
    49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49163, 49165, 49167, 49175, 49176, 49400, 50000, 50001, 50002,
    50003, 50006, 50333, 50389, 50500, 50636, 50800, 51103, 51493, 52673, 52822, 52848, 52869, 54045, 54321, 55055, 55056, 55555,
    55600, 56738, 57294, 57797, 58080, 60000, 60020, 60443, 61532, 61900, 62078, 63331, 64680, 65000, 65129, 65389,
    65533, 65535
]

# 端口信息字典：包含所有1000个端口的服务名称和描述
def _init_port_info():
    """初始化端口信息字典，为所有1000个端口添加服务名称和描述"""
    port_info = {}
    
    # 高危端口详细描述（从原critical_ports迁移）
    critical_descriptions = {
        21: "FTP 文件传输协议，常存在弱口令/匿名访问漏洞",
        22: "SSH 安全远程登录，弱口令爆破首要目标",
        23: "Telnet 明文传输远程服务，凭证易被截获",
        53: "DNS 域名解析服务，缓存投毒风险",
        67: "DHCP 动态主机配置，可伪造地址实施中间人攻击",
        68: "DHCP 客户端服务，同67端口风险",
        69: "TFTP 简易文件传输，常无认证机制",
        80: "HTTP 标准网页服务，目录遍历/注入漏洞高发区",
        443: "HTTPS 加密网页服务，证书配置错误常见",
        8000: "HTTP-ALT 备用Web端口，开发环境常开放",
        8080: "HTTP-Proxy 代理/备用Web服务，常暴露管理后台",
        8443: "HTTPS-ALT 加密备用端口，Jenkins等应用常用",
        3000: "Node.js 前端开发服务，常暴露调试接口",
        5000: "Flask/React Python/前端框架默认端口",
        9000: "Portainer/SonarQube 容器管理/代码审计平台，弱口令风险",
        25: "SMTP 邮件传输协议，可伪造发件人",
        465: "SMTPS 加密邮件传输，配置错误可导致信息泄露",
        587: "SMTP-Submission 邮件提交端口，同25端口风险",
        110: "POP3 邮件接收协议，明文传输凭证",
        995: "POP3S 加密邮件接收，证书验证常被忽略",
        143: "IMAP 邮件同步协议，凭证复用风险高",
        993: "IMAPS 加密邮件同步，配置不当易泄露数据",
        1433: "MSSQL 微软SQL数据库，SA弱口令高危",
        1521: "Oracle 甲骨文数据库，TNS监听漏洞常见",
        3306: "MySQL 开源数据库，root空口令普遍",
        5432: "PostgreSQL 开源数据库，常配置为无密码访问",
        6379: "Redis 内存数据库，未授权访问可直接写SSH密钥",
        11211: "Memcached 缓存服务，UDP反射放大攻击源",
        27017: "MongoDB NoSQL数据库，2015-2017年大规模未授权事件",
        5984: "CouchDB NoSQL数据库，未授权可导致RCE",
        3389: "RDP Windows远程桌面，BlueKeep漏洞高危",
        5900: "VNC 图形远程控制，常无强认证",
        5901: "VNC-1 VNC备用端口，同5900风险",
        6000: "X11 Linux图形界面，可截取屏幕内容",
        135: "MSRPC 微软远程过程调用，永恒之蓝前置条件",
        139: "NetBIOS Windows网络发现，信息泄露风险",
        445: "SMB 文件共享服务，MS17-010漏洞可直接RCE",
        2049: "NFS 网络文件系统，挂载权限配置错误普遍",
        111: "RPCbind RPC服务注册，信息泄露入口",
        161: "SNMP 网络监控协议，团体名爆破可获取设备信息",
        162: "SNMP-Trap 陷阱接收端口，同161风险",
        389: "LDAP 目录服务，凭证泄露导致域渗透",
        636: "LDAPS 加密目录服务，证书错误配置常见",
        9200: "Elasticsearch 搜索引擎，未授权访问可RCE",
        9300: "Elasticsearch-Node 节点通信，未授权可控制集群",
        5601: "Kibana ELK可视化，CVE-2018-17246 RCE漏洞",
        8089: "Splunk 日志分析平台，弱口令可获取敏感日志",
        8888: "Jupyter 数据科学平台，未授权可执行任意代码",
        9418: "Git Git服务协议，可克隆仓库获取源码",
        4243: "Docker-API Docker未授权访问=直接获取root",
        2375: "Docker-REST 未加密Docker API，容器逃逸高危",
        2376: "Docker-TLS TLS加密API，证书验证常被禁用",
        6667: "IRC-Botnet 僵尸网络控制通道，常见于肉鸡",
        6697: "IRC-SSL 加密IRC控制，同6667风险",
        8086: "InfluxDB 时序数据库，1.8前版本未授权访问",
        9090: "WebLogic/Jenkins 中间件管理，反序列化漏洞高发",
        4567: "Metasploit MSF控制端口，暴露可被反制",
        4444: "Metasploit-Payload MSF默认反弹端口，连接即控制",
        12345: "NetBus-Trojan 经典木马端口，持续活跃20年+",
        31337: "Elite-Backdoor 黑客文化端口，常用于隐蔽后门"
    }
    
    # 常见端口服务名称映射
    common_services = {
        1: "TCPMUX", 3: "CompressNet", 4: "Unassigned", 6: "Unassigned", 7: "Echo", 9: "Discard",
        13: "Daytime", 17: "QOTD", 19: "Chargen", 20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet",
        24: "Private", 25: "SMTP", 26: "Unassigned", 30: "Unassigned", 32: "Unassigned", 33: "DSP",
        37: "Time", 42: "WINS", 43: "Whois", 49: "TACACS", 53: "DNS", 67: "DHCP", 68: "DHCP",
        69: "TFTP", 70: "Gopher", 79: "Finger", 80: "HTTP", 81: "HTTP-Alt", 82: "HTTP-Alt",
        83: "HTTP-Alt", 84: "HTTP-Alt", 85: "HTTP-Alt", 88: "Kerberos", 89: "SU-MIT-TG",
        90: "DNSIX", 91: "MIT-DOV", 99: "Metagram", 100: "Unassigned", 106: "POP3PW", 109: "POP2",
        110: "POP3", 111: "RPCbind", 113: "Ident", 119: "NNTP", 125: "Locus-Map", 135: "MSRPC",
        139: "NetBIOS", 143: "IMAP", 144: "News", 146: "ISO-TP0", 161: "SNMP", 162: "SNMP-Trap",
        163: "CMIP", 179: "BGP", 199: "SMUX", 211: "914c/g", 212: "TETP", 222: "rsh-spx",
        254: "Unassigned", 255: "Unassigned", 256: "Unassigned", 259: "ESRO", 264: "BGMP",
        280: "http-mgmt", 311: "Apple-ASL", 318: "TSP", 330: "MySQL", 337: "Unassigned",
        345: "Unassigned", 349: "Unassigned", 366: "ODMR", 369: "Rpc2portmap", 370: "codaauth2",
        371: "ClearCase", 372: "ListProcessor", 383: "HP-OpenView", 389: "LDAP", 399: "ISO-TSAP",
        406: "IMSP", 407: "Timbuktu", 416: "Silverplatter", 417: "Onmux", 425: "ICAD",
        427: "SLP", 434: "MobileIP", 443: "HTTPS", 444: "SNPP", 445: "SMB", 458: "Apple-QuickTime",
        464: "Kerberos", 465: "SMTPS", 481: "Ph", 497: "Retrospect", 500: "ISAKMP", 512: "rexec",
        513: "rlogin", 514: "syslog", 515: "LPD", 524: "NCP", 541: "Uucp-rlogin", 543: "klogin",
        544: "kshell", 548: "AFP", 554: "RTSP", 555: "DSF", 563: "NNTPS", 587: "SMTP-Submission",
        593: "HTTP-RPC", 616: "SCO-Web", 617: "SCO-Web", 625: "OpenDirectory", 631: "IPP",
        636: "LDAPS", 646: "LDP", 648: "RRP", 666: "Doom", 667: "UDP", 668: "MeComm", 683: "CORBA",
        687: "Asipregistry", 691: "MS-Exchange", 700: "EPP", 705: "AgentX", 711: "Cisco-TDP",
        714: "iris-xpcs", 720: "Unassigned", 722: "Unassigned", 726: "Unassigned", 749: "Kerberos",
        765: "webster", 777: "Multiling-HTTP", 783: "SpamAssassin", 787: "Unassigned", 800: "mdbs-daemon",
        801: "Device", 808: "HTTP-Proxy", 843: "Adobe-Flash", 873: "rsync", 888: "cddbp-alt",
        901: "Samba-Swat", 902: "VMware-Auth", 903: "VMware-Auth", 911: "xact-backup", 912: "VMware-Auth",
        981: "SofaWare", 987: "Unassigned", 990: "FTPS", 992: "TelnetS", 993: "IMAPS", 995: "POP3S",
        999: "Applix", 1000: "Cadlock", 1001: "Webpush", 1002: "Windows-ICF", 1007: "Unassigned",
        1009: "Unassigned", 1010: "Surf", 1011: "Unassigned", 1012: "Unassigned", 1013: "Unassigned",
        1014: "Unassigned", 1015: "Unassigned", 1016: "Unassigned", 1017: "Unassigned", 1021: "Unassigned",
        1022: "Unassigned", 1023: "Unassigned", 1024: "Unassigned", 1025: "NFS", 1026: "Unassigned",
        1027: "IIS", 1028: "Unassigned", 1029: "Unassigned", 1030: "Unassigned", 1031: "Unassigned",
        1032: "Unassigned", 1033: "Unassigned", 1034: "Unassigned", 1035: "Unassigned", 1036: "Unassigned",
        1037: "Unassigned", 1038: "Unassigned", 1039: "Unassigned", 1040: "Unassigned", 1041: "Unassigned",
        1042: "Unassigned", 1043: "Unassigned", 1044: "Unassigned", 1045: "Unassigned", 1046: "Unassigned",
        1047: "Unassigned", 1048: "Unassigned", 1049: "Unassigned", 1050: "Unassigned", 1051: "Unassigned",
        1052: "Unassigned", 1053: "Unassigned", 1054: "Unassigned", 1055: "Unassigned", 1056: "Unassigned",
        1057: "Unassigned", 1058: "Unassigned", 1059: "Unassigned", 1060: "Unassigned", 1061: "Unassigned",
        1062: "Unassigned", 1063: "Unassigned", 1064: "Unassigned", 1065: "Unassigned", 1066: "Unassigned",
        1067: "Unassigned", 1068: "Unassigned", 1069: "Unassigned", 1070: "Unassigned", 1071: "Unassigned",
        1072: "Unassigned", 1073: "Unassigned", 1074: "Unassigned", 1075: "Unassigned", 1076: "Unassigned",
        1077: "Unassigned", 1078: "Unassigned", 1079: "Unassigned", 1080: "SOCKS", 1081: "PVUNIWIEN",
        1082: "Unassigned", 1083: "Unassigned", 1084: "Unassigned", 1085: "Unassigned", 1086: "Unassigned",
        1087: "Unassigned", 1088: "Unassigned", 1089: "Unassigned", 1090: "Unassigned", 1091: "Unassigned",
        1092: "Unassigned", 1093: "Unassigned", 1094: "Unassigned", 1095: "Unassigned", 1096: "Unassigned",
        1097: "Unassigned", 1098: "Unassigned", 1099: "RMI", 1100: "POP3", 1102: "Unassigned",
        1104: "Unassigned", 1105: "Unassigned", 1106: "Unassigned", 1107: "Unassigned", 1108: "Unassigned",
        1110: "NFSD", 1111: "Unassigned", 1112: "Unassigned", 1113: "Unassigned", 1114: "Unassigned",
        1117: "Unassigned", 1119: "Unassigned", 1121: "Unassigned", 1122: "Unassigned", 1123: "Unassigned",
        1124: "Unassigned", 1126: "Unassigned", 1130: "Unassigned", 1131: "Unassigned", 1132: "Unassigned",
        1137: "Unassigned", 1138: "Unassigned", 1141: "Unassigned", 1145: "Unassigned", 1147: "Unassigned",
        1148: "Unassigned", 1149: "Unassigned", 1151: "Unassigned", 1152: "Unassigned", 1154: "Unassigned",
        1164: "Unassigned", 1165: "Unassigned", 1166: "Unassigned", 1169: "Unassigned", 1174: "Unassigned",
        1175: "Unassigned", 1183: "Unassigned", 1185: "Unassigned", 1186: "Unassigned", 1187: "Unassigned",
        1192: "Unassigned", 1198: "Unassigned", 1199: "Unassigned", 1201: "Unassigned", 1213: "Unassigned",
        1216: "Unassigned", 1217: "Unassigned", 1218: "Unassigned", 1233: "Unassigned", 1234: "Unassigned",
        1236: "Unassigned", 1244: "Unassigned", 1247: "Unassigned", 1248: "Unassigned", 1259: "Unassigned",
        1271: "Unassigned", 1272: "Unassigned", 1277: "Unassigned", 1287: "Unassigned", 1296: "Unassigned",
        1300: "Unassigned", 1301: "Unassigned", 1309: "Unassigned", 1310: "Unassigned", 1311: "Unassigned",
        1322: "Unassigned", 1328: "Unassigned", 1334: "Unassigned", 1352: "Lotus", 1417: "Timbuktu",
        1433: "MSSQL", 1434: "MSSQL", 1443: "Unassigned", 1455: "ESMTP", 1461: "Unassigned",
        1494: "Citrix", 1500: "Unassigned", 1501: "Unassigned", 1503: "Unassigned", 1521: "Oracle",
        1524: "Unassigned", 1533: "Unassigned", 1556: "Unassigned", 1580: "Unassigned", 1583: "Unassigned",
        1594: "Unassigned", 1600: "Unassigned", 1641: "Unassigned", 1658: "Unassigned", 1666: "Unassigned",
        1687: "Unassigned", 1688: "Unassigned", 1717: "Fjswappnp", 1718: "Unassigned", 1719: "Unassigned",
        1720: "H323", 1721: "Unassigned", 1723: "PPTP", 1755: "MS-Media", 1761: "Unassigned",
        1782: "Unassigned", 1783: "Unassigned", 1801: "Unassigned", 1807: "Unassigned", 1812: "Unassigned",
        1839: "Unassigned", 1840: "Unassigned", 1862: "Unassigned", 1863: "Unassigned", 1864: "Unassigned",
        1875: "Unassigned", 1900: "SSDP", 1914: "Unassigned", 1935: "RTMP", 1947: "Unassigned",
        1971: "Unassigned", 1972: "Unassigned", 1974: "Unassigned", 1984: "Unassigned", 1998: "Unassigned",
        1999: "Unassigned", 2000: "Unassigned", 2001: "Unassigned", 2002: "Unassigned", 2003: "Unassigned",
        2004: "Unassigned", 2005: "Unassigned", 2006: "Unassigned", 2007: "Unassigned", 2008: "Unassigned",
        2009: "Unassigned", 2010: "Unassigned", 2013: "Unassigned", 2020: "Unassigned", 2021: "Unassigned",
        2022: "Unassigned", 2030: "Unassigned", 2049: "NFS", 2065: "Unassigned", 2068: "Unassigned",
        2099: "Unassigned", 2100: "Unassigned", 2103: "Unassigned", 2105: "Unassigned", 2106: "Unassigned",
        2107: "Unassigned", 2111: "Unassigned", 2119: "Unassigned", 2121: "Unassigned", 2126: "Unassigned",
        2135: "Unassigned", 2144: "Unassigned", 2160: "Unassigned", 2161: "Unassigned", 2170: "Unassigned",
        2179: "VMware", 2190: "Unassigned", 2191: "Unassigned", 2196: "Unassigned", 2200: "Unassigned",
        2202: "Unassigned", 2222: "Unassigned", 2251: "Unassigned", 2260: "Unassigned", 2288: "Unassigned",
        2301: "Unassigned", 2323: "Unassigned", 2366: "Unassigned", 2381: "Unassigned", 2399: "Unassigned",
        2401: "Unassigned", 2492: "Unassigned", 2500: "Unassigned", 2522: "Unassigned", 2525: "Unassigned",
        2557: "Unassigned", 2601: "Unassigned", 2602: "Unassigned", 2604: "Unassigned", 2605: "Unassigned",
        2607: "Unassigned", 2608: "Unassigned", 2638: "Unassigned", 2701: "Unassigned", 2702: "Unassigned",
        2710: "Unassigned", 2717: "Unassigned", 2718: "Unassigned", 2725: "Unassigned", 2800: "Unassigned",
        2809: "Unassigned", 2811: "Unassigned", 2869: "Unassigned", 2909: "Unassigned", 2910: "Unassigned",
        2920: "Unassigned", 2967: "Unassigned", 2968: "Unassigned", 2998: "Unassigned", 3000: "Node.js",
        3001: "Unassigned", 3003: "Unassigned", 3005: "Unassigned", 3006: "Unassigned", 3007: "Unassigned",
        3011: "Unassigned", 3013: "Unassigned", 3017: "Unassigned", 3030: "Unassigned", 3031: "Unassigned",
        3052: "Unassigned", 3071: "Unassigned", 3077: "Unassigned", 3128: "Squid", 3168: "Unassigned",
        3211: "Unassigned", 3221: "Unassigned", 3260: "iSCSI", 3261: "Unassigned", 3268: "Unassigned",
        3269: "Unassigned", 3283: "Unassigned", 3300: "Unassigned", 3301: "Unassigned", 3306: "MySQL",
        3322: "Unassigned", 3323: "Unassigned", 3324: "Unassigned", 3325: "Unassigned", 3333: "Unassigned",
        3351: "Unassigned", 3367: "Unassigned", 3369: "Unassigned", 3370: "Unassigned", 3371: "Unassigned",
        3372: "Unassigned", 3375: "Unassigned", 3389: "RDP", 3390: "Unassigned", 3404: "Unassigned",
        3476: "Unassigned", 3493: "Unassigned", 3517: "Unassigned", 3527: "Unassigned", 3535: "Unassigned",
        3546: "Unassigned", 3551: "Unassigned", 3580: "Unassigned", 3659: "Unassigned", 3689: "Unassigned",
        3690: "Unassigned", 3703: "Unassigned", 3737: "Unassigned", 3766: "Unassigned", 3784: "Unassigned",
        3800: "Unassigned", 3801: "Unassigned", 3809: "Unassigned", 3814: "Unassigned", 3826: "Unassigned",
        3827: "Unassigned", 3828: "Unassigned", 3829: "Unassigned", 3851: "Unassigned", 3869: "Unassigned",
        3871: "Unassigned", 3878: "Unassigned", 3880: "Unassigned", 3889: "Unassigned", 3905: "Unassigned",
        3914: "Unassigned", 3918: "Unassigned", 3986: "Unassigned", 3995: "Unassigned", 3998: "Unassigned",
        4000: "Unassigned", 4001: "Unassigned", 4002: "Unassigned", 4003: "Unassigned", 4004: "Unassigned",
        4005: "Unassigned", 4006: "Unassigned", 4045: "Unassigned", 4111: "Unassigned", 4125: "Unassigned",
        4126: "Unassigned", 4129: "Unassigned", 4224: "Unassigned", 4242: "Unassigned", 4279: "Unassigned",
        4321: "Unassigned", 4343: "Unassigned", 4443: "Unassigned", 4444: "Metasploit", 4445: "Unassigned",
        4446: "Unassigned", 4449: "Unassigned", 4550: "Unassigned", 4567: "Metasploit", 4569: "Unassigned",
        4662: "Unassigned", 4664: "Unassigned", 4672: "Unassigned", 4711: "Unassigned", 4725: "Unassigned",
        4728: "Unassigned", 4741: "Unassigned", 4750: "Unassigned", 4840: "Unassigned", 4843: "Unassigned",
        4899: "Unassigned", 4900: "Unassigned", 4998: "Unassigned", 5000: "Flask", 5001: "Unassigned",
        5002: "Unassigned", 5003: "Unassigned", 5004: "Unassigned", 5009: "Unassigned", 5030: "Unassigned",
        5033: "Unassigned", 5050: "Unassigned", 5051: "Unassigned", 5054: "Unassigned", 5060: "Unassigned",
        5061: "Unassigned", 5080: "Unassigned", 5087: "Unassigned", 5100: "Unassigned", 5101: "Unassigned",
        5102: "Unassigned", 5120: "Unassigned", 5145: "Unassigned", 5150: "Unassigned", 5151: "Unassigned",
        5154: "Unassigned", 5190: "Unassigned", 5200: "Unassigned", 5222: "Unassigned", 5225: "Unassigned",
        5226: "Unassigned", 5269: "Unassigned", 5280: "Unassigned", 5298: "Unassigned", 5357: "MDNS",
        5405: "Unassigned", 5414: "Unassigned", 5431: "Unassigned", 5432: "PostgreSQL", 5440: "Unassigned",
        5443: "Unassigned", 5450: "Unassigned", 5500: "Unassigned", 5510: "Unassigned", 5544: "Unassigned",
        5550: "Unassigned", 5555: "Unassigned", 5560: "Unassigned", 5566: "Unassigned", 5631: "Unassigned",
        5633: "Unassigned", 5666: "Unassigned", 5668: "Unassigned", 5669: "Unassigned", 5678: "Unassigned",
        5679: "Unassigned", 5718: "Unassigned", 5730: "Unassigned", 5800: "Unassigned", 5801: "Unassigned",
        5802: "Unassigned", 5810: "Unassigned", 5811: "Unassigned", 5815: "Unassigned", 5822: "Unassigned",
        5825: "Unassigned", 5850: "Unassigned", 5859: "Unassigned", 5862: "Unassigned", 5877: "Unassigned",
        5900: "VNC", 5901: "VNC", 5902: "VNC", 5903: "VNC", 5904: "VNC", 5906: "VNC", 5907: "VNC",
        5910: "VNC", 5911: "VNC", 5915: "VNC", 5922: "VNC", 5925: "VNC", 5950: "Unassigned",
        5952: "Unassigned", 5959: "Unassigned", 5960: "Unassigned", 5961: "Unassigned", 5962: "Unassigned",
        5963: "Unassigned", 5987: "Unassigned", 5988: "Unassigned", 5989: "Unassigned", 5998: "Unassigned",
        5999: "Unassigned", 6000: "X11", 6001: "X11", 6002: "X11", 6003: "X11", 6004: "X11", 6005: "X11",
        6006: "X11", 6007: "X11", 6009: "Unassigned", 6025: "Unassigned", 6059: "Unassigned",
        6100: "Unassigned", 6101: "Unassigned", 6106: "Unassigned", 6112: "Unassigned", 6123: "Unassigned",
        6129: "Unassigned", 6156: "Unassigned", 6346: "Unassigned", 6389: "Unassigned", 6480: "Unassigned",
        6502: "Unassigned", 6514: "Unassigned", 6515: "Unassigned", 6543: "Unassigned", 6547: "Unassigned",
        6565: "Unassigned", 6566: "Unassigned", 6567: "Unassigned", 6580: "Unassigned", 6646: "Unassigned",
        6666: "Unassigned", 6667: "IRC", 6668: "IRC", 6669: "IRC", 6689: "Unassigned", 6692: "Unassigned",
        6699: "Unassigned", 6779: "Unassigned", 6788: "Unassigned", 6789: "Unassigned", 6790: "Unassigned",
        6831: "Unassigned", 6841: "Unassigned", 6842: "Unassigned", 6888: "Unassigned", 6901: "Unassigned",
        6969: "Unassigned", 7000: "Unassigned", 7001: "Unassigned", 7002: "Unassigned", 7004: "Unassigned",
        7007: "Unassigned", 7019: "Unassigned", 7025: "Unassigned", 7070: "Unassigned", 7100: "Unassigned",
        7103: "Unassigned", 7106: "Unassigned", 7200: "Unassigned", 7201: "Unassigned", 7402: "Unassigned",
        7435: "Unassigned", 7443: "Unassigned", 7496: "Unassigned", 7511: "Unassigned", 7625: "Unassigned",
        7626: "Unassigned", 7777: "Unassigned", 7778: "Unassigned", 7779: "Unassigned", 7785: "Unassigned",
        7786: "Unassigned", 7800: "Unassigned", 7911: "Unassigned", 7920: "Unassigned", 7921: "Unassigned",
        7937: "Unassigned", 7938: "Unassigned", 7999: "Unassigned", 8000: "HTTP-Alt", 8001: "HTTP-Alt",
        8002: "HTTP-Alt", 8007: "HTTP-Alt", 8008: "HTTP-Alt", 8009: "HTTP-Alt", 8010: "HTTP-Alt",
        8021: "HTTP-Alt", 8022: "HTTP-Alt", 8031: "HTTP-Alt", 8042: "HTTP-Alt", 8045: "HTTP-Alt",
        8080: "HTTP-Proxy", 8081: "HTTP-Proxy", 8082: "HTTP-Proxy", 8083: "HTTP-Proxy", 8084: "HTTP-Proxy",
        8085: "HTTP-Proxy", 8086: "InfluxDB", 8087: "HTTP-Proxy", 8088: "HTTP-Proxy", 8089: "Splunk",
        8090: "HTTP-Proxy", 8091: "HTTP-Proxy", 8093: "HTTP-Proxy", 8099: "HTTP-Proxy", 8100: "HTTP-Proxy",
        8180: "HTTP-Proxy", 8181: "HTTP-Proxy", 8192: "HTTP-Proxy", 8193: "HTTP-Proxy", 8194: "HTTP-Proxy",
        8200: "HTTP-Proxy", 8222: "HTTP-Proxy", 8254: "HTTP-Proxy", 8290: "HTTP-Proxy", 8291: "HTTP-Proxy",
        8292: "HTTP-Proxy", 8300: "HTTP-Proxy", 8333: "HTTP-Proxy", 8383: "HTTP-Proxy", 8400: "HTTP-Proxy",
        8402: "HTTP-Proxy", 8443: "HTTPS-Alt", 8500: "HTTP-Proxy", 8600: "HTTP-Proxy", 8649: "HTTP-Proxy",
        8651: "HTTP-Proxy", 8652: "HTTP-Proxy", 8654: "HTTP-Proxy", 8701: "HTTP-Proxy", 8767: "HTTP-Proxy",
        8769: "HTTP-Proxy", 8800: "HTTP-Proxy", 8873: "HTTP-Proxy", 8880: "HTTP-Proxy", 8883: "HTTP-Proxy",
        8888: "Jupyter", 8899: "HTTP-Proxy", 8900: "HTTP-Proxy", 8994: "HTTP-Proxy", 8999: "HTTP-Proxy",
        9000: "SonarQube", 9001: "HTTP-Proxy", 9002: "HTTP-Proxy", 9003: "HTTP-Proxy", 9009: "HTTP-Proxy",
        9010: "HTTP-Proxy", 9011: "HTTP-Proxy", 9020: "HTTP-Proxy", 9021: "HTTP-Proxy", 9022: "HTTP-Proxy",
        9050: "HTTP-Proxy", 9071: "HTTP-Proxy", 9080: "HTTP-Proxy", 9081: "HTTP-Proxy", 9090: "WebLogic",
        9091: "HTTP-Proxy", 9099: "HTTP-Proxy", 9100: "HTTP-Proxy", 9101: "HTTP-Proxy", 9102: "HTTP-Proxy",
        9103: "HTTP-Proxy", 9110: "HTTP-Proxy", 9111: "HTTP-Proxy", 9200: "Elasticsearch", 9207: "HTTP-Proxy",
        9220: "HTTP-Proxy", 9290: "HTTP-Proxy", 9300: "Elasticsearch", 9306: "HTTP-Proxy", 9321: "HTTP-Proxy",
        9343: "HTTP-Proxy", 9344: "HTTP-Proxy", 9346: "HTTP-Proxy", 9374: "HTTP-Proxy", 9380: "HTTP-Proxy",
        9390: "HTTP-Proxy", 9391: "HTTP-Proxy", 9392: "HTTP-Proxy", 9418: "Git", 9419: "HTTP-Proxy",
        9420: "HTTP-Proxy", 9443: "HTTPS-Alt", 9500: "HTTP-Proxy", 9502: "HTTP-Proxy", 9503: "HTTP-Proxy",
        9535: "HTTP-Proxy", 9575: "HTTP-Proxy", 9593: "HTTP-Proxy", 9594: "HTTP-Proxy", 9595: "HTTP-Proxy",
        9618: "HTTP-Proxy", 9666: "HTTP-Proxy", 9800: "HTTP-Proxy", 9876: "HTTP-Proxy", 9877: "HTTP-Proxy",
        9878: "HTTP-Proxy", 9898: "HTTP-Proxy", 9900: "HTTP-Proxy", 9917: "HTTP-Proxy", 9943: "HTTP-Proxy",
        9944: "HTTP-Proxy", 9968: "HTTP-Proxy", 9998: "HTTP-Proxy", 9999: "HTTP-Proxy", 10000: "Webmin",
        10001: "HTTP-Proxy", 10002: "HTTP-Proxy", 10003: "HTTP-Proxy", 10004: "HTTP-Proxy", 10009: "HTTP-Proxy",
        10010: "HTTP-Proxy", 10012: "HTTP-Proxy", 10024: "HTTP-Proxy", 10025: "HTTP-Proxy", 10082: "HTTP-Proxy",
        10180: "HTTP-Proxy", 10288: "HTTP-Proxy", 11110: "HTTP-Proxy", 11111: "HTTP-Proxy", 11967: "HTTP-Proxy",
        12000: "HTTP-Proxy", 12174: "HTTP-Proxy", 12265: "HTTP-Proxy", 12345: "NetBus", 13456: "HTTP-Proxy",
        13722: "HTTP-Proxy", 13724: "HTTP-Proxy", 13782: "HTTP-Proxy", 13783: "HTTP-Proxy", 14000: "HTTP-Proxy",
        14238: "HTTP-Proxy", 14441: "HTTP-Proxy", 14442: "HTTP-Proxy", 15000: "HTTP-Proxy", 15002: "HTTP-Proxy",
        15003: "HTTP-Proxy", 15004: "HTTP-Proxy", 15742: "HTTP-Proxy", 16001: "HTTP-Proxy", 16002: "HTTP-Proxy",
        16003: "HTTP-Proxy", 16012: "HTTP-Proxy", 16016: "HTTP-Proxy", 16018: "HTTP-Proxy", 16080: "HTTP-Proxy",
        16992: "HTTP-Proxy", 16993: "HTTP-Proxy", 17877: "HTTP-Proxy", 17988: "HTTP-Proxy", 18040: "HTTP-Proxy",
        18101: "HTTP-Proxy", 18988: "HTTP-Proxy", 19101: "HTTP-Proxy", 19283: "HTTP-Proxy", 19315: "HTTP-Proxy",
        19350: "HTTP-Proxy", 19780: "HTTP-Proxy", 19801: "HTTP-Proxy", 19842: "HTTP-Proxy", 20000: "HTTP-Proxy",
        20005: "HTTP-Proxy", 20031: "HTTP-Proxy", 20221: "HTTP-Proxy", 20222: "HTTP-Proxy", 20828: "HTTP-Proxy",
        21571: "HTTP-Proxy", 22939: "HTTP-Proxy", 23472: "HTTP-Proxy", 24800: "HTTP-Proxy", 25734: "HTTP-Proxy",
        25735: "HTTP-Proxy", 26214: "HTTP-Proxy", 27352: "HTTP-Proxy", 27353: "HTTP-Proxy", 27355: "HTTP-Proxy",
        27356: "HTTP-Proxy", 30000: "HTTP-Proxy", 30718: "HTTP-Proxy", 31038: "HTTP-Proxy", 31337: "Elite",
        32768: "Unassigned", 32769: "Unassigned", 32770: "Unassigned", 32771: "Unassigned", 32772: "Unassigned",
        32773: "Unassigned", 32774: "Unassigned", 32775: "Unassigned", 32776: "Unassigned", 32777: "Unassigned",
        32778: "Unassigned", 32779: "Unassigned", 32780: "Unassigned", 32781: "Unassigned", 32782: "Unassigned",
        32783: "Unassigned", 32784: "Unassigned", 32785: "Unassigned", 33354: "HTTP-Proxy", 33899: "HTTP-Proxy",
        34571: "HTTP-Proxy", 34572: "HTTP-Proxy", 34573: "HTTP-Proxy", 35500: "HTTP-Proxy", 38292: "HTTP-Proxy",
        40193: "HTTP-Proxy", 40911: "HTTP-Proxy", 41511: "HTTP-Proxy", 44176: "HTTP-Proxy", 44442: "HTTP-Proxy",
        44443: "HTTP-Proxy", 44501: "HTTP-Proxy", 45000: "HTTP-Proxy", 49152: "Unassigned", 49153: "Unassigned",
        49154: "Unassigned", 49155: "Unassigned", 49156: "Unassigned", 49157: "Unassigned", 49158: "Unassigned",
        49159: "Unassigned", 49160: "Unassigned", 49161: "Unassigned", 49163: "Unassigned", 49165: "Unassigned",
        49167: "Unassigned", 49175: "Unassigned", 49176: "Unassigned", 49400: "HTTP-Proxy", 50000: "HTTP-Proxy",
        50001: "HTTP-Proxy", 50002: "HTTP-Proxy", 50003: "HTTP-Proxy", 50006: "HTTP-Proxy", 50333: "HTTP-Proxy",
        50389: "HTTP-Proxy", 50500: "HTTP-Proxy", 50636: "HTTP-Proxy", 50800: "HTTP-Proxy", 51103: "HTTP-Proxy",
        51493: "HTTP-Proxy", 52673: "HTTP-Proxy", 52822: "HTTP-Proxy", 52848: "HTTP-Proxy", 52869: "HTTP-Proxy",
        54045: "HTTP-Proxy", 54321: "HTTP-Proxy", 55055: "HTTP-Proxy", 55056: "HTTP-Proxy", 55555: "HTTP-Proxy",
        55600: "HTTP-Proxy", 56738: "HTTP-Proxy", 57294: "HTTP-Proxy", 57797: "HTTP-Proxy", 58080: "HTTP-Proxy",
        60000: "HTTP-Proxy", 60020: "HTTP-Proxy", 60443: "HTTP-Proxy", 61532: "HTTP-Proxy", 61900: "HTTP-Proxy",
        62078: "HTTP-Proxy", 63331: "HTTP-Proxy", 64680: "HTTP-Proxy", 65000: "HTTP-Proxy", 65129: "HTTP-Proxy",
        65389: "HTTP-Proxy", 65535: "Unassigned"
    }
    
    # 为所有1000个端口创建信息字典
    for port in TOP_1000_PORTS:
        service_name = common_services.get(port, "Unknown")
        if port in critical_descriptions:
            description = critical_descriptions[port]
        else:
            # 为没有详细描述的端口生成通用描述
            if service_name == "Unknown" or service_name == "Unassigned":
                description = f"端口 {port}，未分配或未知服务"
            else:
                description = f"{service_name} 服务端口"
        port_info[port] = {"name": service_name, "description": description, "critical": port in critical_descriptions}
    
    return port_info

# 初始化端口信息字典
PORT_INFO = _init_port_info()

#单扫描
def scan_port(adder):
    ip, port = adder
    sock = None
    try:
        # 创建TCP连接的socket，IPv4协议
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)  # 设置超时时间
        result = sock.connect_ex((ip, port))  # 尝试连接端口，返回0表示连接成功
        if result == 0:  # 如果连接成功，说明端口是开放的
            return port
        else:
            return None
    except socket.gaierror:  # 检测IP地址解析错误（比如IP格式不对）
        return None
    except Exception:  # 捕获其他所有异常
        return None
    finally:  # 无论有没有错误都会执行这里，确保socket被关闭
        if sock is not None:
            sock.close()

#多线程扫描
def scan_ports_concurrently(ip, start_port, end_port, max_workers=200, step=400):
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
        print("端口范围不合法，应在 1-65535 之间，且起始端口不大于结束端口。")
        return

    open_ports = []
    # 创建线程池，最多max_workers个线程同时工作
    with ThreadPoolExecutor(max_workers) as pool:
        # 分块扫描，使用tqdm显示进度
        for block_start in tqdm(range(start_port, end_port + 1, step), desc="扫描进度"):
            # 计算当前块的结束端口，保证不超过end_port
            # step-1是因为块的端口区间是包含block_start的，避免多扫端口
            block_end = min((block_start + step - 1), end_port)
            results = pool.map(scan_port, ((ip, port) for port in range(block_start, block_end + 1)))
            # pool.map是线程池里面的多个线程一起去跑
            # 第一个参数是要跑的函数，第二个参数是要传给函数的参数列表
            # 因为scan_port里面只有一个参数adder，所以我们传入元组(ip,port)
            # 但还要保证port能遍历整个端口范围，所以这里用生成器表达式
            # 生成所有(ip,port)的组合
            
            # 把开放的端口都收集到列表里面
            for r in results:
                if r is not None:
                    open_ports.append(r)

    return open_ports  # 把列表返回出去

#常用扫描
def top_1000(ip):
    """扫描Top 1000常用端口"""
    open_ports = []
    with ThreadPoolExecutor(max_workers=200) as pool:
        # 创建所有扫描任务
        tasks = [(ip, port) for port in TOP_1000_PORTS]
        
        # 提交任务并显示进度
        results = list(tqdm(pool.map(scan_port, tasks), total=len(TOP_1000_PORTS), desc="扫描进度"))
    
    # 收集开放的端口
    for result in results:
        if result is not None:
            open_ports.append(result)
    
    return open_ports

#输出样式
def input_result(open_ports):
    """输出端口扫描结果，显示端口号、服务名称和描述"""
    if open_ports:
        print(f"\n{BOLD}{COLOR_CYAN}{'='*80}{RESET}")
        print(f"{BOLD}{COLOR_CYAN}PORT SCAN RESULTS{RESET} {COLOR_WHITE}({len(open_ports)} open port{'s' if len(open_ports) > 1 else ''}){RESET}")
        print(f"{BOLD}{COLOR_CYAN}{'='*80}{RESET}")
        print(f"{COLOR_WHITE}{'PORT':<8} {'STATE':<8} {'SERVICE':<20} {'DESCRIPTION'}{RESET}")
        print(f"{COLOR_CYAN}{'-'*80}{RESET}")
        
        for port in sorted(open_ports):
            if port in PORT_INFO:
                port_data = PORT_INFO[port]
                service_name = port_data["name"]
                description = port_data["description"]
                is_critical = port_data["critical"]
                
                if is_critical:
                    # 高危端口：红色警告，类似nmap风格
                    print(f"{COLOR_RED}{BOLD}{port:<8}{RESET} {COLOR_RED}{'open':<8}{RESET} {COLOR_YELLOW}{service_name:<20}{RESET} {COLOR_RED}{description}{RESET}")
                else:
                    # 普通端口：绿色正常状态
                    print(f"{COLOR_GREEN}{port:<8}{RESET} {COLOR_GREEN}{'open':<8}{RESET} {COLOR_WHITE}{service_name:<20}{RESET} {COLOR_GREEN}{description}{RESET}")
            else:
                # 不在Top 1000列表中的端口
                print(f"{COLOR_CYAN}{port:<8}{RESET} {COLOR_CYAN}{'open':<8}{RESET} {COLOR_BLUE}{'unknown':<20}{RESET} {COLOR_CYAN}Unknown service{RESET}")
        
        print(f"{BOLD}{COLOR_CYAN}{'='*80}{RESET}\n")
    else:
        print(f"\n{BOLD}{COLOR_BLUE}[-]{RESET} {COLOR_BLUE}No open ports detected{RESET}\n")

#主函数
def main():
    # 欢迎界面
    title = "JayeScan"
    width = 60
    padding = (width - len(title)) // 2
    print(f"\n{BOLD}{COLOR_CYAN}{'='*width}{RESET}")
    print(f"{BOLD}{COLOR_CYAN}{' '*padding}{title}{RESET}")
    print(f"{BOLD}{COLOR_CYAN}{'='*width}{RESET}\n")
    
    # 输入目标IP
    ip = input(f"{COLOR_CYAN}[*]{RESET} {COLOR_WHITE}Target IP{RESET} {COLOR_CYAN}[127.0.0.1]:{RESET} ").strip() or "127.0.0.1"
    
    # 输入端口范围
    port_in = input(f"{COLOR_CYAN}[*]{RESET} {COLOR_WHITE}Port Range{RESET} {COLOR_CYAN}[Top1000]:{RESET} ").strip()
    
    print()  # 空行分隔
    
    if port_in == "":
        # Top 1000扫描
        input_result(top_1000(ip))
    else:
        if "-" in port_in:
            # 端口范围扫描
            try:
                parts = port_in.split("-")
                if len(parts) != 2:
                    print(f"{COLOR_RED}[!]{RESET} {COLOR_RED}格式错误：端口范围格式应为 起始端口-结束端口{RESET}")
                    return
                s, e = map(int, parts)
                m = int(input(f"{COLOR_CYAN}[*]{RESET} {COLOR_WHITE}Threads{RESET} {COLOR_CYAN}[200]:{RESET} ").strip() or 200)
                print()  # 空行分隔
                sp = m * 2
                ports = scan_ports_concurrently(ip, s, e, m, sp)
                input_result(ports)
            except ValueError:
                print(f"{COLOR_RED}[!]{RESET} {COLOR_RED}格式错误：请输入有效的数字{RESET}")
        else:
            # 单端口扫描
            try:
                p = int(port_in)
                if not (1 <= p <= 65535):
                    print(f"{COLOR_RED}[!]{RESET} {COLOR_RED}端口范围不合法，应在 1-65535 之间{RESET}")
                else:
                    print(f"\n{COLOR_CYAN}{'='*60}{RESET}")
                    if scan_port((ip, p)):
                        print(f"{COLOR_GREEN}[+] Port {p} is {BOLD}OPEN{RESET}{COLOR_GREEN}{RESET}")
                    else:
                        print(f"{COLOR_BLUE}[-] Port {p} is {BOLD}CLOSED{RESET}{COLOR_BLUE}{RESET}")
                    print(f"{COLOR_CYAN}{'='*60}{RESET}\n")
            except ValueError:
                print(f"{COLOR_RED}[!]{RESET} {COLOR_RED}格式错误：请输入有效的端口号{RESET}")

if __name__ == "__main__":
    main()