##使用模块前 需安装PIL库


python-web-images
=================

python web
此模块主要是为web开发 在图片处理上做了封装
使用该模块，你仅仅需要传入上传地址（绝对地址）和HttpRequest.FILES，初始化一下里面的Graphics类，然后使用类的方法，指定需要的尺寸tuple即可返回上传图片的名字。
 
Graphics类里有几个方法 是外部调用的，分别是run_cut，run_zoom_w，run_zoom_h和run_thumbnail。
 
run_cut:是根据你提供的尺寸，对原图片进行剪切，原图片比例和你指定的尺寸比例不相等时，程序会以原图中心为准放大缩小剪切成你需要的尺寸，图片不会拉伸。需要传入一个或多个尺寸tuple，如(150,100),(300,200),(50,50)
 
run_zoom_w:是根据你提供的宽度，等比列缩放。方法需要传入一个或多个宽度tuple，如 150,100,200,300
run_zoom_h:是根据你提供的高度，等比列缩放。方法需要传入一个或多个高度tuple，如 150,100,200,300
 
run_thumbnail:是传统的缩略图方法，需要传入一个或多个尺寸tuple，如(150,100),(300,200),(50,50)
 
这三个方法，能把原图处理成多种尺寸规格，也就是说能同时处理并上传成 多张不同尺寸的图片。图片处理的时候，全部采用Image.ANTIALIAS抗锯齿的过滤属性，保存的图片质量暂时定在100，这些都是为了保证剪切图片的时候，最大降低失真度，这样出来的图片体积就稍微大些了。图片的名字组合方式：uuid+"_"+w+"_"+h.jpg，如：ae5c011e- 5e98-11e0-96e6-001a6bd081a2-600-400.jpg

validate_code.py
================
此模块提供了生成图像验证码的功能
