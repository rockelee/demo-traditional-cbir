**********************************************
python�汾��2.7.8��32λ��
	    ��Ҫ�Լ���װctypes��,wxpython��

**********************************************
����˵��1105��
1. �ӿڸĶ�
       ��   unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile, unsigned char *pRansacPath);
       ��Ϊ unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile��;

2. ��"ft"�ļ������е�log�ļ�������¼�˷Ƿ�·��֮�⣬����¼�˲�����Ҫ���ͼƬ��
   ��ȡ������ʱ�����ᱣ����ЩͼƬ�����������������ͼƬ������Ҫ������ȡ��

   
**********************************************
����˵����
1. �ӿڸĶ����£�
   1�� ɾ���� float *FeatureExtract(unsigned char *pImageFile);
           �� unsigned char *FeatureMatch(unsigned char *pBuildId, float *pFeature);

   2�� ��    unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile��;
       ��Ϊ  unsigned char *FeatureExtractMatch(unsigned char *pBuildId, unsigned char *pImageFile, unsigned char *pRansacPath);

   3�� ��   void FeatureRelease(int *pFeature);
       ��Ϊ void FeatureRelease(float *pFeature);
   

2. ����Ķ���ɾ���˷ֲ�����ȡ������ƥ��ͼ��İ�ť 


**********************************************
����˵����
1��ѡ���뱾
2������������
3��ѡ���ƥ�������� 
4��ѡ����ͼ��·�������ڲ��Ҳ���ʾƥ�䵽��ͼ��·������ѡ��'image',��image�µ�ͼƬ�洢��ʽ����ǰһ�������ܸĶ���

5����ѡ��1������ͼ��·����Ȼ���ͷ�1��ƥ����
   ��ѡ��ͳ�Ʋ���·����


6�������Ҫ��ȡ�����⣬���ȼ����뱾��Ȼ��ѡ��������·����·����ȷ�����������'image\420100\01\01'����
   Ȼ��ѡ����ȡ�����⡱���������в�������Ƿ�·���������»��ߵģ���ͼƬ������

**********************************************

