import os
import random
import uuid

# 简历输出目录
output_dir = "resumes"
os.makedirs(output_dir, exist_ok=True)

# 基础数据池
surnames = ["张", "李", "王", "赵", "陈", "刘", "吴", "孙", "周", "郑", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜"]
given_names = ["伟", "娜", "强", "敏", "刚", "芳", "平", "梅", "杰", "华", "秀英", "民", "军", "洋", "勇", "艳", "博", "磊", "霞", "婷", "思", "远", "静", "超", "明", "建国", "和平", "建军", "志强", "文", "武", "浩", "然"]

# ================= 行业角色定义 (累加) =================

# 1. 通用行业
general_roles = [
    {
        "role": "金融分析师",
        "desc_template": "具备CFA{level}资格，拥有扎实的财务分析能力。善于通过数据分析发现投资机会。",
        "exp_template": "- 专注于{sector}行业的深度研究，撰写多篇行业报告。\n- 构建财务估值模型，为投资提供支持。\n- 参与上市公司调研。",
        "skills": ["财务分析", "估值建模", "Bloomberg", "Wind", "Python"],
        "vars": {
            "level": ["一级", "二级", "三级"],
            "sector": ["新能源", "TMT", "医药", "消费", "制造"]
        }
    },
    {
        "role": "市场经理",
        "desc_template": "{years}年市场营销经验，擅长{focus}。具有成功的千万级预算项目管理经验。",
        "exp_template": "- 策划并执行了年度{campaign}活动，曝光量超千万。\n- 统筹管理新媒体矩阵，粉丝增长{number}万。\n- 负责KOL合作筛选与谈判。",
        "skills": ["品牌策略", "整合营销", "SEO/SEM", "项目管理"],
        "vars": {
            "focus": ["品牌推广", "数字营销", "渠道拓展"],
            "campaign": ["新品发布", "双11大促", "品牌升级", "节日营销"],
            "number": ["50", "100", "200", "10"]
        }
    },
    {
        "role": "平面设计师",
        "desc_template": "拥有敏锐的色彩感和独到的审美。擅长{type}设计。",
        "exp_template": "- 主导了多个{project}的视觉升级项目。\n- 负责公司官网及APP界面的UI/UX设计。\n- 制作高转化率的广告素材。",
        "skills": ["Photoshop", "Illustrator", "Sketch", "Figma", "After Effects"],
        "vars": {
            "type": ["品牌VI", "UI界面", "电商视觉", "插画"],
            "project": ["新消费品牌", "企业形象", "活动主视觉"]
        }
    },
    {
        "role": "人力资源主管",
        "desc_template": "精通人力资源六大模块，尤其擅长{module}。致力于通过人才战略推动业务发展。",
        "exp_template": "- 负责{dept}部门的招聘工作，招聘达成率100%。\n- 搭建员工培训体系，组织领导力课程。\n- 处理复杂的员工关系问题。",
        "skills": ["招聘与配置", "培训与开发", "绩效管理", "薪酬福利"],
        "vars": {
            "module": ["招聘", "员工关系", "薪酬绩效"],
            "dept": ["研发", "销售", "运营", "职能"]
        }
    },
    {
        "role": "教师",
        "desc_template": "持有{cert}教师资格证，热爱教育事业。教学风格{style}。",
        "exp_template": "- 担任{grade}年级{subject}教学工作，成绩优异。\n- 组织各类课外活动，提升学生综合素质。\n- 多次获得校级优秀教师称号。",
        "skills": ["课堂管理", "教案设计", "心理辅导", "多媒体教学"],
        "vars": {
            "cert": ["高级中学", "初级中学", "小学"],
            "style": ["亲切自然", "严谨治学", "幽默风趣"],
            "grade": ["初一", "初二", "高一", "高二"],
            "subject": ["英语", "数学", "语文", "物理"]
        }
    },
    {
        "role": "销售总监",
        "desc_template": "10年B2B销售经验，拥有丰富的{resource}。擅长组建狼性销售团队。",
        "exp_template": "- 负责{region}区域的市场拓展，连续超额完成指标。\n- 建立了完善的代理商体系。\n- 制定销售策略，大幅提升团队人效。",
        "skills": ["大客户销售", "渠道管理", "商务谈判", "战略规划"],
        "vars": {
            "resource": ["客户资源", "渠道资源", "政府资源"],
            "region": ["华东", "华南", "华北", "西部"]
        }
    },
    {
        "role": "护士",
        "desc_template": "拥有主管护师职称，5年{dept}工作经验。具备极强的抗压能力。",
        "exp_template": "- 熟练操作各类急救设备。\n- 负责病人的生命体征监测和基础护理。\n- 严格执行无菌操作规范。",
        "skills": ["急危重症护理", "静脉穿刺", "ACLS", "院感控制"],
        "vars": {
            "dept": ["ICU", "急诊科", "外科", "内科"]
        }
    },
    {
        "role": "土木工程师",
        "desc_template": "拥有注册结构工程师资格。熟悉建筑规范，参与过多个{building}项目。",
        "exp_template": "- 负责结构设计与计算，确保安全与经济性。\n- 配合建筑师完成方案设计。\n- 协调施工现场的技术问题。",
        "skills": ["PKPM", "AutoCAD", "Revit", "结构力学"],
        "vars": {
            "building": ["商业综合体", "超高层建筑", "住宅小区", "公共设施"]
        }
    },
    {
        "role": "律师",
        "desc_template": "通过法律职业资格考试。擅长{field}领域的法律事务。",
        "exp_template": "- 负责构建法律风险防控体系，审核合同。\n- 处理投融资相关的尽职调查。\n- 代理多起{case_type}案件，维护客户权益。",
        "skills": ["合同审核", "诉讼仲裁", "知识产权", "合规管理"],
        "vars": {
            "field": ["公司法", "知识产权", "劳动法", "合同法"],
            "case_type": ["民商事", "不正当竞争", "劳动争议"]
        }
    }
]

# 2. 计算机/互联网行业
tech_roles = [
    {
        "role": "Python后端工程师",
        "desc_template": "拥有{years}年Python开发经验，精通Django/Flask框架。熟悉高并发系统设计。",
        "exp_template": "- 负责{system}核心模块开发，代码覆盖率提升至90%。\n- 优化数据库查询，接口响应时间降低50%。\n- 进行微服务拆分，提升系统可扩展性。",
        "skills": ["Python", "Django", "FastAPI", "MySQL", "Redis", "Docker", "Celery"],
        "vars": {
            "system": ["电商", "社交", "内容管理", "金融支付"]
        }
    },
    {
        "role": "Java开发工程师",
        "desc_template": "精通Java并发编程和JVM调优，{years}年大厂经验。熟悉Spring Boot/Cloud全家桶。",
        "exp_template": "- 设计并重构了旧版{system}系统，解决了历史遗留的性能瓶颈。\n- 引入RocketMQ削峰填谷，能够支撑百万级并发。\n- 负责核心业务链路的稳定性建设。",
        "skills": ["Java", "Spring Boot", "MyBatis", "Dubbo", "Kafka", "Elasticsearch"],
        "vars": {
            "system": ["订单交易", "物流配送", "CRM", "结算平台"]
        }
    },
    {
        "role": "前端开发工程师",
        "desc_template": "专注于Web前端技术，熟练掌握Vue/React生态。{years}年经验，追求极致用户体验。",
        "exp_template": "- 主导公司{project}项目的前端架构搭建，统一UI组件库。\n- 优化首屏加载速度，LCP指标提升40%。\n- 开发复杂可视化大屏，支持千万级数据点渲染。",
        "skills": ["JavaScript", "TypeScript", "React", "Vue.js", "Webpack", "Node.js"],
        "vars": {
            "project": ["SaaS管理后台", "大数据可视化", "混合App", "企业官网"]
        }
    },
    {
        "role": "Golang工程师",
        "desc_template": "熟悉Go语言特性，{years}年云原生开发经验。由于Kubernetes二次开发经验。",
        "exp_template": "- 使用Go重写了部分{service}服务，内存占用降低60%。\n- 参与K8s Operator开发，实现中间件自动化运维。\n- 构建高性能网关，支持动态路由和熔断限流。",
        "skills": ["Go", "gRPC", "Kubernetes", "Docker", "Etcd", "Prometheus"],
        "vars": {
            "service": ["消息推送", "海量日志处理", "实时计算", "CDN调度"]
        }
    },
    {
        "role": "数据科学家",
        "desc_template": "统计学硕士背景，{years}年机器学习落地经验。擅长NLP/推荐算法。",
        "exp_template": "- 负责{algo}模型的训练与部署，CTR提升15%。\n- 构建用户画像体系，实现精准营销。\n- 利用大模型技术优化智能客服系统。",
        "skills": ["Python", "PyTorch", "TensorFlow", "Pandas", "Scikit-learn", "Hadoop"],
        "vars": {
            "algo": ["推荐排序", "文本分类", "销量预测", "风控反欺诈"]
        }
    },
    {
        "role": "DevOps工程师",
        "desc_template": "{years}年运维开发经验，致力于提升研发效能。精通CI/CD流水线搭建。",
        "exp_template": "- 基于Jenkins/GitLab打造自动化CICD平台，发布效率提升3倍。\n- 负责生产环境的稳定性保障，SLA达到99.99%。\n- 实施{cloud}云资源管理与成本优化。",
        "skills": ["Linux", "Shell", "Python", "Jenkins", "Ansible", "Terraform", "AWS"],
        "vars": {
            "cloud": ["AWS", "阿里云", "腾讯云", "Azure"]
        }
    },
    {
        "role": "Android开发工程师",
        "desc_template": "{years}年Android原生开发经验，熟悉Kotlin。有大型App架构经验。",
        "exp_template": "- 负责App核心功能迭代，DAU突破百万。\n- 深度优化内存泄漏和卡顿问题，Crash率低于0.01%。\n- 探索Flutter跨平台技术在{scene}场景的落地。",
        "skills": ["Java", "Kotlin", "Android SDK", "Flutter", "Jetpack", "Performance"],
        "vars": {
            "scene": ["活动页", "个人中心", "列表展示", "详情页"]
        }
    },
    {
        "role": "测试开发工程师",
        "desc_template": "具备开发能力的QA，{years}年自动化测试经验。擅长性能压测。",
        "exp_template": "- 搭建自动化测试框架，回归测试时间缩短80%。\n- 负责核心接口的性能压测，发现并协助解决多个并发死锁问题。\n- 推广{method}测试理念，提升提测质量。",
        "skills": ["Python", "Java", "Selenium", "JMeter", "TestNG", "Pytest"],
        "vars": {
            "method": ["左移", "持续集成", "精准", "全链路"]
        }
    }
]

# 合并所有角色池
all_roles = general_roles + tech_roles

def generate_random_resume():
    # 随机选择身份
    role_info = random.choice(all_roles)
    surname = random.choice(surnames)
    given_name = random.choice(given_names)
    full_name = f"{surname}{given_name}"
    
    # 随机生成变量
    years = random.randint(2, 12)
    vars_dict = {k: random.choice(v) for k, v in role_info["vars"].items()}
    vars_dict["years"] = years
    
    # 构建内容
    desc = role_info["desc_template"].format(**vars_dict)
    exp = role_info["exp_template"].format(**vars_dict)
    # 随机取3-5个技能
    skills_count = min(5, len(role_info["skills"]))
    if skills_count > 0:
        skills = ", ".join(random.sample(role_info["skills"], k=skills_count))
    else:
        skills = "暂无详细技能"
    
    phone = f"13{random.randint(0, 9)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # 邮箱生成
    email_user = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(random.randint(6, 12))])
    email_suffix = random.choice(["gmail.com", "outlook.com", "yahoo.com", "163.com", "qq.com"])
    email = f"{email_user}@{email_suffix}"
    
    # 教育经历
    univs = ["某理工大学", "某综合性大学", "某师范大学", "某财经大学", "电子科技大学", "北京邮电大学", "浙江大学", "清华大学"]
    degree = random.choice(["本科", "硕士"])
    grad_year = 2026 - years - 1 
    
    content = f"""姓名：{full_name}
电话：{phone}
邮箱：{email}
求职意向：{role_info['role']}

个人简介：
{desc}

教育背景：
{grad_year-4} - {grad_year} | {random.choice(univs)} | 相关专业 | {degree}

工作经历：
{2020 + (years//2)} - 至今 | 某知名企业 | {role_info['role']}
{exp}

{2016 + (years//2)} - {2020 + (years//2)} | 某初创公司 | 专员
- 协助团队完成项目目标。
- 参与内部流程优化。

技能清单：
- {skills}
- 具备良好的沟通协调能力
"""
    # 增加 UUID 保证文件名绝对唯一，方便累加
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{role_info['role']}_{full_name}_{unique_id}.txt"
    return filename, content

# 可配置生成数量
BATCH_SIZE = 100

print(f"开始生成 {BATCH_SIZE} 份简历 (混合行业)...")
for i in range(BATCH_SIZE):
    fname, fcontent = generate_random_resume()
    path = os.path.join(output_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fcontent)
    if (i+1) % 20 == 0:
        print(f"已生成 {i+1} 份...")

print(f"本批次 {BATCH_SIZE} 份简历生成完毕！")
