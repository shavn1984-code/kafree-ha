咖啡自由 (Kafree) — Home Assistant 自定义集成
https://img.shields.io/badge/HACS-Custom-41BDF5.svg
https://img.shields.io/badge/Home%2520Assistant-2023.0+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg

将「咖啡自由」微信小程序接入 Home Assistant，实现咖啡机的本地化监控与控制。

📖 目录
功能特性

支持机型

传感器列表

控制按钮

安装方法

获取 Token

Lovelace UI 配置

实体命名对照表

常见问题

更新日志

免责声明

✨ 功能特性
✅ 支持 21 个传感器数据采集

✅ 支持 4 个控制按钮（开机/关机/锁定/解锁）

✅ 实时监控咖啡机状态

✅ 部件异常告警（水箱/豆仓/水温等）

✅ 清洁分与清洗进度追踪

✅ 饮品制作数据统计

✅ 可定制的 Lovelace UI

📟 支持机型
机型	支持状态
SF1-MAX	✅ 完全支持
SF1-PRO	✅ 完全支持
⚠️ 目前仅支持中国地区使用

📊 传感器列表
状态类
传感器	说明
sensor.ka_pei_zi_you_ka_pei_ji_zhuang_tai	咖啡机状态（在线/休眠/离线）
sensor.ka_pei_zi_you_she_bei_zhuang_tai	设备状态（待完善）
sensor.ka_pei_zi_you_tong_suo	童锁状态（开启/关闭）
sensor.ka_pei_zi_you_she_bei_xiao_xi	设备消息通知
清洗类
传感器	说明
sensor.ka_pei_zi_you_dang_qian_qing_ji_fen	当前清洁分（0-100）
sensor.ka_pei_zi_you_chong_pao_qi_qing_xi	冲泡器清洗进度
sensor.ka_pei_zi_you_chu_gou_qing_xi	除垢清洗进度
sensor.ka_pei_zi_you_nai_mo_qi_qing_xi	奶沫器清洗进度
用量统计类
传感器	说明
sensor.ka_pei_zi_you_yi_zhi_zuo_bei_shu	已制作杯数
sensor.ka_pei_zi_you_lei_ji_ka_pei_dou	累计咖啡豆用量
sensor.ka_pei_zi_you_lei_ji_shui_liang	累计水量
sensor.ka_pei_zi_you_lei_ji_niu_nai	累计牛奶用量
sensor.ka_pei_zi_you_bi_ka_pei_dian_jie_sheng	比咖啡店节省金额
饮品分类
传感器	说明
sensor.ka_pei_zi_you_hei_ka	黑咖制作杯数
sensor.ka_pei_zi_you_nai_ka	奶咖制作杯数
sensor.ka_pei_zi_you_qi_ta_yin_liao	其他饮料制作杯数
部件状态
传感器	说明
sensor.ka_pei_zi_you_shui_xiang	水箱状态（正常/异常）
sensor.ka_pei_zi_you_shui_wen	水温状态（正常/异常）
sensor.ka_pei_zi_you_xu_shui_pan	蓄水盘状态（正常/异常）
sensor.ka_pei_zi_you_nai_pao_qi	奶泡器状态（正常/异常）
sensor.ka_pei_zi_you_dou_cang	豆仓状态（正常/异常）
🎮 控制按钮
按钮实体	功能
button.ka_pei_zi_you_kai_ji	开机
button.ka_pei_zi_you_guan_ji	关机
button.ka_pei_zi_you_kai_suo	锁定童锁
button.ka_pei_zi_you_guan_suo	解锁童锁
📦 安装方法
方法一：HACS 安装（推荐）
打开 HACS → 集成 → 右上角菜单 → 自定义存储库

添加此仓库地址，类别选择「集成」

搜索 Kafree 并安装

重启 Home Assistant

方法二：手动安装
bash
# 进入 Home Assistant 配置目录
cd /config

# 克隆仓库到 custom_components
git clone https://github.com/yourusername/kafree.git custom_components/kafree
或手动下载：

下载此仓库的 最新 Release

解压并将 kafree 文件夹复制到 custom_components 目录

重启 Home Assistant

配置集成
进入 配置 → 设备与服务 → 添加集成

搜索并选择 咖啡自由

填入以下信息：

参数	说明
API 域名	kafree-app-cn.coffee-iot.com（一般不变）
Token	通过抓包获取（见下文）
点击提交完成配置

🔑 获取 Token
使用 Reqable 抓包
⚠️ 如需长期使用，建议定期更新 Token

打开 Reqable → 开启 镜像模式

安装证书 → 开启系统代理（快捷键 Ctrl+P）

设置过滤规则：coffee-iot.com

打开 PC 微信 → 进入 咖啡自由小程序

在请求头中找到 Authorization: Bearer "xxxxxx"

复制引号内的 xxxxxx 即为 Token

使用 Charles / Fiddler
同样通过抓包工具过滤 coffee-iot.com 域名，在请求头中获取 Authorization 字段。

🎨 Lovelace UI 配置
前置要求
在 HACS 中安装以下 Lovelace 组件：

组件	用途
picture-elements	咖啡机状态可视化面板（内置）
mushroom-template-card	设备消息显示
bar-card	清洗进度条
mini-graph-card	制作杯数趋势图
背景图片
将背景图片放在 /config/www/lovelace/image/ 目录下，命名为 kafree.png

💡 或在可视化面板中上传至媒体库，然后替换 media_content_id

UI 配置代码
<details> <summary>点击展开完整配置代码</summary>
yaml
type: vertical-stack
cards:
  # ==================== 咖啡机状态可视化面板 ====================
  - type: picture-elements
    elements:
      # ---- 隐藏的状态徽章 ----
      - type: conditional
        conditions: []
        elements:
          - entity: sensor.ka_pei_zi_you_yi_zhi_zuo_bei_shu
            type: state-badge
            style:
              top: 25%
              left: 55%
              font-size: 0.8em
              color: rgba(0,0,0,0)
          - entity: sensor.ka_pei_zi_you_dang_qian_qing_ji_fen
            type: state-badge
            style:
              top: 25%
              left: 22%
              font-size: 0.8em
              color: rgba(0,0,0,0)
          - entity: sensor.ka_pei_zi_you_ka_pei_ji_zhuang_tai
            type: state-badge
            style:
              top: 14%
              left: 25%
              font-size: 0.8em
              color: rgba(0,0,0,0)

      # ---- 电源按钮（在线 → 关机） ----
      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_ka_pei_ji_zhuang_tai
            state: 在线
        elements:
          - type: icon
            style:
              left: 45%
              top: 10%
              color: orange
            icon: fas:power-off
            tap_action:
              action: perform-action
              perform_action: button.press
              target:
                entity_id: button.ka_pei_zi_you_guan_ji
              data: {}

      - entity: sensor.ka_pei_zi_you_she_bei_zhuang_tai
        type: state-badge
        style:
          top: 14%
          left: 35%
          font-size: 0.8em
          color: rgba(0,0,0,0)

      # ---- 电源按钮（休眠 → 开机） ----
      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_ka_pei_ji_zhuang_tai
            state: 休眠
        elements:
          - type: icon
            style:
              left: 45%
              top: 10%
            icon: fas:power-off
            tap_action:
              action: perform-action
              perform_action: button.press
              target:
                entity_id: button.ka_pei_zi_you_kai_ji
              data: {}

      # ---- 部件异常告警 ----
      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_shui_wen
            state: 异常
        elements:
          - type: state-badge
            style:
              left: 40%
              top: 40%
              name: 水温
            entity: sensor.ka_pei_zi_you_shui_wen

      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_xu_shui_pan
            state: 异常
        elements:
          - type: state-badge
            style:
              left: 35%
              top: 80%
              name: 蓄水盘
            entity: sensor.ka_pei_zi_you_xu_shui_pan

      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_nai_pao_qi
            state: 异常
        elements:
          - type: state-badge
            style:
              left: 20%
              top: 65%
              name: 奶泡器
            entity: sensor.ka_pei_zi_you_nai_pao_qi

      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_shui_xiang
            state: 异常
        elements:
          - type: state-badge
            style:
              left: 77%
              top: 35%
              name: 水箱
            entity: sensor.ka_pei_zi_you_shui_xiang

      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_dou_cang
            state: 异常
        elements:
          - type: state-badge
            style:
              left: 77%
              top: 10%
              name: 豆仓
            entity: sensor.ka_pei_zi_you_dou_cang

      # ---- 童锁按钮 ----
      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_tong_suo
            state: 开启
        elements:
          - type: icon
            style:
              left: 52%
              top: 10%
              color: orange
            icon: fas:lock
            tap_action:
              action: perform-action
              perform_action: button.press
              target:
                entity_id: button.ka_pei_zi_you_kai_suo
              data: {}

      - type: conditional
        conditions:
          - condition: state
            entity: sensor.ka_pei_zi_you_tong_suo
            state: 关闭
        elements:
          - type: icon
            style:
              left: 52%
              top: 10%
            icon: fas:lock
            tap_action:
              action: perform-action
              perform_action: button.press
              target:
                entity_id: button.ka_pei_zi_you_guan_suo
              data: {}

    image:
      media_content_id: media-source://image_upload/your_image_id
      media_content_type: image/png
    card_mod:
      style: |
        ha-card {
          box-shadow: none !important;
          background: none !important;
          border: none !important;
        }

  # ==================== 设备消息 ====================
  - type: custom:mushroom-template-card
    secondary: "{{ states('sensor.ka_pei_zi_you_she_bei_xiao_xi') }}"
    icon: mdi:message-alert
    features_position: bottom
    entity: sensor.ka_pei_zi_you_she_bei_xiao_xi
    primary: 设备消息

  # ==================== 节省金额 ====================
  - type: entity
    entity: sensor.ka_pei_zi_you_bi_ka_pei_dian_jie_sheng
    name: 比咖啡店节省

  # ==================== 累计用量 ====================
  - show_name: true
    show_icon: true
    show_state: true
    type: glance
    entities:
      - entity: sensor.ka_pei_zi_you_lei_ji_ka_pei_dou
        name: 累计咖啡豆
      - entity: sensor.ka_pei_zi_you_lei_ji_niu_nai
        name: 累计牛奶
      - entity: sensor.ka_pei_zi_you_lei_ji_shui_liang
        name: 累计水量

  # ==================== 清洁分仪表盘 ====================
  - entity: sensor.ka_pei_zi_you_dang_qian_qing_ji_fen
    max: 100
    min: 0
    severity:
      green: 60
      yellow: 75
      red: 90
    type: gauge
    name: 当前清洁分

  # ==================== 清洗进度条 ====================
  - entities:
      - icon: mdi:cup
        entity: sensor.ka_pei_zi_you_nai_mo_qi_qing_xi
        name: 奶沫器清洗
      - icon: mdi:barrel
        name: 冲泡器清洗
        entity: sensor.ka_pei_zi_you_chong_pao_qi_qing_xi
      - entity: sensor.ka_pei_zi_you_chu_gou_qing_xi
        name: 除垢清洗
        icon: mdi:water-pump
    show_header_toggle: false
    type: custom:bar-card
    severity:
      - color: Red
        to: "25"
        from: "0"
      - color: Orange
        from: "26"
        to: "50"
      - color: Green
        from: "51"
        to: "100"
    direction: right
    columns: "1"
    icon: mdi:broom

  # ==================== 制作杯数趋势图 ====================
  - entities:
      - entity: sensor.ka_pei_zi_you_yi_zhi_zuo_bei_shu
        name: 累计制作
      - entity: sensor.ka_pei_zi_you_hei_ka
        name: 黑咖
      - entity: sensor.ka_pei_zi_you_nai_ka
        name: 奶咖
      - entity: sensor.ka_pei_zi_you_qi_ta_yin_liao
        name: 其他饮料
        show_indicator: false
        show_legend: false
        show_line: false
        show_points: false
        show_state: false
        y_axis: secondary
    show:
      labels: true
    type: custom:mini-graph-card
</details>
📋 实体命名对照表
中文名称	Entity ID
咖啡机状态	sensor.ka_pei_zi_you_ka_pei_ji_zhuang_tai
设备状态	sensor.ka_pei_zi_you_she_bei_zhuang_tai
童锁	sensor.ka_pei_zi_you_tong_suo
当前清洁分	sensor.ka_pei_zi_you_dang_qian_qing_ji_fen
已制作杯数	sensor.ka_pei_zi_you_yi_zhi_zuo_bei_shu
累计咖啡豆	sensor.ka_pei_zi_you_lei_ji_ka_pei_dou
累计水量	sensor.ka_pei_zi_you_lei_ji_shui_liang
累计牛奶	sensor.ka_pei_zi_you_lei_ji_niu_nai
比咖啡店节省	sensor.ka_pei_zi_you_bi_ka_pei_dian_jie_sheng
黑咖	sensor.ka_pei_zi_you_hei_ka
奶咖	sensor.ka_pei_zi_you_nai_ka
其他饮料	sensor.ka_pei_zi_you_qi_ta_yin_liao
水箱	sensor.ka_pei_zi_you_shui_xiang
水温	sensor.ka_pei_zi_you_shui_wen
蓄水盘	sensor.ka_pei_zi_you_xu_shui_pan
奶泡器	sensor.ka_pei_zi_you_nai_pao_qi
豆仓	sensor.ka_pei_zi_you_dou_cang
设备消息	sensor.ka_pei_zi_you_she_bei_xiao_xi
奶沫器清洗	sensor.ka_pei_zi_you_nai_mo_qi_qing_xi
冲泡器清洗	sensor.ka_pei_zi_you_chong_pao_qi_qing_xi
除垢清洗	sensor.ka_pei_zi_you_chu_gou_qing_xi
开机	button.ka_pei_zi_you_kai_ji
关机	button.ka_pei_zi_you_guan_ji
锁定	button.ka_pei_zi_you_kai_suo
解锁	button.ka_pei_zi_you_guan_suo
❓ 常见问题
Q: Token 过期了怎么办？
A: Token 有效期不定，过期后需要重新抓包获取新的 Token，然后在集成中更新配置。

Q: 设备状态显示"待完善"？
A: 该字段目前数据源不完整，后续版本会完善。

Q: 控制按钮点击无反应？
A: 检查咖啡机是否在线，以及 Token 是否有效。

Q: 支持远程控制吗？
A: 只要 Home Assistant 能访问互联网即可远程控制。

Q: 数据更新频率是多少？
A: 集成会定期轮询 API 获取最新数据，具体间隔可配置。

📝 更新日志
v1.0.0
🎉 初始版本发布

✅ 支持 21 个传感器

✅ 支持 4 个控制按钮

✅ 完整 Lovelace UI 配置

⚖️ 免责声明
本集成仅供学习和个人使用

使用本集成造成的设备损坏或数据丢失，作者概不负责

本集成与「咖啡自由」官方无关

请遵守咖啡机厂商的使用规范

🤝 贡献
欢迎提交 Issue 和 Pull Request！

📄 许可证
MIT © 2026

