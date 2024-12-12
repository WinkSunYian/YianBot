def construct(items):
    show = "┏ ━ ━ ━\n"
    if items is None:
        show += "┣ 空空如也\n"
    else:
        for item in items:
            show += f"┣ {item.name} * {item.quantity}\n"
    show += "┗ ━ ━ ━"
    return show