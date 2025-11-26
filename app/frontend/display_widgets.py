def get_scrollable_box(text):
    html_text = f"""
        <div style="
            border: 1px solid #ccc;
            padding: 1rem;
            height: 200px;
            overflow-y: auto;
            font-family: sans-serif;
        ">
            {text}
        </div>
    """
    return html_text