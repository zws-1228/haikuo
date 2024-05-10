import json
import requests
from datetime import datetime
import time
import os
 
def download_image(url, file_path):
response = requests.get(url) # 发送GET请求获取响应对象
with open(file_path, 'wb') as f: # 以二进制写入模式打开文件
f.write(response.content) # 将响应内容写入文件
 
def main():
now = datetime.now() # 获取当前日期时间
date = now.date() # 获取当前日期
folder = str(date) # 文件夹名称为日期字符串
if not os.path.exists(folder): # 如果文件夹不存在，则创建文件夹
os.makedirs(folder)
# 读取以前创建的图片名 JSON 文件并去除重复项
failename = 'img_name.json'
if os.path.exists(failename):
with open(failename, 'r') as f:
image_names = json.load(f)
image_names = list(set(image_names))
else:
image_names = []
fileurl='img_url.json'
if os.path.exists(fileurl):
with open(fileurl, 'r') as f:
fileurls = json.load(f)
fileurls = list(set(fileurls))
else:
fileurls = []
downloaded_names = [] # 新下载的图片名列表
i = 20
while i > 0:
time.sleep(1)
url = 'https://www.dmoe.cc/random.php?return=json'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
'Referer': 'https://www.dmoe.cc',
}
turl = requests.get(url,headers=headers).json()
url = turl['imgurl']
filename = url.split("/")[-1]
if filename in image_names:
continue
image_names.append(filename)
downloaded_names.append('https://cdn.jsdelivr.net/gh/用户名/仓库名/'+folder+'/'+filename) # 将新下载的图片名添加到列表中
fileurls.append('https://cdn.jsdelivr.net/gh/用户名/仓库名/'+folder+'/'+filename) # 将新下载的图片名添加到列表中
file_path = os.path.join(folder, filename)
download_image(url, file_path)
i -= 1
# 将本次下载的图片名列表与之前的图片名列表进行合并，并写回到 JSON 文件中
image_names = list(set(image_names)) # 去除重复项
with open(failename, 'w') as f:
json.dump(image_names, f)
with open(fileurl, 'w') as f:
json.dump(fileurls, f)
 
# 将新下载的图片名 imgname_filename = '${folder}/img_name.json'列表写入到指定的 JSON 文件中
imgname_filename = os.path.join(folder, 'img_name.json')
with open(imgname_filename, 'w') as f:
json.dump(downloaded_names, f)
# 创建一个 Markdown 文件，并写入一些内容
md_filename = 'README.md'
md_path = os.path.join(folder, md_filename)
with open(md_path, 'w') as f:
f.write('# Downloaded Images\n\n')
for name in downloaded_names:
f.write(f'![]({name})\n')
f.write(f'```\n')
f.write(f'{name}\n')
f.write(f'```\n')
 
 
if __name__ == '__main__':
main()
 
 
