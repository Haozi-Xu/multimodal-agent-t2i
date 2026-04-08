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
