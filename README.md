# 空洞骑士&amp;丝之歌存档文件解析

使用 Python3 编写

算法借鉴于 https://github.com/bloodorca/hollow

## 使用说明

```bash
# 安装依赖
pip install -r requirements

# 解压存档文件（user1.dat 是你的存档文件），执行后会生成一个解压后的 json 文件
python hollow_user_data.py -D user1.dat > 1.json

# 压缩成存档文件，压缩后会生成一个名为 1.json.dat 的存档文件
python hollow_user_data.py -E 1.json
# 重命名
mv 1.json.dat user1.dat
```
