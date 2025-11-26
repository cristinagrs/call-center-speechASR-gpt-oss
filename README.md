Project that transcribes audio from Call Centers using OCI Speech and then gets insights using OCI Generative AI Service with OpenAI gpt-oss models.

# How to run the app
Install requirements:

Go to the main app folder:
cd app

Create a .config file with the following variables:


1. Install Python (this project requires Python 3.13.5 or later). You can check your current Python version by running:
   ```
   python --version
   ```
   or
   ```
   python3 --version
   ```
2. Install the requirements from `requirements.txt` file.
   ```
   pip install -r requirements.txt
   ```
3. Create a bucket in OCI, copy the namespace and name for the configuration.
4. Move to the app folder: ```cd app```
5. Create a `.config` file with the following variables:
   ```
   CONFIG_FILE_PATH = <path_to_oci_login_config_file>
   PROFILE_NAME = "DEFAULT" ## profile name in config file
   COMPARTMENT_ID = <compartment_OCID>

   # Change the endpoint to match your account's region
   ENDPOINT = "https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com"

   BUCKET_NAMESPACE = "<bucket-namespace>"
   BUCKET_NAME = "<bucket-name>"
   ```

6. Run the app:
   ```
   streamlit run app.py
   ```
