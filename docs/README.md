## 設計文件

資料來源：

* miro https://miro.com/app/board/uXjVPNJTm9s=/
* draw.io https://app.diagrams.net/#G18-C-vW4yZpTPyehy3oFA7g2A1o_ksNpC

### 事件風暴討論成果

![](event_storming.png)

### 初版 OOA

![](OOA_v1.png)

### 細節版 OOA

![](OOA_v2.png)

### 特殊規則

* 遊戲設置時，依人數 `移除的卡片` 會在什麼時候用到？如何使用呢？
    - 當玩家A抽了牌堆中最後一張，並打出`王子`要求玩家B重抽一張牌，此時玩家B就會抽取`移除牌`
