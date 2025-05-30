# Ollama

## Mac上安装ollama

在 https://ollama.com/download ollmam官网下载对应的版本并安装在电脑上（Mac上下载之后直接放到应用程序文件里就行）。
首次打开ollama会有安装提示，点击next->install就行了，以后再打开ollama就没有安装提示了，在屏幕上方状态栏会有ollama图标。

````shell
# 修改环境变量改变模型存储位置
# Linux系统是~/.bashrc
vi ~/.zshrc

# 在文件末尾增加
export OLLAMA_MODELS=/Users/sunweisheng/Documents/OllamaModel

# 重新加载
# Linux系统是~/.bashrc
source ~/.zshrc
````

## 下载并运行模型
在 https://ollama.com/search 选择模型复制下载指令并下载：
````shell
# 默认是qwen3 8.19B Q4_K_M
ollama pull qwen3
````

## 管理模型

````shell
# 列出下载的所有模型
# 可以执行这个命令之后查看新路径中是否自动创建了新文件夹（blobs和manifests）就知道新路径是否生效
ollama list 

# 显示
NAME            ID              SIZE      MODIFIED           
qwen3:latest    e4b5fd7f8af0    5.2 GB    About a minute ago  

# 移除指定模型
ollama rm 模型名称

# 运行模型（如果没有自动下载）
ollama run qwen3
````

在Ubuntu中运行ollama
````shell
# 需要先启动服务
ollama serve
````
有两个启动参数：
OLLAMA_HOST：默认是127.0.0.1:11434只能被本机访问，改成0.0.0.0:11434就能被其他设备访问了。
OLLAMA_KEEP_ALIVE：如果5分钟不用ollama模型就会被卸载，可以改成-1避免这个问题。
````shell
OLLAMA_HOST=0.0.0.0:11434 OLLAMA_KEEP_ALIVE=-1 ollama serve
````

## 测试运行模型速度

````shell
# 输出结果增加运行指标结果
ollama run qwen3 --verbose

# Mac air M3 16G 回答问题时统一内存占用4.96G左右

# **总持续时间**  
# **含义**：整个推理流程的总耗时，包括模型加载、提示处理（prompt evaluation）和生成输出（eval）的全部时间。  
# **意义**：反映模型从接收到请求到返回结果的总时间，是整体性能的综合指标。
total duration:       28.705464125s

# **加载持续时间**  
# **含义**：模型加载到内存或准备就绪所需的时间。  
# **意义**：如果加载时间过长，可能需要优化模型加载流程（例如使用更高效的模型格式或硬件加速）。
load duration:        29.833667ms

# **提示评估计数**
# **含义**：处理输入提示（prompt）时，模型处理的token数量。  
# **意义**：表示模型对输入内容的解析和处理量，通常与输入长度相关。
prompt eval count:    17 token(s)

# **提示评估持续时间** 
# **含义**：模型处理输入提示（prompt）所花费的时间。  
# **意义**：反映模型对输入的解析效率。如果时间过长，可能需要优化输入格式或模型架构。
prompt eval duration: 2.965349458s

# **提示评估速率**
# **含义**：模型处理输入提示的token速度（token数/秒）。  
# **意义**：表示模型解析输入的效率。更高的速率意味着更高效的处理。
prompt eval rate:     5.73 tokens/s

# **评估计数** 
# **含义**：模型生成输出时处理的token数量（即生成的文本长度）。  
# **意义**：反映模型生成内容的长度，通常与输出复杂度相关。
eval count:           429 token(s)

# **评估持续时间**
# **含义**：模型生成输出（eval）所花费的时间。  
# **意义**：表示模型生成文本的耗时，若时间过长，可能需要优化生成策略（如调整温度、top-p等参数）或硬件资源
eval duration:        25.708690958s

# **评估速率**
# **含义**：模型生成输出的token速度（token数/秒）。  
# **意义**：反映模型生成文本的效率。较低的速率可能表明模型在生成复杂内容时需要更多计算资源。
eval rate:            16.69 tokens/s
````

````shell
# 另一台Mac min上测试一下
ollama run qwen3 --verbose

# Mac min M2 16G 回答问题时统一内存占用4.5G左右
total duration:       15.315935417s
load duration:        33.100459ms
prompt eval count:    17 token(s)
prompt eval duration: 709.963416ms
prompt eval rate:     23.94 tokens/s
eval count:           250 token(s)
eval duration:        14.571133792s
eval rate:            17.16 tokens/s
````

在Ubuntu中监控显卡使用情况可以用：
````shell
# 1秒刷新一次
watch -n 1 nvidia-smi
# 36核 128G内存 3090 24G显卡，qwen3 8B Q4量化版本回答问题时显存6.67G
ollama run qwen3 --verbose

total duration:       3.120056433s
load duration:        80.897589ms
prompt eval count:    18 token(s)
prompt eval duration: 311.190413ms
prompt eval rate:     57.84 tokens/s
eval count:           249 token(s)
eval duration:        2.726602382s
eval rate:            91.32 tokens/s

# 再试试其他模型
ollama list
NAME            ID              SIZE      MODIFIED     
qwen3:30b       0b28110b7a33    18 GB     23 hours ago    
qwen3:32b       030ee887880f    20 GB     23 hours ago    
qwen3:14b       bdbd181c33f2    9.3 GB    24 hours ago    
qwen3:latest    500a1f067a9f    5.2 GB    26 hours ago

# 36核 128G内存 3090 24G显卡，qwen3 32B Q4回答问题时显存20.7G
ollama run qwen3:32b --verbose

total duration:       11.292684395s
load duration:        108.30065ms
prompt eval count:    18 token(s)
prompt eval duration: 248.86851ms
prompt eval rate:     72.33 tokens/s
eval count:           351 token(s)
eval duration:        10.934249156s
eval rate:            32.10 tokens/s
````