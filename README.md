# 咖啡自由 (Kafree) — Home Assistant 自定义集成



##功能

将「咖啡自由」微信小程序接入 Home Assistant。

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

##lovelace UI界面
1. 需要用到于以下lovelace组件（custom:bar-card，custom:mini-graph-card，gauge，glance，entity，custom:mushroom-template-card，picture-elements），可在hacs中搜索安装
2. 背景图片在image目录下kafree.png
3. 代码文件lovelace.txt