from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 你本地模型的真实路径
model_path = r"D:\model_T\Qwen\Qwen3-2.5\qwen\Qwen2.5-0.5B-Instruct"

# 加载本地模型 + 分词器
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="cuda"  # 用GPU，没有就写 "cpu"
)

# 创建本地推理 pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.95,
    do_sample=True
)

# 包装成 Langchain 格式
llm = HuggingFacePipeline(pipeline=pipe)

# 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手"),
    ("user", "{user_question}")
])

# 构建链
chain = prompt | llm

# 运行
response = chain.invoke({"user_question": "你好"})
print(response)