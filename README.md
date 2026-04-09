# multimodal-agent-t2i

论文级多模态智能体文生图系统项目。

## 项目总体规划

请查看：`docs/PROJECT_MASTER_PLAN.md`

## 当前工程结构

核心代码位于 `src/`，其中：
- `src/schemas/generation.py`：生成协议
- `src/models/`：T2I 后端与 generator service
- `src/utils/logging.py`：JSONL 运行日志
- `src/main.py`：命令行入口

## 运行与测试

- 运行：`python -m src.main --prompt "一只戴墨镜的柴犬，电影感"`
- 测试：`pytest`
- Demo：`bash scripts/run_demo.sh`

## 在服务器启用 SDXL 真模型

当前工程默认后端是 `sdxl`，并且已经支持两种模式：

- 安装了 `torch + diffusers`：调用真实 SDXL 生成图片。
- 未安装相关依赖：自动回退到占位图（保证链路可运行）。

### 1) 安装依赖（建议在 GPU 服务器）

> `torch` 需要按你的 CUDA 版本安装，以下命令仅为示例。

```bash
pip install diffusers transformers accelerate safetensors
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### 2) 配置 SDXL 模型

在 `configs/base.yaml` 的 `generator.backends.sdxl` 配置：

- `model_id`：可填 HF 仓库 ID 或本地模型目录。
- `device`：`cuda` / `cpu` / `null`（自动选择）。
- `torch_dtype`：`float16` / `float32` / `bfloat16`。
- `local_files_only`：离线服务器建议设为 `true`。

### 3) 运行

```bash
python -m src.main \
  --config configs/base.yaml \
  --backend sdxl \
  --prompt "cinematic photo of a corgi astronaut on Mars" \
  --num-images 2 \
  --seed 42
```
