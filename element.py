from spellchecker import SpellChecker
import re
import copy

def auto_archive(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        obj = args[0] if args else None
        if obj == HtmlElement.root: HtmlElement.archive()
        return result
    return wrapper

class HtmlElement:
    existing_ids = set()
    states = []
    state_point = -1
    root = None
    basic_tags = ('html', 'head', 'title', 'body')
    spell = SpellChecker()

    def __init__(self, tag, content='', element_id=None, children=None):
        self.tag = tag
        self.children = children if children is not None else []
        self.is_basic_tag = self.tag in HtmlElement.basic_tags
        self.id = self.__validate_id(element_id)
        self.set_content(content)
    
    def __bool__(self):
        return self.tag != ""
    
    def __validate_id(self, element_id):
        if not element_id:
            if self.is_basic_tag: element_id = self.tag
            else: raise ValueError(f"Element '{self.tag}' must have a unique id.")
        if element_id in HtmlElement.existing_ids:
            raise ValueError(f"Element '{self.tag}' must have a unique id. Duplicate id: '{element_id}'")
        HtmlElement.existing_ids.add(element_id)
        return element_id

    def add_child(self, child, index=None):
        if index is None:
            self.children.append(child)
        else:
            self.children.insert(index, child)

    def set_content(self, content):
        if content == '': 
            self.content = ''
            return
        if self.id == "title1":
            1+1
        # 删除content中和空格相连或头尾的标点符号
        # 删除数字和字符的组合
        # 删除 xx.com
        sub_list = [r'[^\w\d\s]+', r'[^a-zA-Z ]+', r'\w+\.com']
        cleaned_content = ' ' + content + ' '
        for sub in sub_list:
            re_str = r'\s' + sub + r'|' + sub + r'\s'
            cleaned_content = re.sub(re_str, ' ', cleaned_content)
        misspelled = HtmlElement.spell.unknown(cleaned_content.strip().split())
        if not misspelled:
            self.spell_correct = True
        else:
            self.spell_correct = False
        self.content = content

    def update_id(self, new_id):
        if new_id in HtmlElement.existing_ids:
            raise ValueError(f"Element '{self.tag}' must have a unique id. Duplicate id: '{new_id}'")
        HtmlElement.existing_ids.remove(self.id)
        HtmlElement.existing_ids.add(new_id)
        self.id = new_id
    
    def __update_element(self, element_id, new_id=None, new_content=None):
        element = self.find_by_id(element_id)
        if not element:
            raise ValueError(f"Element with id '{element_id}' not found.")
        if new_id:
            element.update_id(new_id)
        if new_content:
            element.set_content(new_content)
    
    
    def find_by_id(self, element_id):
        if self.id == element_id:
            return self
        for child in self.children:
            found = child.find_by_id(element_id)
            if found:
                return found
        return None
    
    def tab_render(self, indent=0, step=2, check=False):
        # 创建缩进字符串
        indent_str = ' ' * indent
        # 开始标签
        html = f"{indent_str}<{self.tag} id=\"{self.id}\">" if not self.is_basic_tag else f"{indent_str}<{self.tag}>"
        # 内容
        if self.content:
            html += f"{self.content}" if self.spell_correct or not check else f"\033[91m{self.content}\033[0m"
        # 子标签
        if self.children: html += "\n"
        for child in self.children:
            html += child.tab_render(indent + step, step, check)
        # 结束标签
        html += f"{indent_str}</{self.tag}>\n" if self.children else f"</{self.tag}>\n"
        return html
    

    def tree_render(self, prefix='', check=False):
        # 构建当前元素的描述
        description = f"{self.tag}#{self.id}" if not self.is_basic_tag else self.tag
        # 打印当前元素
        tree_str = f"{prefix}{description}\n" 
        # if self.id == "title1":
        #     1+1
        if prefix:
            if prefix.strip()[-3] == '└': 
                prefix = prefix[:-4] + "    "
            else:
                prefix = prefix[:-4] + "│   "
        
        # 如果有内容，打印内容
        symbol_len = 0
        symbol_len = len(self.children) + 1 if self.content else len(self.children)
        symbol = ["├── "] * (symbol_len-1) + ["└── "] if symbol_len else []
        if self.content:
            tree_str += f"{prefix}{symbol[0]}{self.content}\n" if self.spell_correct or not check else f"\033[91m{prefix}{symbol[0]}{self.content}\033[0m\n"
            del symbol[0]
        # 处理子元素
        for i, child in enumerate(self.children):
            # 判断是否是最后一个子元素
            is_last = (i == len(self.children) - 1)
            # 更新前缀
            # if symbol[0][0] == '└': prefix = prefix[:-4] + "    "
            child_prefix = f"{prefix}{symbol[0]}"
            del symbol[0]
            # 递归打印子元素
            tree_str += child.tree_render(child_prefix,check)
        return tree_str

    @auto_archive
    def insert(self, new_tag, new_id, element_id, *content):
        content = ' '.join(map(str, content))
        new_element = HtmlElement(new_tag, content, element_id=new_id)
        for i, child in enumerate(self.children):
            if child.id == element_id:
                self.children.insert(i, new_element)
                return True
            if child.insert(element_id, new_element):
                return True
        return False
    
    @auto_archive
    def append(self, new_tag, new_id, element_id, *content):
        content = ' '.join(map(str, content))
        new_element = HtmlElement(new_tag, content, element_id = new_id)
        element = self.find_by_id(element_id)
        if element: element.add_child(new_element)
        else: raise ValueError(f"Element with id '{element_id}' not found.")
    
    @auto_archive
    def edit_id(self, old_id, new_id):
        self.__update_element(old_id, new_id=new_id)
    
    @auto_archive
    def edit_text(self, old_id, *content):
        content = ' '.join(map(str, content))
        self.__update_element(old_id, new_content=content)
    
    @auto_archive
    def delete(self, del_id):
        if del_id == "html": raise Exception("无法删除html节点")
        if self.id == del_id:
            return self
        found = None
        for i, child in enumerate(self.children):
            found = child.delete(del_id)
            if found: break
        if found: del self.children[i]
        return None
    
    def print_indent(self, step=2):
        print(self.tab_render(step=step))
    
    def print_tree(self):
        print(self.tree_render())
    
    def spell_check(self):
        print(self.tab_render(check=True))
    
    @staticmethod
    def read(path):
        HtmlElement.reset()
        from bs4 import BeautifulSoup

        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(html_content, 'html.parser')

        def create_html_element(soup_element):
            """递归地将 BeautifulSoup 元素转换为 HtmlElement 对象"""
            if not soup_element.name:
                return None
            
            # 创建 HtmlElement 对象
            element = HtmlElement(
                tag=soup_element.name,
                content=soup_element.string.strip() if soup_element.string else '',
                element_id=soup_element.get('id', None)
            )
            
            # 递归处理子元素
            for child in soup_element.children:
                child_element = create_html_element(child)
                if child_element:
                    element.children.append(child_element)
            
            return element

        # 从 soup 对象中构造 HtmlElement 对象
        HtmlElement.root = create_html_element(next(soup.children))
        HtmlElement.archive()
        return HtmlElement.root

    @staticmethod
    def save(path, root):
        HtmlElement.save_reset()
        with open(path, "w", encoding='utf-8') as f:
            f.write(root.tab_render())
    
    @staticmethod
    def init():
        HtmlElement.reset()
        root = HtmlElement(tag='html')
        body = HtmlElement(tag='body')
        head = HtmlElement(tag='head')
        title = HtmlElement(tag='title')
        root.children.append(head)
        root.children.append(body)
        head.children.append(title)

        HtmlElement.root = root
        HtmlElement.archive()
        return root
    
    @staticmethod
    def undo():
        if HtmlElement.state_point <= 0: 
            raise Exception("已回到初始状态")
        HtmlElement.state_point -= 1
        HtmlElement.root = HtmlElement.states[HtmlElement.state_point]
        return HtmlElement.root

    @staticmethod
    def archive():
        HtmlElement.state_point += 1
        if HtmlElement.state_point < len(HtmlElement.states):
            del HtmlElement.states[HtmlElement.state_point:]
        HtmlElement.states.append(copy.deepcopy(HtmlElement.root))

    @staticmethod
    def redo():
        if HtmlElement.state_point >= len(HtmlElement.states) - 1: 
            raise Exception("已为最新状态")
        HtmlElement.state_point += 1
        HtmlElement.root = HtmlElement.states[HtmlElement.state_point]
        return HtmlElement.root

    @staticmethod
    def reset():
        HtmlElement.states = []
        HtmlElement.state_point = -1
        HtmlElement.existing_ids = set()
        HtmlElement.root = None

    @staticmethod
    def save_reset():
        HtmlElement.states = []
        HtmlElement.state_point = -1
        HtmlElement.archive()