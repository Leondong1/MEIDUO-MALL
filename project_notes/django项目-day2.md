# Django项目-day2




## 常见错误解析：

1. Access-Control-Allow-Origin（CORS跨域请求）

   域：协议（HTTP/HTTPS）、域名、端口号 （即便两个域名指向同一个IP地址，也不是同源）

   前端与后端分处不同的域名，我们需要为后端添加跨域访问的支持

   解决方案：前端：jsonp跨域  后端： 跨域资源共享（CORS）发起 option 请求，浏览器询问我的域名是否能够访问

   咱们后端的接口，后端根据自己设定的白名单域名，来进行判断，如果能，浏览器则发送请求

   **注意**  咱们跨域请求中添加的白名单 含有咱们的 端口号 （有域的概念） 而 访问咱们后端的域名 则不需要端口号

2. celery 中异步处理导包的问题

   redis之间的版本出现不兼容的情况，咱们可以进入redis里面对具有版本的语句进行修改(譬如咱们里面  if redis.VERSION > (3, 2, 0):)  使其无法进入里面抛出异常

3. git中出现“non-fast-forward”errors

   根本原因是repository已经存在项目且不是你本人提交（我知道是大概率你提交的，但是git只认地址），你commit的项目和远程repo不一样.
   然而pull回来之后，你再push依旧会fail。 
   原因是他们是两个不同的项目，要把两个不同的项目合并，不能简单的git pull

   ```shell
   git pull origin master --allow-unrelated-histories
   git push origin master
   ```
4. 登陆后如何在前端观察是否登录成功：在console打印输出  如：vm.username;localStorage.token
5. 什么时候需要捕获异常，进行try except  ：涉及到 网络请求  或 get 在模型类中查询


## qq登录三种情况

1. 已经绑定过的qq
2. qq第一次登录在本站点没有账号,注册账号绑定qq
3. qq第一次登录在本站点有账号，直接和qq绑定