# django项目-day1

## 每日反馈



## 项目学习重点

1. 业务流程

   1. 注册功能

      接收参数

2. 技术点

   1. session，cookie
   2. jwt
   3. 页面静态化



## 美多项目目录结构

```python
meiduo					 		#项目目录
|--front_end_pc		 	#前端文件目录
|--meiduo_mall			#django后端项目目录
|--|--docs					#文档目录
|--|--logs			 		#日志目录
|--|--scripts				#脚本文件目录  [shell脚本、python脚本]
|--|--manage.py			#自动化脚本	
|--|--meiduo_mall		#项目管理目录(django项目同名目录)
|--|--|--apps			  #应用目录
|--|--|--|--users   #用户应用
|--|--|--|--goods   #商品应用
|--|--|--libs			  #第三方库目录
|--|--|--settings		#配置文件目录	 [prod.py,dev.py]
|--|--|--utils			#自定义库目录
```



## git仓库

分支： master  dev  tag1.1





## 搭建项目

### 创建一个仓库

克隆仓库  `git clone gitee.com/meiduo.git`

`meiduo/frot_end_pc`  前端

`meiduo/meiduo_mall` 后端

### 创建后端工程

```shell
mkvirtualenv meiduo
pip install django==1.11.11
pip install djangorestframework
pip pymysql
pip django_redis  (django_redis , redis)


# 创建工程
cd /meiduo/
django-admin startproject meiduo_mall
```

### 修改导包路径

```python
#/meiduo/meiduo_mall/settings/dev.py
import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
应用名.apps.应用名Config
AUTH_CLASS = "users.UserModel"
```

## 注册业务分析

#### 图片验证码

说明：获取验证码图片

请求方式： GET

url地址：image_codes/<image_code_id>/

```python
class ImageCodes():
  def get(self, request, image_code_id):
    # 生成图片资源和图片文本
    # 把图片文本保存到服务器端  image_code_id：图片文本
    # 返回图片资源
    
```

请求参数: 无

响应数据： 图片资源

`<img src="接口地址"/>`

#### 判断用户名是否注册

#### 判断手机号是否注册

#### 获取短信验证码

#### 注册操作

