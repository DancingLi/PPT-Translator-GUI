# GUI可视化界面与一键安装包规格说明书

## 1. 项目背景与目标

### 1.1 背景
PPT Translator 是一个功能强大的 PowerPoint 翻译工具，但目前仅支持命令行界面（CLI），对非技术用户不够友好。

### 1.2 目标
- **可视化操作界面（GUI）**: 创建直观、美观的图形界面，让普通用户无需了解命令行即可使用
- **一键安装包**: 将 Python 环境、依赖库和应用程序打包为单一安装程序，用户下载后双击即可安装使用

---

## 2. 技术方案选型

### 2.1 GUI 框架选择

**推荐方案: CustomTkinter**

| 特性 | CustomTkinter |
|------|---------------|
| 美观度 | 现代化外观，支持深色/浅色主题 |
| 学习曲线 | 低，类似标准 Tkinter |
| 打包兼容性 | 优秀，与 PyInstaller 配合良好 |
| 资源占用 | 低 |
| 跨平台 | Windows/macOS/Linux |

**备选方案: PyQt5/PySide6**
- 功能更丰富，但打包体积大（>100MB）
- 学习曲线较陡

### 2.2 打包工具选择

**推荐方案: PyInstaller + Inno Setup**

| 工具 | 用途 |
|------|------|
| PyInstaller | 将 Python 脚本打包为可执行文件（.exe） |
| Inno Setup | 创建 Windows 安装程序（.exe 安装包） |

**打包流程:**
1. PyInstaller 将 Python 代码 + 依赖 + Python 解释器打包为单个 exe
2. Inno Setup 创建安装程序，包含 exe、图标、卸载程序

---

## 3. GUI 界面设计规格

### 3.1 整体布局

```
+----------------------------------------------------------+
|  PPT Translator                                    [设置] |
+----------------------------------------------------------+
|                                                          |
|  +----------------------------------------------------+  |
|  |  ① 选择文件                                        |  |
|  |                                                    |  |
|  |  [选择PPT文件...]  或  [选择文件夹...]              |  |
|  |                                                    |  |
|  |  已选择: example.pptx                              |  |
|  +----------------------------------------------------+  |
|                                                          |
|  +----------------------------------------------------+  |
|  |  ② 翻译设置                                        |  |
|  |                                                    |  |
|  |  翻译提供商: [DeepSeek ▼]                          |  |
|  |                                                    |  |
|  |  源语言: [中文(简体) ▼]     目标语言: [英语 ▼]       |  |
|  |                                                    |  |
|  |  API密钥: [************************] [验证]          |  |
|  +----------------------------------------------------+  |
|                                                          |
|  +----------------------------------------------------+  |
|  |  ③ 高级选项 (可选)                                  |  |
|  |                                                    |  |
|  |  [ ] 保留中间文件                                   |  |
|  |                                                    |  |
|  |  最大线程数: [4 ▼]    分块大小: [1000] 字符        |  |
|  |                                                    |  |
|  |  输出目录: [与输入相同 ▼]  [浏览...]                |  |
|  +----------------------------------------------------+  |
|                                                          |
|          [           开始翻译           ]                  |
|                                                          |
+----------------------------------------------------------+
|  进度: [████████████░░░░░░░░] 60%  |  正在翻译第 3/5 页...   |
+----------------------------------------------------------+
|  状态: 就绪                                              |
+----------------------------------------------------------+
```

### 3.2 界面主题规格

**颜色方案（深色模式）:**
- 背景色: `#1a1a2e`
- 卡片背景: `#16213e`
- 主色调: `#0f3460`
- 强调色: `#e94560`
- 文字颜色: `#eaeaea`
- 次要文字: `#a0a0a0`
- 边框颜色: `#2a2a4a`
- 成功色: `#4caf50`
- 警告色: `#ff9800`
- 错误色: `#f44336`

**字体规格:**
- 主字体: "Segoe UI" (Windows), "SF Pro Display" (macOS)
- 标题字号: 18-24px
- 正文字号: 12-14px
- 小字/标签: 10-11px

### 3.3 交互设计规格

**文件选择:**
- 支持单个 .pptx 文件选择
- 支持批量选择（多选文件）
- 支持选择整个文件夹（递归处理）
- 拖放支持（高级功能）

**实时验证:**
- API 密钥格式验证（长度、字符检查）
- 文件格式验证（.pptx 扩展名）
- 语言对验证（某些提供商不支持的语言组合）
- "验证"按钮：测试 API 连接

**进度反馈:**
- 总体进度条（百分比）
- 当前步骤文字说明
- 文件计数（第 X/Y 个文件）
- 预计剩余时间（可选）

**结果展示:**
- 成功：显示输出文件路径，提供"打开文件夹"按钮
- 失败：显示错误详情，提供"重试"按钮
- 批量结果：表格展示每个文件的状态

---

## 4. 一键安装包规格

### 4.1 安装包结构

```
PPT-Translator-Setup.exe
├── setup.exe                    # 安装程序
├── PPTTranslator/               # 安装目录
│   ├── PPTTranslator.exe        # 主程序
│   ├── _internal/              # PyInstaller 依赖
│   ├── config/                 # 配置文件
│   └── translations/           # 界面翻译文件
├── vcredist/                   # Visual C++ 运行时
├── icon.ico                    # 程序图标
├── uninstall.exe               # 卸载程序
└── README.txt                  # 安装说明
```

### 4.2 安装流程规格

**安装向导步骤:**

1. **欢迎页面**
   - 应用名称、版本、图标
   - 简介文字
   - "下一步"按钮

2. **许可协议**
   - MIT 许可证全文
   - "我接受许可协议"复选框
   - "打印"按钮（可选）

3. **选择安装位置**
   - 默认：`C:\Program Files\PPTTranslator`
   - 浏览按钮
   - 磁盘空间检查

4. **准备安装**
   - 摘要：安装位置、所需空间
   - "安装"按钮

5. **安装进度**
   - 进度条
   - 当前操作文字
   - 取消按钮（带确认对话框）

6. **完成**
   - "安装完成"消息
   - "运行 PPT Translator"复选框（默认勾选）
   - "查看 README"复选框
   - "完成"按钮

### 4.3 卸载流程规格

**卸载方式:**
- 开始菜单："PPT Translator → 卸载"
- 控制面板：程序和功能
- 安装目录：`uninstall.exe`

**卸载步骤:**
1. 确认对话框："确定要卸载 PPT Translator 吗？"
2. 进度：删除文件、注册表项
3. 完成："已成功卸载"（可选：保留用户配置）

### 4.4 安装包技术规格

**构建工具链:**

| 工具 | 用途 | 版本 |
|------|------|------|
| PyInstaller | Python → 可执行文件 | 6.x |
| Inno Setup | 安装程序创建 | 6.2+ |
| UPX | 可执行文件压缩 | 4.x |

**PyInstaller 配置:**

```python
# build.py
PyInstaller.__main__.run([
    'main.py',
    '--name=PPTTranslator',
    '--onefile',              # 单文件模式
    '--windowed',             # 无控制台窗口（GUI 模式）
    '--icon=assets/icon.ico',
    '--add-data=config;config',
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--collect-all=customtkinter',
    '--upx-dir=upx',
    '--clean',
    '--noconfirm',
])
```

**Inno Setup 脚本:**

```pascal
; setup.iss
[Setup]
AppName=PPT Translator
AppVersion=1.0.0
AppPublisher=PPT Translator Team
DefaultDirName={autopf}\PPTTranslator
DefaultGroupName=PPT Translator
OutputDir=dist
OutputBaseFilename=PPT-Translator-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\PPTTranslator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\PPT Translator"; Filename: "{app}\PPTTranslator.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\卸载 PPT Translator"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PPT Translator"; Filename: "{app}\PPTTranslator.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Run]
Filename: "{app}\PPTTranslator.exe"; Description: "{cm:LaunchProgram,PPT Translator}"; Flags: nowait postinstall skipifsilent
```

### 4.5 安装包体积优化

**目标体积:** < 200MB（安装包）

**优化策略:**

1. **PyInstaller 优化**
   - 使用 `--exclude-module` 排除未使用的库
   - 使用 `--upx-dir` 压缩可执行文件
   - 使用 `--onefile` 减少文件碎片

2. **依赖精简**
   ```
   必须: python-pptx, customtkinter, Pillow, python-dotenv
   提供商: openai, anthropic, google-generativeai, etc.
   移除: 测试依赖、文档生成工具、开发工具
   ```

3. **资源压缩**
   - 图标使用 ICO 格式（多分辨率）
   - 界面图片使用 WebP 格式
   - 安装程序使用 LZMA2 压缩

---

## 5. 开发计划与任务分解

### 5.1 开发阶段

| 阶段 | 内容 | 预计工期 |
|------|------|---------|
| Phase 1 | GUI 设计与开发 | 5-7 天 |
| Phase 2 | 核心功能集成 | 3-4 天 |
| Phase 3 | 安装包构建 | 2-3 天 |
| Phase 4 | 测试与优化 | 2-3 天 |
| **总计** | | **12-17 天** |

### 5.2 技术栈总结

| 层级 | 技术 | 用途 |
|------|------|------|
| GUI 框架 | CustomTkinter | 跨平台现代化界面 |
| 图标/图片 | Pillow | 图像处理 |
| 配置存储 | JSON/YAML | 用户偏好设置 |
| 打包工具 | PyInstaller | Python → EXE |
| 安装程序 | Inno Setup | Windows 安装包 |

---

## 6. 风险与注意事项

### 6.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| PyInstaller 杀毒软件误报 | 高 | 使用 --onefile 模式，添加数字签名 |
| 安装包体积过大 | 中 | 精简依赖，使用 UPX 压缩 |
| 不同 Windows 版本兼容性 | 中 | 测试 Win7/10/11，静态链接 VC++ 运行时 |

### 6.2 用户体验注意事项

1. **首次启动引导** - 提供 API 密钥配置向导
2. **错误友好提示** - 网络错误、文件占用等情况给出明确提示
3. **进度可视化** - 长时间操作提供进度条和预计时间
4. **日志记录** - 保存操作日志便于问题排查

---

## 7. 附录

### 7.1 参考资源

- CustomTkinter 文档: https://github.com/TomSchimansky/CustomTkinter
- PyInstaller 文档: https://pyinstaller.org/
- Inno Setup 文档: https://jrsoftware.org/ishelp/
- Python-pptx 文档: https://python-pptx.readthedocs.io/

### 7.2 文件命名规范

```
项目根目录/
├── gui/
│   ├── __init__.py
│   ├── main_window.py          # 主窗口
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── file_selector.py    # 文件选择组件
│   │   ├── provider_selector.py # 提供商选择
│   │   ├── progress_bar.py     # 进度条
│   │   └── log_viewer.py       # 日志查看器
│   ├── dialogs/
│   │   ├── __init__.py
│   │   ├── settings_dialog.py  # 设置对话框
│   │   ├── api_key_dialog.py   # API密钥配置
│   │   └── about_dialog.py     # 关于对话框
│   └── utils/
│       ├── __init__.py
│       ├── config_manager.py   # 配置管理
│       └── theme_manager.py    # 主题管理
├── build/
│   ├── build.py                # PyInstaller 构建脚本
│   ├── setup.iss               # Inno Setup 脚本
│   └── assets/
│       ├── icon.ico            # 程序图标 (多分辨率)
│       ├── banner.bmp          # 安装程序横幅
│       └── splash.png          # 启动画面
└── dist/                       # 输出目录
```

### 7.3 版本规划

**V1.0.0** (MVP)
- 基础 GUI 界面
- 文件/文件夹选择
- 提供商配置
- 基础翻译功能
- Windows 安装包

**V1.1.0**
- 主题切换（深色/浅色）
- 多语言界面
- 批量处理优化
- 历史记录

**V1.2.0**
- 拖放支持
- 预览功能
- 自定义模板
- 自动更新
