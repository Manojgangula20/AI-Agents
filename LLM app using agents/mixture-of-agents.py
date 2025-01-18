import streamlit as st
import asyncio
import os
from together import AsyncTogether, Together

st.title("Mixture-of-Agents LLM App")
together_api_key = st.text_input("Enter your Together API Key:", type="password")

if together_api_key:
    os.environ["TOGETHER_API_KEY"] = together_api_key
    client = Together(api_key=together_api_key)
    async_client = AsyncTogether(api_key=together_api_key)

reference_models=[
    "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "google/gemma-2b-it",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    
]
aggregator_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

aggregator_system_prompt = """You have been provided with a set of responses from various open-source models to the latest user query.
Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information
provided in these responses, recognizing that some of it may be biased or incorrect. Your responses should not simply replicate the given
answers but should offer a refined, accurate and comprehensive reply to the instruction. Ensure your response is well-structured, coherenet
and adheres to the highest standards of accuracy and reliability. Responses from models:"""

async def run_llm(model):
    response = await async_client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content": user_prompt}],
        temperature=0.7,
        max_tokens=512,
    )
    return model, response.choices[0].message.content

async def main():
    results = await asyncio.gather(*[run_llm(model) for model in reference_models])

    # Display individual model responses:
    st.subheader("Individual Model Responses:")
    for model, response in results:
        with st.expander(f"Response from {model}"):
            st.write(response)

    #Aggregate Responses
    st.subheader("Aggregated Response:")
    finalStream= client.chat.completions.create(
        model=aggregator_model,
        messages=[
            {"role": "system", "content": aggregator_system_prompt},
            {"role":"user", "content":",".join(response for _,response in results)},
        ],
        stream= True
    )

    # Display aggregated response
    response_container = st.empty()
    full_response = ""
    for chunk in finalStream:
        content = chunk.choices[0].delta.content or ""
        full_response += content
        response_container.markdown(full_response + " ")
    response_container.markdown(full_response)

user_prompt = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if user_prompt:
        asyncio.run(main())
    else:
        st.warning("Please enter a question.")
    
      




    