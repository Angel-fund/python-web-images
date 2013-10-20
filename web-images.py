#coding:utf-8
"""图片上传后端处理"""
__modify__ = '2goo.info'
__email__ ='nmgkjdxjsj@gmail.com'
VERSION = "Graphics v0.1 build 2011-03-27"

import os,Image,ImageFile,uuid

class Graphics:    
    def __init__(self,uploadedfile,targetpath):
        '''初始化参数'''
        self.uploadedfile=uploadedfile
        self.targetpath = targetpath

    def check_folder(self):
        '''检查目标文件夹是否存在，不存在则创建之'''
        if not os.path.isdir(self.targetpath):
            os.mkdir(self.targetpath)
        return self.targetpath

    def pic_info(self, img):
        '''获取照片的尺寸和确定图片横竖版'''
        w, h = img.size
        if  w>h:
            return w, h, 0  #横版照片
        else:
            return w, h, 1  #竖版照片

    def comp_ratio(self, x, y):
        '''计算比例.'''
        x = float(x)
        y = float(y)
        return float(x/y)

    def pic_cut(self, image, p_w, p_h):
        '''根据设定的尺寸，对指定照片进行像素调整
        图形不会变形 如果指定尺寸比例和原图比例不
        相等时，最大范围剪切'''
        #获取指定照片的规格，一般是1024,768       
        img = image   
        w, h, isVertical = self.pic_info(img)
        #判断照片横竖，为竖版的话对调w,h
        if isVertical:
            p_w, p_h = p_h, p_w

        #如果照片调整比例合适，直接输出
        if self.comp_ratio(p_h, p_w) == self.comp_ratio(h, w):
            target = img.resize((int(p_w), int(p_h)),Image.ANTIALIAS)#hack:高保真必备！                            
            # ANTIALIAS: a high-quality downsampling filter
            # BILINEAR: linear interpolation in a 2x2 environment
            # BICUBIC: cubic spline interpolation in a 4x4 environment
            return target

        #比例不合适就需要对照片进行计算，保证输出照片的正中位置
        #算法灵感来源于ColorStrom
        if self.comp_ratio(p_h, p_w) > self.comp_ratio(h, w):
            #偏高照片的处理
            #以高为基准先调整照片大小
            #根据新高按比例设置新宽
            p_w_n = p_h * self.comp_ratio(w,h) 
            temp_img = img.resize((int(p_w_n), int(p_h)),Image.ANTIALIAS)

            #获取中间选定大小区域
            c = (p_w_n - p_w)/2 #边条大小
            box = (c, 0, c+p_w, p_h) #选定容器
            #换成crop需要的int形参数
            box = tuple(map(int, box)) 
            target = temp_img.crop(box)

            return target

        else:
            #偏宽的照片
            #以宽为基准先调整照片大小
            p_h_n = p_w * self.comp_ratio(h, w)  # 根据新宽按比例设置新高
            temp_img = img.resize((int(p_w), int(p_h_n)),Image.ANTIALIAS)

            #获取新图像
            c = (p_h_n - p_h)/2
            box = (0, c, p_w, c+p_h)
            box = tuple(map(int, box))
            target = temp_img.crop(box)

            return target
        
    def pic_zoom_w(self, image, p_w):
        '''根据设定的宽度，对指定照片进行像素缩放 图形不会变形
        图形比例不变 高度根据指定的宽度等比列放大缩小'''
        #获取指定照片的规格，一般是1024,768       
        img = image   
        w, h, isVertical = self.pic_info(img)
        p_h=p_w * self.comp_ratio(h, w)
        temp_img = img.resize((int(p_w), int(p_h)),Image.ANTIALIAS)
        
        box = (0, 0, p_w, p_h)
        box = tuple(map(int, box))
        target = temp_img.crop(box)

        return target
    
    def pic_zoom_h(self, image, p_h):
        '''根据设定的高度，对指定照片进行像素缩放 图形不会变形
        图形比例不变 宽度根据指定的高度等比列放大缩小'''
        #获取指定照片的规格，一般是1024,768       
        img = image   
        w, h, isVertical = self.pic_info(img)
        p_w=p_h * self.comp_ratio(w, h)
        temp_img = img.resize((int(p_w), int(p_h)),Image.ANTIALIAS)
        
        box = (0, 0, p_w, p_h)
        box = tuple(map(int, box))
        target = temp_img.crop(box)

        return target   

    #外部调用方法
    def run_cut(self,quality=80,*args):
        '''运行调整照片尺寸进程 接纳规格列表，每个规格为一个tuple'''
        parser = ImageFile.Parser()  
        for chunk in self.uploadedfile.chunks():  
            parser.feed(chunk)  
        img = parser.close()
        list=[]
        uuid_str=str(uuid.uuid1())
        try:
            for std in args:
                w, h = std[0], std[1]  #获取照片的规格               
                filename=uuid_str+"-"+str(w)+"-"+str(h)+'.jpg'      
                opfile = os.path.join(self.check_folder(),filename)
                
                tempimg = self.pic_cut(img,int(w), int(h))
                tempimg.save(opfile, 'jpeg',quality=quality)
                list.append(filename)
            return list
        except:
            pass       
    
    def run_zoom_w(self,*args):
        '''运行图形缩放 接纳图形宽度tuple列表，每个宽度为一个整数'''
        parser = ImageFile.Parser()  
        for chunk in self.uploadedfile.chunks():  
            parser.feed(chunk)  
        img = parser.close()
        list=[]
        uuid_str=str(uuid.uuid1())
        w, h, isVertical = self.pic_info(img)
        try:
            for woh in args:#获取照片的宽度              
                th=int(float(woh) * self.comp_ratio(h,w))
                #生成唯一的图片名字     
                filename=uuid_str+"-"+str(woh)+"-"+str(th)+'.jpg'
                #图片路径+图片名字     
                opfile = os.path.join(self.check_folder(),filename)           
                tempimg=self.pic_zoom_w(img,int(woh))                
                tempimg.save(opfile, 'jpeg',quality=80)
                list.append(filename)
            return list
        except:
            pass
        
    def run_zoom_h(self,*args):
        '''运行图形缩放 接纳图形高度tuple列表，每个高度为一个整数'''
        parser = ImageFile.Parser()  
        for chunk in self.uploadedfile.chunks():  
            parser.feed(chunk)  
        img = parser.close()
        list=[]
        uuid_str=str(uuid.uuid1())
        w, h, isVertical = self.pic_info(img)
        try:
            for woh in args:#获取照片的高度                
                tw=int(float(woh) * self.comp_ratio(w,h))
                filename=uuid_str+"-"+str(tw)+"-"+str(woh)+'.jpg'   
                opfile = os.path.join(self.check_folder(),filename)                    
                tempimg=self.pic_zoom_h(img,int(woh))
                tempimg.save(opfile, 'jpeg',quality=80)
                list.append(filename)
            return list
        except:
            pass
        
    def run_thumbnail(self,*args):
        '''传统的生成缩略图 接纳规格列表，每个规格为一个tuple'''
        parser = ImageFile.Parser()  
        for chunk in self.uploadedfile.chunks():  
            parser.feed(chunk)  
        img = parser.close()
        list=[]
        uuid_str=str(uuid.uuid1())
        try:
            for std in args:
                #获取照片的规格            
                w, h = std[0], std[1]
                #生成唯一的图片名字         
                filename=uuid_str+"-"+str(w)+"-"+str(h)+'.jpg'
                #图片路径+图片名字
                opfile = os.path.join(self.check_folder(),filename)
                tempimg=img.copy()
                tempimg.thumbnail((int(w), int(h)),Image.ANTIALIAS)
                tempimg.save(opfile, 'jpeg',quality=80)
                list.append(filename)
            return list
        except:
            pass