import sys
from element import HtmlElement


def main():
    root = HtmlElement('', element_id='default')
    print("请输入命令，输入 'exit' 退出：")

    safe_cmds = ("exit", "read", "init")
    dynamic_cmds = ("insert","append","edit-id","edit-text","delete","print-indent","print-tree","spell-check","undo","redo")
    static_cmds = ("read", "save", "init")

    static_cmds_func = {
        "read":[HtmlElement.read, "无法读取文件"],
        "save":[HtmlElement.save, "无法写入文件"],
        "init":[HtmlElement.init, "无法初始化"]
    }

    for line in sys.stdin:
        dynamic_cmds_func = {
            "insert": [root.insert, "无法插入"],
            "append": [root.append, "无法插入"],
            "edit-id":[root.edit_id, "无法编辑id"],
            "edit-text":[root.edit_text, "无法编辑text"],
            "delete":[root.delete, "无法删除"],
            "print-indent":[root.print_indent, "无法显示"],
            "print-tree":[root.print_tree, "无法显示"],
            "spell-check":[root.spell_check, "无法检查"],
            "undo":[root.undo, "无法撤销"],
            "redo":[root.redo, "无法重做"],
        }
        command = line.strip()
        if command.lower() == 'exit':
            break

        parts = command.split()
        if not parts: continue
        cmd = parts[0]
        if cmd not in set(dynamic_cmds)|set(static_cmds):
            print("不支持的命令")
            continue
        
        if not root and cmd in dynamic_cmds:
            print(f"未初始化，无法执行 {cmd}")
            continue

        print(cmd,'##############')
        if cmd == "edit-id":
            1+1
        args = parts[1:]
        act = dynamic_cmds_func[cmd] if cmd in dynamic_cmds else static_cmds_func[cmd]
        try:
            if cmd == "save": args.append(root)
            res = act[0](*args)
            if cmd in ["init", "read", "undo", "redo"]: root = res
        except Exception as e:
            print(act[1], e)
            

if __name__ == "__main__":
    sys.stdin = [
        "print-tree",
        "init",
        "print-tree",
        "read example.html",
        "print-tree",
        "append li item4 list Item 4",
        "print-tree",
        "edit-id list list-new",
        "print-tree",
        "edit-text list-new now I have content",
        "print-tree",
        "delete item3",
        "print-tree",
        "spell-check",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "undo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "redo",
        "print-tree",
        "undo",
        "print-tree",
        "save test.html",
        "undo",
        "print-tree",
        
    ]
    main()
