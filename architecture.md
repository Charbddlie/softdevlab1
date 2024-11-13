## 架构设计
### 1. 模块设计

![模块设计](architecture.svg)


#### 1.1 `auto_archive` 装饰器
- 装饰器 `auto_archive` 依赖于 `HtmlElement.archive()` 方法.它将 `HtmlElement` 类中的一些方法（如 `insert, append, edit_id, edit_text, delete` 等）进行装饰,以在这些方法执行后自动保存状态.
`auto_archive` 检查传入的对象是否为 `HtmlElement.root`,然后调用 `archive` 方法保存当前状态.

> 使得 HTML 元素在进行插入、追加、编辑或删除等操作时,能够自动保存状态,为后续的撤销和重做功能提供状态历史支持.

#### 1.2 `HtmlElement` 类
`HtmlElement` 是核心类,负责 HTML 元素的创建、操作和存档.该类依赖多个内部和外部模块实现不同功能

##### 1.2.1 外部库依赖
- `SpellChecker`：用于拼写检查,检测内容中的拼写错误,帮助用户识别并纠正文本中的错误.
- `re`：用于正则表达式操作,以清理内容中的无效字符或 URL,帮助 `set_content` 方法实现内容清理.
- `copy`：用于**深拷贝**当前的 `HtmlElement` 结构,以在 `archive()` 中存储当前状态,实现撤销/重做功能.
- `BeautifulSoup`：用于 `read` 方法读取并解析 `HTML` 文件,将文件内容转换成 `HtmlElement` 对象树.

### 2. `undo_redo` 的实现

`undo`和`redo`配合`archive`后,可以实现自动状态存档和回滚功能.`archive` 在元素变更时被 `auto_archive` 调用，将当前状态存储到 `states` 中；`undo` 和 `redo` 操作会修改 `state_point`，在历史记录中向前或向后移动。

### 3. 不同形式输出的实现

在 `HtmlElement` 类中,提供了 `tab_render`和`tree_render`两种输出方式,可以根据需求进行输出.

---

## 运行说明

### 1. 运行环境
- python 3.6+
- windows/linux/macOS

### 2. 如何运行

#### 2.1 解压缩
- 将压缩包解压到任意目录
#### 2.2 进入文件目录
```bash
cd folder_name
```
#### 2.3 安装依赖
```bash
pip install -r requirements.txt
```
#### 2.4 运行
```bash
python session.py
```