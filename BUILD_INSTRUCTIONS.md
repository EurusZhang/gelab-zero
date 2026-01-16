# 如何为打包的 EXE 添加版本号和图标

本文档说明如何为 Gelab Zero 项目的可执行文件添加版本信息和自定义图标。

## 📋 已完成的配置

### 1. 版本信息文件 (version_info.txt)

已创建 `version_info.txt` 文件，包含以下信息：
- **文件版本**: 1.0.0.0
- **产品版本**: 1.0.0.0
- **公司名称**: Gelab Zero Team
- **文件描述**: Gelab Zero Task Runner - AI Agent for Mobile Automation
- **版权信息**: Copyright (c) 2024-2026 Gelab Zero Team
- **产品名称**: Gelab Zero Task Runner

### 2. PyInstaller 配置文件 (gelab_zero.spec)

已更新 `gelab_zero.spec` 文件，添加了：
```python
icon='app_icon.ico',  # 图标文件
version='version_info.txt',  # 版本信息文件
```

## 🎨 创建应用图标

### 方法一：使用在线工具（推荐）

1. 访问以下任一网站：
   - https://www.icoconverter.com/
   - https://convertio.co/zh/png-ico/
   - https://www.aconvert.com/cn/icon/png-to-ico/

2. 准备一张 PNG 或 JPG 图片（建议尺寸：256x256 或 512x512 像素）

3. 上传图片并转换为 ICO 格式

4. 下载生成的 ICO 文件，重命名为 `app_icon.ico`

5. 将 `app_icon.ico` 放在项目根目录（与 `gelab_zero.spec` 同级）

### 方法二：使用 Python 工具

如果你有 PNG 图片，可以使用 Python 转换：

```bash
pip install pillow
```

然后运行以下 Python 代码：

```python
from PIL import Image

# 打开 PNG 图片
img = Image.open('your_image.png')

# 调整大小（可选）
img = img.resize((256, 256), Image.Resampling.LANCZOS)

# 保存为 ICO 格式
img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
```

### 方法三：使用 ImageMagick

如果安装了 ImageMagick：

```bash
magick convert your_image.png -define icon:auto-resize=256,128,64,32,16 app_icon.ico
```

## 🔧 修改版本信息

如需修改版本号或其他信息，编辑 `version_info.txt` 文件：

```python
# 修改文件版本和产品版本
filevers=(1, 0, 0, 0),  # 格式：(主版本, 次版本, 修订版本, 构建版本)
prodvers=(1, 0, 0, 0),

# 修改字符串信息
StringStruct(u'FileVersion', u'1.0.0.0'),
StringStruct(u'ProductVersion', u'1.0.0.0'),
StringStruct(u'CompanyName', u'你的公司名称'),
StringStruct(u'FileDescription', u'你的应用描述'),
StringStruct(u'LegalCopyright', u'版权信息'),
```

## 📦 打包应用程序

完成上述配置后，使用以下命令打包：

```bash
# 使用 spec 文件打包
pyinstaller gelab_zero.spec

# 或者清理后重新打包
pyinstaller --clean gelab_zero.spec
```

生成的 EXE 文件将位于 `dist` 目录中，文件名为 `GelabZeroTaskRunner_v1.0.0.exe`。

### 关于文件名中的版本号

当前配置中，EXE 文件名包含版本号（`GelabZeroTaskRunner_v1.0.0.exe`）。如果需要修改：

1. **修改文件名中的版本号**：编辑 `gelab_zero.spec` 文件中的 `name` 参数
   ```python
   name='GelabZeroTaskRunner_v1.0.0',  # 修改这里的版本号
   ```

2. **移除文件名中的版本号**：如果不想在文件名中显示版本号
   ```python
   name='GelabZeroTaskRunner',  # 只保留应用名称
   ```

注意：文件名中的版本号和 `version_info.txt` 中的版本信息是独立的：
- **文件名版本号**：显示在文件名中，需要手动修改 spec 文件
- **元数据版本号**：嵌入在 EXE 文件属性中，通过 `version_info.txt` 配置

## ✅ 验证结果

打包完成后，验证版本信息和图标：

1. **查看图标**：
   - 在文件资源管理器中查看 EXE 文件，应该显示自定义图标

2. **查看版本信息**：
   - 右键点击 EXE 文件
   - 选择"属性"
   - 切换到"详细信息"选项卡
   - 查看文件版本、产品版本、公司名称等信息

## 📝 注意事项

1. **图标文件位置**：`app_icon.ico` 必须放在项目根目录，与 `gelab_zero.spec` 同级

2. **图标格式**：必须是 `.ico` 格式，不能是 PNG 或 JPG

3. **图标尺寸**：建议包含多个尺寸（16x16, 32x32, 64x64, 128x128, 256x256）以适应不同显示场景

4. **版本号格式**：版本号必须是四个数字的元组，如 `(1, 0, 0, 0)`

5. **重新打包**：修改图标或版本信息后，需要重新运行 PyInstaller 打包命令

6. **清理构建**：如果遇到问题，使用 `--clean` 参数清理之前的构建文件

## 🔍 常见问题

### Q: 图标没有显示？
A: 
- 确认 `app_icon.ico` 文件存在且路径正确
- 尝试使用 `--clean` 参数重新打包
- 检查 ICO 文件是否有效（可以用图片查看器打开测试）

### Q: 版本信息没有显示？
A: 
- 确认 `version_info.txt` 文件存在
- 检查文件编码是否为 UTF-8
- 确保版本号格式正确

### Q: 如何更新版本号？
A: 
- 编辑 `version_info.txt` 文件
- 修改 `filevers` 和 `prodvers` 的值
- 同时更新 `FileVersion` 和 `ProductVersion` 字符串
- 重新打包应用程序

## 📚 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [Windows 版本信息结构](https://docs.microsoft.com/en-us/windows/win32/menurc/versioninfo-resource)
- [ICO 文件格式说明](https://en.wikipedia.org/wiki/ICO_(file_format))
