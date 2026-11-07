# 鲜期管家

面向家庭与宿舍的食品、药品库存与期限管理微信小程序。本仓库目前完成项目框架，业务板块尚未实现。

依据《系统概要设计说明书》V1.3（2026-10-28）搭建：原生微信小程序（WXML / WXSS / JavaScript）+ Python 3.11 及以上 + Flask 3.1 + SQLite。按单使用者、单份库存设计，不设账号或微信登录。

## 当前范围

- 服务端：应用工厂、配置加载、统一 JSON 响应与异常处理、健康检查、统一时钟、公共校验、数据库连接与事务。
- 数据库：九张表、外键、索引、去重约束及结构版本。初始化只建空表，不生成样例库存、风险参数或计算结果。
- 模块边界：食品、药品、风险、提醒、计划与统计五个包，以及 32 个业务接口占位。合法请求返回 HTTP 501 / `NOT_IMPLEMENTED`。
- 小程序：四个底部入口、12 个页面入口、食品/药品切换、公共组件、请求封装、接口服务与连接检查。业务页显示“开发中”，不提供业务表单和算法。
- 工程支持：启动脚本、测试、前端静态检查、依赖清单与协作说明。

具体库存操作、有效期计算、评分、提醒生成、计划安排、统计以及样例数据均留给下一阶段。

## 启动服务

在项目根目录运行。Windows 推荐 PowerShell；下列命令不要求激活虚拟环境。

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m flask --app app init-db
.\bin\start.bat
```

完成依赖安装和数据库初始化后，后续直接运行 `bin\start.bat` 即可。服务默认监听 `http://127.0.0.1:5000`，终端按 Ctrl+C 停止。

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
```

健康检查返回 `ok: true`、计算日期、实际时间、数据库版本，以及 `business_modules_implemented: false`。它检查基础设施，不表示业务功能已经完成。

Linux / macOS：使用 `python3 -m venv .venv`，后续 Python 路径改为 `.venv/bin/python`，启动使用 `sh bin/start.sh`。

## 打开小程序

1. 在微信开发者工具中导入**仓库根目录**；`project.config.json` 已将小程序目录设为 `miniprogram/`。
2. `touristappid` 只用于本机框架查看。真机预览使用自己有权限的 AppID，通过工具本地项目设置配置，不在仓库写入凭据。
3. 本地 HTTP 调试在开发者工具“本地设置”中按需关闭合法域名校验。仓库默认保持域名校验开启，该调试方式不作为发布配置。
4. 确认服务已启动，打开“首页 → 我的设置 → 检查连接”。
5. 真机访问时按 [部署说明](docs/deployment.md) 配置电脑局域网 IP 与监听地址；手机上的 `127.0.0.1` 不是电脑。

小程序无 npm 依赖，不需要“构建 npm”。当前仅进行了代码和引用的静态检查；微信开发者工具编译、真实 AppID 预览和真机验收仍需在对应环境完成。

## 检查代码

需 Python 开发依赖及 Node.js 18 或以上。

```powershell
.\.venv\Scripts\python.exe -m pytest
node --test tests/client.test.cjs
node bin/check-miniprogram.cjs
.\.venv\Scripts\python.exe bin/smoke.py
```

也可在允许运行 PowerShell 脚本的环境使用 `bin/check.ps1` 执行前三项检查。Python 单元测试使用独立临时数据库。最后一项需要已初始化的运行数据库，只读取数据，在随机本地端口启动临时服务并自动停止。

## 目录

```text
app_server.py             本地服务启动入口
app/
  routes/                 HTTP 接口、统一刷新编排预留入口
  services/
    foodstock/            食品库存与生命周期
    medicinestock/        药品库存与生命周期
    riskeval/             风险评估
    remindercenter/       提醒中心
    planstats/            七日计划与统计
  commonbase/             连接、事务、时钟、校验、常量、响应及建表 SQL
config/                   默认配置与本机配置示例
db/                       运行数据库及备份位置，不提交数据文件
logs/                     日志预留目录；当前输出至控制台
miniprogram/
  pages/                  四个底部入口及业务页面占位
  components/             页头、模块占位、加载/错误状态
  services/               与后端对应的接口函数
  utils/                  请求与页面导航
  config/                 服务地址及超时
bin/                      启动、检查脚本
tests/                    公共框架与客户端基础设施测试
docs/                     接口、架构、部署和后续开发约定
```

## 接着开发

- [架构与分工](docs/architecture.md)：模块职责、事务和派生刷新约定。
- [接口说明](docs/api.md)：统一协议、全部接口及占位语义。
- [部署说明](docs/deployment.md)：配置、局域网联调及手工备份恢复。
- [测试记录](docs/verification.md)：设计依据、检查结果和待验证项目。

