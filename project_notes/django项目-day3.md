# django项目-day3

## 修改apt-get源文件

源文件所在目录：`/et/apt/`

把sources.list 复制进去

> Ps:如果不能下载docker的情况下，使用



## 三码（IP）合一

1. ubuntu下 ifconfig 查看的ip地址

2. 创建storage容器的时候指定的ip

   ```shell
   890-=docker run -dti --network=host --name storage -e TRACKER_SERVER=ip:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
   ```

3. fastdfs客户端配置文件的ip

   ```shell
   #meiduo_mall/utils/fastdfs/client.conf  
   tracker_server=运行tracker服务的机器ip:22122
   
   ```

## 虚拟机的网络连接方式

1. 桥接
2. NAT    DHCP的租约63天（DHCP分配的ip，是咱们的IP的有效期，过了这个时间段重新分配）
3. 仅主机模式

## 知识点遗漏处：
1. python manage.py shell 相当于运行Django的启动项目，及加载里面的配置文件
2. 富文本编辑器在咱们的前端使用更加多元，后端也是引用的咱们的前端。
3. python的脚本只是帮助咱们去触发程序的执行，而不用去关心咱们在那里设置的定时时间段(crontab 定时任务)
4. 启动定时任务会自动触发咱们的 脚本命令等