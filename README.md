# 咖啡自由 (Kafree) — Home Assistant 自定义集成



## 功能

将「咖啡自由」微信小程序接入 Home Assistant。

## 支持

目前只支持中国地区使用，兼容机型SF1-MAX、SF1-PRO。

## 传感器 (21 个)

咖啡机状态、设备状态（待完善）、童锁、冲泡器清洗、除垢清洗、奶沫器清洗、当前清洁分、已制作杯数、累计咖啡豆、累计水量、累计牛奶、比咖啡店节省、黑咖、奶咖、其他饮料、水箱、水温、蓄水盘、奶泡器、豆仓、设备消息

## 控制按钮 (4 个)

开机、关机、锁定、解锁

## 安装

1. 将 `custom_components/kafree` 复制到 HA 的 `custom_components` 目录
2. 重启 HA
3. 配置 → 集成 → 添加「咖啡自由」
4. 输入API 域名: kafree-app-cn.coffee-iot.com（域名一般不变，可长期使用），Token（通过Reqable抓包获取）


## 抓包 (Reqable)

1. 打开 Reqable → 镜像模式
2. 安装证书 → 开启系统代理 (Ctrl+P)
3. 过滤栏输入: coffee-iot.com
4. 打开 PC 微信 → 咖啡自由小程序
5. 在请求头中找到 Authorization: Bearer "xxxxxx"(引号内xxxxxx为真实token)

## lovelace UI界面

1. 需要用到于以下lovelace组件（custom:bar-card，custom:mini-graph-card，gauge，glance，entity，custom:mushroom-template-card，picture-elements），可在hacs中搜索安装
2. 背景图片在/lovelace/image目录下kafree.png
   <img width="440" height="440" alt="kafree" src="https://github.com/user-attachments/assets/53a625b8-4edc-487a-9417-70fe07c73b4f" />
4. 代码文件:
   cards:
  - type: picture-elements
    elements:
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
      media_content_id: media-source://image_upload/eb57d6809c9dbdd648697176e99fd90c
      media_content_type: image/png
      metadata:
        title: 1779686660960_Dz6X45Di3n.png
        thumbnail: /api/image/serve/eb57d6809c9dbdd648697176e99fd90c/256x256
        media_class: image
        navigateIds:
          - {}
          - media_content_type: app
            media_content_id: media-source://image_upload
    card_mod:
      style: |
        ha-card {
          box-shadow: none !important;
          background: none !important;
          border: none !important;
        }
  - type: custom:mushroom-template-card
    secondary: "{{states('sensor.ka_pei_zi_you_she_bei_xiao_xi')}}"
    icon: mdi:message-alert
    features_position: bottom
    entity: sensor.ka_pei_zi_you_she_bei_xiao_xi
    primary: 设备消息
  - type: entity
    entity: sensor.ka_pei_zi_you_bi_ka_pei_dian_jie_sheng
    name: 比咖啡店节省
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
  - entity: sensor.ka_pei_zi_you_dang_qian_qing_ji_fen
    max: 100
    min: 0
    severity:
      green: 60
      yellow: 75
      red: 90
    theme: default
    type: gauge
    name: 当前清洁分
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
    view_layout:
      column: 3
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
type: vertical-stack

   
