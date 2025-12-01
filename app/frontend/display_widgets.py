import streamlit as st

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
    
def display_transcription(speakers_list):

    # Colors for each speaker
    colors = {
        0: "#d2e3fc",  # light blue (speaker 0)
        1: "#fde2e4",  # light pink (speaker 1)
    }

    # Start scrollable container
    html = """
        <div style="
            height: 200px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #fafafa;">
    """

    # Build message bubbles
    for msg in speakers_list:
        speaker = msg["speaker_id"]
        text = msg["speaker_text"].replace("\n", "<br>")
        color = colors.get(speaker, "#eee")

        # Speaker 0 → left
        if speaker == 0:
            bubble = f"""
                <div style="
                    background-color: {color};
                    padding: 10px;
                    margin: 6px 0;
                    border-radius: 10px;
                    max-width: 70%;
                    text-align: left;">
                    {text}
                </div>
            """
            html += f'<div style="display:flex; justify-content:flex-start;">{bubble}</div>'

        # Speaker 1 → right
        else:
            bubble = f"""
                <div style="
                    background-color: {color};
                    padding: 10px;
                    margin: 6px 0;
                    border-radius: 10px;
                    max-width: 70%;
                    text-align: right;">
                    {text}
                </div>
            """
            html += f'<div style="display:flex; justify-content:flex-end;">{bubble}</div>'
    html += "</div>"
    return html