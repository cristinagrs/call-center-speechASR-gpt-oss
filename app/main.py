import os
import streamlit as st
import config
from backend import ai_tools
from frontend import display_widgets, navbar

## TODO: add diarization
## show better the transcription, with the diarization

def upload_audio(uploaded_file):
    uploaded_file.seek(0)
    audio_file = os.path.join(config.UPLOAD_PATH, uploaded_file.name)
    if not os.path.exists(config.UPLOAD_PATH): os.mkdir(config.UPLOAD_PATH)
    with open(audio_file, "wb") as f: f.write(uploaded_file.read())
    return audio_file

def main():
    ## init ##
    st.markdown("<h1 style='margin-bottom: 0;'>Process Audio</h1>", unsafe_allow_html=True)
    st.divider()

    speech_pipeline = ai_tools.SpeechPipeline(config)
    genai_pipeline = ai_tools.GenAIPipeline(config)

    uploaded_file, run_button, selected_model = navbar.make_sidebar(config)

    if uploaded_file and run_button:
        do_diarization = True

        with st.spinner("Transcribing...", show_time=True):
            audio_file = upload_audio(uploaded_file) ## save file
            ####
            st.audio(audio_file)
            whisper_trans = speech_pipeline.get_transcription(
                audio_file, model_type="Oracle",#"Whisper", #
                whisper_prompt=None, diarization=do_diarization, number_of_speakers=2)
            processed_trans, speakers_list = ai_tools.post_process_trans(whisper_trans, diarization=do_diarization)

        st.header('SPEECH TRANSCRIPTION:')
        #st.divider()
        if do_diarization:
            transcription_display = display_widgets.display_transcription(speakers_list)
        else:
            transcription_display = display_widgets.get_scrollable_box(text=processed_trans)
        st.markdown(transcription_display, unsafe_allow_html=True)

        with st.spinner("Getting LLM summary...", show_time=True):
            prompt = config.SUMMARIZE_PROMPT.format(
                conversation = processed_trans,
                format = config.SUMMARY_FORMAT
            )
            response = genai_pipeline.get_chat_response(prompt, model_id=config.GENAI_MODELS[selected_model])
        
        # write LLM response
        st.header('CALL SUMMARY BY LLM:')
        #st.divider()
        st.markdown(response)

if __name__=='__main__':
    main()