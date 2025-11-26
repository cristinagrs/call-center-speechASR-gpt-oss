import os
import oci
from time import sleep
import json

class SpeechPipeline:
    "A class to transcribe the audio from a Video file"
    def __init__(self, config):
        oci_config = oci.config.from_file(config.CONFIG_FILE_PATH, profile_name=config.PROFILE_NAME)
        self.client = oci.ai_speech.AIServiceSpeechClient(oci_config)
        self.object_client = oci.object_storage.ObjectStorageClient(oci_config)
        self.config = config
    
    def upload_file_to_object_storage(self, file_path, object_name):        
        with open(file_path, 'rb') as f:
            response = self.object_client.put_object(
                namespace_name=self.config.BUCKET_NAMESPACE,
                bucket_name=self.config.BUCKET_NAME,
                object_name=object_name,
                put_object_body=f
            )
        print(f"Upload complete to bucket complete.")
        return response

    def get_transcription(self, audio_file, model_type, whisper_prompt=None):
        object_name = os.path.join(self.config.BUCKET_FILE_PREFIX, os.path.basename(audio_file))
        _ = self.upload_file_to_object_storage(audio_file, object_name)

        # Getting video file input location
        object_location_1 = oci.ai_speech.models.ObjectLocation(
            namespace_name=self.config.BUCKET_NAMESPACE,
            bucket_name=self.config.BUCKET_NAME,
            object_names=[object_name])
        input_location = oci.ai_speech.models.ObjectListInlineInputLocation(
            location_type="OBJECT_LIST_INLINE_INPUT_LOCATION",
            object_locations=[object_location_1])
        
        # Creating output location
        output_location = oci.ai_speech.models.OutputLocation(
            namespace_name=self.config.BUCKET_NAMESPACE,
            bucket_name=self.config.BUCKET_NAME,
            prefix = self.config.SPEECH_BUCKET_OUTPUT_PREFIX
        )

        if model_type == "Oracle":
            model_config = oci.ai_speech.models.TranscriptionModelDetails(
                model_type = "ORACLE",
                domain="GENERIC",
                language_code="it-IT",
            )
        
        elif whisper_prompt is None:
            model_config = oci.ai_speech.models.TranscriptionModelDetails(
                model_type="WHISPER_LARGE_V3T",
                domain="GENERIC",
                language_code="it", 
                #transcription_settings=oci.ai_speech.models.TranscriptionSettings(
                #    diarization=oci.ai_speech.models.Diarization(
                #        is_diarization_enabled=False,
                #    ),
                    #additional_settings={
                    #    "whisperPrompt": "<Sample Prompt Input>" # Only valid for Whisper models.
                    #    }
                #    )
            )
        else:
            model_config = oci.ai_speech.models.TranscriptionModelDetails(
                model_type="WHISPER_LARGE_V3T",
                domain="GENERIC",
                language_code="it", 
                transcription_settings=oci.ai_speech.models.TranscriptionSettings(
                    additional_settings={
                        "whisperPrompt": whisper_prompt # Only valid for Whisper models.
                    }
                )
            )

        ## Create transcription job
        transcription_job = self.client.create_transcription_job(
            create_transcription_job_details=oci.ai_speech.models.CreateTranscriptionJobDetails(
                compartment_id=self.config.COMPARTMENT_ID,
                input_location=input_location,
                output_location=output_location,
                model_details=model_config
            )
        )
        job_id = transcription_job.data.id
        seconds = 0
        while transcription_job.data.lifecycle_state == "IN_PROGRESS" or transcription_job.data.lifecycle_state == "ACCEPTED":
            print(f"Job {job_id} is IN_PROGRESS for {str(seconds)} seconds, progress: {transcription_job.data.percent_complete}")
            sleep(2)
            seconds += 2
            transcription_job = self.client.get_transcription_job(transcription_job_id=job_id)

        print(f"Job {job_id} is in {transcription_job.data.lifecycle_state} state.")
        if transcription_job.data.lifecycle_state == "FAILED":
            return f"Transcription job {job_id} failed."

        # Getting response from object storage
        list_response = self.object_client.list_objects(
            namespace_name=transcription_job.data.output_location.namespace_name,
            bucket_name=transcription_job.data.output_location.bucket_name,
            prefix=transcription_job.data.output_location.prefix
        )
        output_object_name = list_response.data.objects[0].name
        transcription_response = self.object_client.get_object(output_location.namespace_name, output_location.bucket_name, output_object_name)
        return transcription_response
    



class GenAIPipeline:
    def __init__(self, config):
        
        oci_config = oci.config.from_file(config.CONFIG_FILE_PATH, profile_name="LONDON")
        self.generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
            config=oci_config, 
            service_endpoint=config.ENDPOINT, 
            retry_strategy=oci.retry.NoneRetryStrategy(), 
            timeout=(10,240)
            )
        self.config = config

    def get_chat_response(self, input_message, model_id):

        txt = oci.generative_ai_inference.models.TextContent()
        txt.text = f"{input_message}"
        message = oci.generative_ai_inference.models.UserMessage()
        #oci.generative_ai_inference.models.Message()
        #message.role = "USER"
        message.content = [txt]

        chat_request = oci.generative_ai_inference.models.GenericChatRequest()
        chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
        chat_request.messages = [message]
        chat_request.max_tokens = 2048
        chat_request.temperature = 0.5
        chat_request.frequency_penalty = 0
        chat_request.presence_penalty = 0
        chat_request.top_p = 0.8
        chat_request.top_k = -1

        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id)
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = self.config.COMPARTMENT_ID

        response = self.generative_ai_inference_client.chat(chat_detail)
        return response.data.chat_response.choices[0].message.content[0].text
    

def post_process_trans(transcription_response):
    object_content_bytes = transcription_response.data.content  # this is in bytes
    object_content_str = object_content_bytes.decode("utf-8")

    transcription_json = json.loads(object_content_str)
    transcriptions = transcription_json.get("transcriptions", [])
    text_trans = "\n".join([trans['transcription'] for trans in transcriptions])
    return text_trans