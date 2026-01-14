import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError

aws_profile = "mvp"  # Nome do perfil configurado no AWS CLI (ex.: default)
region = "us-east-1"  # Região AWS
model_id = "amazon.nova-lite-v1:0"

#Sessão python
session = boto3.Session(profile_name=aws_profile, region_name=region)

#valida seção do chat
if "chat" not in st.session_state:
    st.session_state.chat = []

def request_to_bedrock(question):
    #st.session_state.pergunta = ""
    bedrock = session.client(
        service_name="bedrock-runtime"
    )
    conversation = [
        {
        "role": "user",
        "content": [{"text": question}],
        }
    ]
    try:
        # Send the message to the model, using a basic inference configuration.
        response = bedrock.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
            )
        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except (ClientError, Exception) as e:
        return f"ERROR: Can't invoke '{model_id}'. Reason: {e}"
    


st.title(f"Aplicação Simples utilizando BedRock")
pergunta = st.text_input(f"Digite uma pergunta para o {model_id}: ", key="pergunta")

if pergunta:
    resposta = request_to_bedrock(pergunta)
    st.session_state.chat.append({
        "pergunta": pergunta,
        "resposta": resposta
    })
    #st.session_state.text_input = ""


for item in st.session_state.chat:
    st.markdown(f"**Pergunta:** {item['pergunta']}")
    st.markdown(f"**Resposta:** {item['resposta']}")
    st.markdown("---")
