# 565455-API接口文档

## 简介

565455API是由FANCC编写的可免费使用的API

FANCC使用这些API为前端项目提供服务

仓库结构（重要组成部分）

```
.
|____index.html
|____README.md
|____api
| |____title.py
| |____youdian.py
| |____bilidown.py
| |____lanzou.py
| |____node.py
| |____send.py（已废弃）
| |...
```

每一个`.py`文件代表一个API

服务托管在vercel服务器上，服务链接有

- `https://api.565455.xyz/[项目名]` （推荐）
- `https://565455.vercel.app/[项目名]` （中国大陆无法使用）

bug反馈：fancc@565455.xyz

## 调用说明

API接口不支持跨域访问，所以我们对调用结果进行了特殊处理，再返回内容前加入了`api_response=`，这样便可以使用`script`标签跨域调用，下方为示例

```javascript
let api_response;
function load_api(url, callback){
    setTimeout(()=>{
        let s = document.createElement("script");
        s.src = url;
        document.querySelector("body").appendChild(s);
        s.onload = ()=>{
            s.remove();
            callback(api_response);
        };
    });
}
load_api("https://api.565455.xyz/api/title?link=https://www.baidu.com/", (r)=>{console.log(r)});
```


## API接口

### title

- 用途：获取任意网页的标题
- 链接：https://api.565455.xyz/api/title
- 请求方式：`GET`
- 必要参数：
    - link：网页链接
- 示例：
    - 请求链接：`https://api.565455.xyz/api/title?link=https://www.baidu.com/`
    - 返回结果：
```
api_response={"code": 0, "msg": "ok", "title": "\u767e\u5ea6\u4e00\u4e0b\uff0c\u4f60\u5c31\u77e5\u9053"}
```

---

### youdian

- 用途：获取优点英语听力密码
- 使用例：<https://g.565455.xyz/youdian.html>
- 链接：https://api.565455.xyz/api/youdian
- 请求方式：`GET`
- 必要参数：
    - route：**处理过的**优点英语链接（链接预处理详情见上方使用例链接）
- 示例：
    - 请求链接：`https://api.565455.xyz/api/youdian?route=h.qr61.cn/obzgrD/qfcYoXX`
    - 返回结果：
```
api_response={"code": 0, "msg": "", "mima": "513278"}
```

---

### bilidown

- 用途：获取360p哔哩哔哩视频
- 使用例：<https://g.565455.xyz/bilidown.html>
- 链接：https://api.565455.xyz/api/bilidown
- 请求方式：`GET`
- 必要参数：
    - bv：视频bv号
    - p：视频p号，若视频不分p请填1，不可省略
- 示例：
    - 请求链接：`https://api.565455.xyz/api/bilidown?bv=BV1FW411k76N&p=5`
    - 返回结果：
```
api_response={"code": 0, "msg": "ok", "v_link": "https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/06/32/55573206/55573206-1-6.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1685282663&gen=playurlv2&os=akam&oi=919718885&trid=59f42e720a354606a1fdf75600627fdch&mid=0&platform=html5&upsig=d461704ceae4eb75169659a13fa7046f&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&hdnts=exp=1685282663~hmac=9fbfcac4f7ffb6e67cd5d58733be029bd7563c28c939b0696a90c5c504196a01&bvc=vod&nettype=0&bw=16833&logo=80000000"}
```

---

### lanzou

- 用途：获取蓝奏云分享文件的直链
- 链接：https://api.565455.xyz/api/lanzou
- 请求方式：`GET`
- 必要参数：
    - lz：蓝奏云的分享链接
- 示例：
    - 请求链接：`https://api.565455.xyz/api/lanzou?lz=https://fancc.lanzout.com/ishoG0shd33a`
    - 返回结果：
```
api_response={"code": 0, "msg": "", "link": "https://developer.lanzoug.com/file/?AmRSbAo7AjNUXQc/BjNTP1plBDwHHgVGAEkARVNMAS0F7VWFXqlS41KMULBQR1WzVKEBgwSyApgDgQTqVqUBuwIsUnUKMwIwVCQHNwY7Uz5aZQReBzEFYwA6ADdTPgEwBTVVMV4wUjdSMFA2UCJVMlR9ATkEaQI4AzcEN1YzATYCJFJ1CicCa1QwB2EGYFNhWi8EMQdsBSgANwA/UyABYgVmVWNeYVI0UmZQMlA3VTdUPgE2BD4CNQM1BDRWPQFlAjtSPApuAmBUNAdmBmRTalo3BGIHaQVkAD8AY1M4AS4FdVVmXmVSIFJxUHVQYVUmVGcBYARmAjEDMgQxVjsBMwI6UjEKcQIiVGsHPAY3UzRaPQQwB24FPwAyADRTOAE2BTNVN146UihSKlAgUGJVOFR5ATkEagI2AzwEN1Y4ATQCO1IxCmICb1QkByQGIlMlWj0EMAduBT8ANgA2Uz8BNgU9VTBeNVIgUnFQb1B0VWlUOgEwBHUCMQM9BDpWJAE1AjFSKwplAmRUMw=="}
```

---

### node

- 用途：从nodefree.org获得最新的节点yaml文件，方便在clash中更新
- 链接：https://api.565455.xyz/api/node
- 请求方式：`GET`
- 必要参数：
    - 无
- 示例：
    - 请求链接：`https://api.565455.xyz/api/node`
    - 返回结果：
```
[.yaml文件]
```
