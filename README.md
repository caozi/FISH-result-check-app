# 通过微信公众号平台实现的一个简单的病理结果的自助查询，通知系统,
##  为什么叫 FISH-result-check-app呢，我在我们科干FISH的活，一开始是想弄个通知患者FISH结果的这么一个服务，后来就逐渐推广到全科在测试
## 基于 Django，mysql，jquery，weui，wechatpy
###测试号二维码，用微信扫描
![二维码](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/-1.jpg)
### 关注完会根据关注事件，推送消息
![关注事件](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/0.jpg)
### 默认的菜单有登记，查询，登录。登记目前有会诊登记和FISH登记，查询提供查询报告查询功能，登录功能仅供科里面人员使用，用来给患者发送消息，更改报告状态
![菜单](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/1.jpg)
### 会诊登记页面，患者填写会诊号，在填写会诊号时会检测会诊号是否存在，再输入一遍会诊号后会再要求输入一遍，因为发现经常有输错的。
![会诊登记页面](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/2.jpg)
### 会诊登记成功
![会诊登记成功](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/6.jpg)
### 会诊登记成功后会发送消息给患者的微信
![发送消息给患者](https://github.com/caozi/FISH-result-check-app/blob/master/13.jpg)
### 登记完之后点击查询，会诊查询可以查询报告状态
![查询报告状态](https://github.com/caozi/FISH-result-check-app/blob/master/10.jpg)
### 登记完之后会阻止患者再次登记，因为发现有患者反复登记，很是头疼
![已登记后不能再次登记](https://github.com/caozi/FISH-result-check-app/blob/master/7.jpg)

### 下面是登录界面，点击登录
![登录](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/9.jpg)
### 如果没有授权，无法登录
![登录失败](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/12.jpg)
### 患者管理页面
![单个患者管理](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/2.jpg)
![单个患者管理](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/3.jpg)
![单个患者管理](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/4.jpg)
![单个患者管理](https://github.com/caozi/FISH-result-check-app/blob/master/screenshot/6.jpg)

### 2020/6/12 工作比较忙，时间不富裕，偷空改改，慢慢改进吧，今天下午有时间，赶紧把READEME好好写一下