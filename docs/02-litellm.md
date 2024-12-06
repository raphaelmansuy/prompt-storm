# LiteLLM Documentation: Streaming + Async

LiteLLM provides robust support for both **streaming responses** and **asynchronous completions**, enabling developers to handle real-time data and efficiently integrate LLM APIs into their workflows. Below is the detailed documentation on these features:

---

## **Streaming Responses**

### Overview
LiteLLM allows streaming the model's response by passing `stream=True` as an argument to the `completion` function. This feature is especially useful for applications that require real-time feedback, such as chatbots or live transcription.

---

### **Usage: Streaming Responses**

```python
from litellm import completion

messages = [{"role": "user", "content": "Hey, how's it going?"}]
response = completion(model="gpt-4o-mini", messages=messages, stream=True)

# Process the streaming response
for part in response:
    print(part.choices[0].delta.content or "")
```

---

### **Helper Function: Rebuild Complete Streaming Response**

LiteLLM includes a helper function, `stream_chunk_builder`, to concatenate all the streaming chunks into a single response.

```python
from litellm import completion

# Initialize messages
messages = [{"role": "user", "content": "Hey, how's it going?"}]
chunks = []

# Streaming response
response = completion(model="gpt-4o-mini", messages=messages, stream=True)

# Collect chunks
for chunk in response:
    chunks.append(chunk)

# Rebuild full response
from litellm import stream_chunk_builder
print(stream_chunk_builder(chunks, messages=messages))
```

---

## **Async Completion**

### Overview
LiteLLM supports asynchronous completions using the `acompletion` function. This is particularly useful for high-performance applications where non-blocking I/O operations are critical.

---

### **Usage: Asynchronous Completion**

```python
from litellm import acompletion
import asyncio

async def test_get_response():
    user_message = "Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="gpt-4o-mini", messages=messages)
    return response

response = asyncio.run(test_get_response())
print(response)
```

---

## **Async + Streaming Completion**

### Overview
LiteLLM supports asynchronous streaming functionality, enabling developers to handle streaming responses within async workflows. This is implemented using the `__anext__()` function for async iteration.

---

### **Usage: Asynchronous Streaming**

```python
from litellm import acompletion
import asyncio, os, traceback

async def completion_call():
    try:
        print("Starting async streaming completion...")
        response = await acompletion(
            model="gpt-4o-mini",
            messages=[{"content": "Hello, how are you?", "role": "user"}],
            stream=True
        )
        print(f"Response metadata: {response}")
        async for chunk in response:
            print(chunk)
    except Exception:
        print(f"Error occurred: {traceback.format_exc()}")
        pass

asyncio.run(completion_call())
```

---

## **Error Handling: Infinite Loops in Streaming**

### Issue
Some models may enter an infinite loop, continuously repeating the same response chunks. LiteLLM provides built-in protection against such scenarios by tracking the repetition of chunks.

### Solution
Use `litellm.REPEATED_STREAMING_CHUNK_LIMIT` to limit the number of repeated chunks. If the limit is exceeded, LiteLLM raises a `litellm.InternalServerError`.

```python
import litellm
import time

# Set the repetition limit
litellm.REPEATED_STREAMING_CHUNK_LIMIT = 100

# Simulate a looping response
chunks = [
    litellm.ModelResponse(**{
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 1694268190,
        "model": "gpt-4o-mini-0125",
        "system_fingerprint": "fp_44709d6fcb",
        "choices": [{"index": 0, "delta": {"content": "How are you?"}, "finish_reason": "stop"}],
    }, stream=True)
] * (litellm.REPEATED_STREAMING_CHUNK_LIMIT + 1)

# Wrap the response
completion_stream = litellm.ModelResponseListIterator(model_responses=chunks)
response = litellm.CustomStreamWrapper(
    completion_stream=completion_stream,
    model="gpt-4o-mini",
    custom_llm_provider="test_provider",
    logging_obj=litellm.Logging(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hey"}],
        stream=True,
        call_type="completion",
        start_time=time.time(),
        litellm_call_id="12345",
        function_id="1245",
    ),
)

# Iterate over the response (will raise InternalServerError)
for chunk in response:
    continue
```

### Notes:
- Default repetition limit: **100**
- To adjust this limit, modify `litellm.REPEATED_STREAMING_CHUNK_LIMIT`.

---

## **Logging and Observability for Streaming**

### Track Costs, Usage, and Latency
LiteLLM allows you to define custom callback functions to monitor costs, usage, and latency during streaming.

#### Example: Custom Callback for Cost Tracking

```python
import litellm

# Define a custom callback
def track_cost_callback(kwargs, completion_response, start_time, end_time):
    try:
        response_cost = kwargs.get("response_cost", 0)
        print("Streaming response cost:", response_cost)
    except Exception:
        pass

# Set the callback
litellm.success_callback = [track_cost_callback]

# Make a streaming completion call
response = litellm.completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi 👋 - I'm OpenAI"}],
    stream=True
)

for chunk in response:
    pass
```

---

## **Proxy Support for Streaming**

LiteLLM's Proxy Server also supports streaming completions. You can route streaming requests via the proxy server.

### **Quick Start with Proxy**

1. Start the proxy server:
   ```bash
   $ litellm --model huggingface/bigcode/starcoder
   # INFO: Proxy running on http://0.0.0.0:4000
   ```

2. Make a streaming completion request:
   ```python
   import openai

   # Configure OpenAI client to use the LiteLLM Proxy Server
   client = openai.OpenAI(api_key="your-api-key", base_url="http://0.0.0.0:4000")
   response = client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": "Write a short poem."}]
   )

   for chunk in response:
       print(chunk)
   ```

---

## **Mock Responses for Streaming**

LiteLLM allows you to mock streaming responses to save costs during testing.

### Example: Mock Streaming Response

```python
from litellm import completion

model = "gpt-4o-mini"
messages = [{"role": "user", "content": "Hey, I'm a mock request"}]

response = completion(model=model, messages=messages, stream=True, mock_response="Mock response content")
for chunk in response:
    print(chunk)  # {'choices': [{'delta': {'role': 'assistant', 'content': 'Mock'}, 'finish_reason': None}]}
```

---

This documentation covers the core aspects of **Streaming** and **Async Completion** in LiteLLM. For further details, visit the [LiteLLM GitHub Repository](https://github.com/BerriAI/litellm).