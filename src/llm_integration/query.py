from .tokenization import get_token_length
import config
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

def construct_prompt(similar_contexts: list[str]) -> str:
    """
    Fetch relevant 
    """
    chosen_contexts = []
    chosen_contexts_len = 0
    separator_len = get_token_length(config.SEPERATOR)
     
    for sim_context in similar_contexts:
        
        chosen_contexts_len += get_token_length(sim_context) + separator_len
        if chosen_contexts_len > config.MAX_TOKEN_LENGTH:
            break
            
        chosen_contexts.append(config.SEPERATOR + sim_context.replace("\n", " "))            
        
    return chosen_contexts, chosen_contexts_len

def answer_with_gpt_4(
    query: str,
    similar_contexts: list[str],
    show_prompt: bool = True
) -> str:
    messages = [
        {"role" : "system", "content":"You are a Ballpark Housing chatbot, only answer the question by using the provided context. If your are unable to answer the question using the provided context, say 'I don't know'"}
    ]
    prompt, context_length = construct_prompt(
        similar_contexts
    )
    if show_prompt:
        print("Prompt: ", prompt)

    context= ""
    for article in prompt:
        context = context + article 

    context = context + '\n\n --- \n\n + ' + query

    messages.append({"role" : "user", "content":context})
    response = client.chat.completions.create(
        model=config.COMPLETIONS_MODEL,
        messages=messages,  
    )
    
    # logging.info("Model response: ", response)

    return '\n' + response.choices[0].message.content, context_length