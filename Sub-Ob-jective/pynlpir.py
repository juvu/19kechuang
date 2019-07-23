# 有授权问题，见下
# https://blog.csdn.net/weixin_39885687/article/details/81082005
import pynlpir
pynlpir.open()
s = '因为我比较懒,所以我就只是修改了这句话,代码还是原博客的'
segments = pynlpir.segment(s)
print(str(segments))

# for segment in segments:
#     print(segment[0], '\t', segment[1])

pynlpir.close()
