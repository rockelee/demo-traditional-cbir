**********************************************
python版本：2.7.8（32位）
	    需要自己安装ctypes包,wxpython包

**********************************************
更新说明1105：
1. 接口改动
       将   unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile, unsigned char *pRansacPath);
       改为 unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile）;

2. 在"ft"文件夹中中的log文件，除记录了非法路径之外，还记录了不符合要求的图片，
   提取特征库时，不会保存这些图片的特征；如果更改了图片，则需要重新提取。

   
**********************************************
更新说明：
1. 接口改动如下：
   1） 删除了 float *FeatureExtract(unsigned char *pImageFile);
           和 unsigned char *FeatureMatch(unsigned char *pBuildId, float *pFeature);

   2） 将    unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile）;
       改为  unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile, unsigned char *pRansacPath);

   3） 将   void FeatureRelease(int *pFeature);
       改为 void FeatureRelease(float *pFeature);
   

2. 界面改动，删除了分步骤提取特征和匹配图像的按钮 


**********************************************
操作说明：
1）选择码本
2）加载特征库
3）选择待匹配特征库 
4）选择结果图像路径（用于查找并显示匹配到的图像，路径必须选择'image',且image下的图片存储方式和以前一样，不能改动）

5）“选择1”测试图像路径，然后“释放1”匹配结果
   “选择”统计测试路径，


6）如果需要提取特征库，请先加载码本，然后选择样本集路径（路径精确到建筑物，比如'image\420100\01\01'，）
   然后选择“提取特征库”，特征库中不会包含非法路径（即有下划线的）的图片的特征

**********************************************

