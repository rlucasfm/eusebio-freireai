import asyncio
import streamlit as st
from openai import OpenAI
from llama_index.core import StorageContext, load_index_from_storage

from Workflow.ChatFlow import ChatFlow

client = OpenAI()
assistant_id = "asst_gVWsPVMdh1MbgwR2K7Y3Gs9C"


st.title("FreireAI/Eusébio")

storage_context = StorageContext.from_defaults(persist_dir="vectorstorage")
index = load_index_from_storage(storage_context)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """Bem-vindo! Eu sou o FreireAI, um cérebro artificial pronto pra te ajudar a entender um pouco mais sobre o Project Thinking.
                                    \nSou uma criação da FWK Labs. Caso queira saber mais, acesse: https://fwk.global."""}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state['thread_id'] = thread.id
    
async def get_response():
    flow = ChatFlow()
    result = await flow.run(query=prompt, thread_id=st.session_state['thread_id'], index=index)

    if result is not None:
        print(result)

    msg = result['response'] + "\n \n \n Fontes citadas: " + result['source']

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    asyncio.run(get_response())
    

        
