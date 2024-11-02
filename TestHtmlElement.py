import unittest
from element import HtmlElement

class TestHtmlElement(unittest.TestCase):

    # def setUp(self):
    #     # 初始化测试前重置HtmlElement
    #     HtmlElement.init()
    def test_create_basic_element(self):
        # 测试基本元素的创建
        root = HtmlElement(tag="html", element_id="html")
        self.assertEqual(root.tag, "html")
        self.assertEqual(root.id, "html")
        self.assertEqual(root.children, [])


    def test_add_child(self):
        # 测试添加子元素
        root = HtmlElement.init()
        div = HtmlElement(tag="div", element_id="div_id")
        root.add_child(div)
        self.assertIn(div, root.children)
    
    def test_find_by_id(self):
        # 测试通过 id 查找元素
        root = HtmlElement.init()
        div = HtmlElement(tag="div", element_id="div_id")
        root.add_child(div)
        self.assertEqual(root.find_by_id("div_id"), div)
        self.assertIsNone(root.find_by_id("nonexistent"))

    def test_set_content(self):
        # 测试设置内容，并验证拼写检查
        root = HtmlElement(tag="html", element_id="html")
        root.set_content("Hello, World!")
        self.assertEqual(root.content, "Hello, World!")
        self.assertTrue(root.spell_correct)

    def test_update_id(self):
        # 测试更新元素的 id
        root = HtmlElement(tag="html", element_id="html")
        new_id = "new_html"
        root.update_id(new_id)
        self.assertEqual(root.id, new_id)

    def test_insert_and_append(self):
        # 测试插入和追加子元素
        root = HtmlElement.init()
        root.append("div", "div_id", "html")
        self.assertEqual(root.find_by_id("div_id").id, "div_id")
        
        root.insert("meta", "meta1", "div_id", "charset=utf-8")
        self.assertEqual(root.find_by_id("meta1").content, "charset=utf-8")

    def test_edit_id_and_text(self):
        # 测试修改 id 和内容
        root = HtmlElement.init()
        root.append("div", "div_id", "html")
        root.append("p", "p_id", "div_id", "Original Title")
        
        root.edit_id("p_id", "new_title1")
        self.assertEqual(root.find_by_id("new_title1").id, "new_title1")

        root.edit_text("new_title1", "Updated Title")
        self.assertEqual(root.find_by_id("new_title1").content, "Updated Title")

    def test_delete_element(self):
        # 测试删除元素
        root = HtmlElement.init()
        div = HtmlElement(tag="div", element_id="div_id")
        root.add_child(div)
        root.delete("div_id")
        self.assertIsNone(root.find_by_id("div_id"))

    def test_undo_and_redo(self):
        # 测试撤销和重做操作
        root = HtmlElement.init()
        root.append("div", "div_id", "html")
        div = root.find_by_id("div_id")
        root.append("p", "p_id", "div_id", "Original Title")
        root=root.undo()
        self.assertIsNone(root.find_by_id("p_id"))

        root=root.redo()
        self.assertEqual(root.find_by_id("p_id").content, "Original Title")

    def test_spell_check(self):
        # 测试拼写检查功能
        element = HtmlElement(tag="p", content="Thiss is a tst.", element_id="p1")
        element.spell_check()
        self.assertFalse(element.spell_correct)

    def test_tab_render(self):
        # 测试缩进渲染
        root = HtmlElement.init()
        root.append("div", "div_id", "html")
        div = root.find_by_id("div_id")
        div.append("p", "p_id", "div_id", "My Page")
        expected_output = """  <html>
    <head>
      <title></title>
    </head>
    <body></body>
    <div id="div_id">
      <p id="p_id">My Page</p>
    </div>
  </html>
"""

        self.assertEqual(root.tab_render(indent=2, step=2), expected_output)

    def test_tree_render(self):
        # 测试树状渲染
        root = HtmlElement.init()
        root.append("div", "div_id", "html")
        div = root.find_by_id("div_id")
        div.append("p", "p_id", "div_id", "My Page")
        expected_output = """html
├── head
│   └── title
├── body
└── div#div_id
    └── p#p_id
        └── My Page
"""
        self.assertEqual(root.tree_render(), expected_output)

    def test_save_and_read(self):
        # 测试保存和读取功能
        path = "test.html"
        root = HtmlElement.init()
        root.append("div", "div1", "html")
        div = root.find_by_id("div1")
        div.append("p", "title1", "div1", "My Page")
        HtmlElement.save(path, root)
        loaded_root = HtmlElement.read(path)
        self.assertEqual(loaded_root.find_by_id("title1").content, "My Page")

    def tearDown(self):
        # 测试后清理
        HtmlElement.reset()


if __name__ == "__main__":
    unittest.main()