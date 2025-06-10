from transformers import GPT2LMHeadModel, GPT2Tokenizer
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
import asyncio

class GPT2Connector:
    def __init__(self, model_name="gpt2"):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    async def get_chat_message_contents(self, messages: str, settings: PromptExecutionSettings = None, chat_history: ChatHistory = None):
        input_ids = self.tokenizer.encode(messages, return_tensors="pt")
        output = self.model.generate(
                        input_ids,max_length=150,no_repeat_ngram_size=3,pad_token_id=self.tokenizer.eos_token_id
                    ) # Prevents repeating 3-grams
        response_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        

        return [ChatMessageContent(role=AuthorRole.ASSISTANT, content=response_text)]

async def main():
    gpt2_service = GPT2Connector()

    # Example prompt
    prompt = "Explain the term 'center frequency' in signal processing in one sentence"

    response = await gpt2_service.get_chat_message_contents(
        messages=prompt,
        settings=PromptExecutionSettings(),
    )

    print("🤖 Response:", response[0].content)

if __name__ == "__main__":
    asyncio.run(main())
