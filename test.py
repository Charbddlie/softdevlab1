from element import HtmlElement

# # 使用示例
# head = HtmlElement('head', 'Title')
# body = HtmlElement('body', '', [
#     HtmlElement('div', 'Hello World!', element_id='div1'),
#     HtmlElement('div', 'This is a div.', element_id='div2'),
# ])

# html = HtmlElement('html', '', [head, body])

# # 渲染 HTML
# print(html.tab_render())
# html_element = HtmlElement.read("example.html")
html_element = HtmlElement.init()
# 渲染并打印 HtmlElement 对象
print(html_element.tab_render())
print(html_element.tree_render())
