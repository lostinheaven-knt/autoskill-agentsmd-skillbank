# SkillBank 治理改造执行清单

> 用途：把 `docs/skillbank-governance-v2-implementation.md` 压缩成可执行任务单。
> 
> 使用方式：按批次执行；每完成一项就打勾并提交。

---

## 批次 0：止血与基线

### 0.1 基线盘点
- [ ] 新建分支：`cleanup/skillbank-governance-v2`
- [ ] 新建 `reports/`
- [ ] 运行/补齐 inventory 报告脚本
- [ ] 产出 `reports/skillbank-inventory.md`
- [ ] 产出 `reports/skillbank-inventory.json`

### 0.2 production 止血
- [ ] 从 `AGENTS.md` index 中清除明显坏示范路径
- [ ] 标出 production tree 中的 `imported/` 路径
- [ ] 标出 `product/genstore/genstore-operation`
- [ ] 标出 `superpowers-raw/` 路径
- [ ] 标出随机/不可解释路径（如 `426345955d8e/...`）

### 0.3 seed 止血
- [ ] 明确 seed 保留原则：只留少量通用外部样例
- [ ] 建立 retained seed allowlist 初稿
- [ ] 标出必须移除/隔离的私有 seed

验收：
- [ ] 有 inventory 基线
- [ ] 有明确的 production 坏示范清单
- [ ] 有 seed 保留白名单初稿

---

## 批次 1：治理文件入场

### 1.1 meta 文件
- [ ] 新建 `SkillBank/meta/production-skill-checklist.md`
- [ ] 新建 `SkillBank/meta/seed-status-conventions.md`
- [ ] 新建 `SkillBank/meta/retained-seed-allowlist.yml`
- [ ] 新建 `SkillBank/meta/taxonomy.yml`
- [ ] 新建 `SkillBank/meta/inventory.schema.json`

### 1.2 文档修正
- [ ] 更新 `SkillBank/README.md`
- [ ] 更新根 `README.md` 的定位描述
- [ ] 更新 `TECHNICAL_SPEC.md`，删除 pipeline-first 口径

验收：
- [ ] repo 内有完整治理元文件
- [ ] 文档开始反映 governance-first 路线

---

## 批次 2：脚本模块骨架

### 2.1 建模块目录
- [ ] 新建 `scripts/skillbank/__init__.py`
- [ ] 新建 `scripts/skillbank/paths.py`
- [ ] 新建 `scripts/skillbank/indexer.py`
- [ ] 新建 `scripts/skillbank/inventory.py`
- [ ] 新建 `scripts/skillbank/detectors.py`
- [ ] 新建 `scripts/skillbank/validators.py`
- [ ] 新建 `scripts/skillbank/reports.py`

### 2.2 迁出 indexer 逻辑
- [ ] `build_agents_md_index.py` 改为调用 `skillbank.indexer`
- [ ] 保持 `--print/--write` 兼容
- [ ] 测试通过

验收：
- [ ] 脚本不再把核心逻辑全塞在 CLI 文件里
- [ ] index 构建逻辑可复用

---

## 批次 3：第一批治理型 CLI

### 3.1 inventory
- [ ] 新建 `scripts/review_inventory.py`
- [ ] 支持 `--print`
- [ ] 支持 `--write`
- [ ] 输出 markdown/json 报告

### 3.2 validate
- [ ] 新建 `scripts/validate_seed_status.py`
- [ ] 新建 `scripts/validate_production_skills.py`
- [ ] 先实现最小校验：状态标签、坏路径、敏感信号、TODO-heavy

### 3.3 reports
- [ ] 统一报告输出格式
- [ ] 统一退出码策略

验收：
- [ ] 可以用 CLI 看清 repo 当前问题
- [ ] 可以对 production/seed 做基础 gate

---

## 批次 4：seed 收口

### 4.1 新目录语义
- [ ] 建立 `SkillBank/seed_openclaw_skills/`
- [ ] 建立 `SkillBank/.trash/`
- [ ] 明确旧 `skill-seeds/` 退役策略

### 4.2 裁剪 seed
- [ ] 新建 `scripts/prune_seed_examples.py`
- [ ] `--dry-run` 输出将保留/将迁移列表
- [ ] `--apply` 将非 allowlist seed 移到 `.trash/`
- [ ] 保留样例数量控制在 5~8 个

### 4.3 seed 状态
- [ ] 为保留 seed 补 `SEED STATUS`
- [ ] 对敏感 seed 明确 `SENSITIVE`

验收：
- [ ] seed 目录规模显著收缩
- [ ] 没有明显私有/敏感 seed 留在示范面

---

## 批次 5：production 树清理

### 5.1 路径清理
- [ ] 从 `SkillBank/skills/` 移出 `imported/`
- [ ] 从 `SkillBank/skills/` 移出 `superpowers-raw/`
- [ ] 从 `SkillBank/skills/` 移出 `product/genstore/genstore-operation`
- [ ] 处理随机/不可解释路径

### 5.2 taxonomy 对齐
- [ ] 建立稳定分类树
- [ ] 调整现有 production 路径到 taxonomy 下
- [ ] 重新生成 AGENTS index

验收：
- [ ] `SkillBank/skills/` 一眼看上去像 production，不像事故现场
- [ ] AGENTS index 不再暴露坏示范路径

---

## 批次 6：legacy 收口

### 6.1 迁移旧脚本
- [ ] 新建 `scripts/_legacy/`
- [ ] 移入 `pipeline_init.py`
- [ ] 移入 `llm_fill_drafts.py`
- [ ] 移入 `import_seeds_to_drafts.py`
- [ ] 移入 `dedupe_merge_skills.py`
- [ ] 移入 `promote_drafts.py`

### 6.2 文档标记
- [ ] 为 legacy 文件加顶部说明
- [ ] README 不再推荐 legacy 命令

验收：
- [ ] 新读者不会再被旧流水线误导

---

## 批次 7：第二批治理 CLI

### 7.1 sanitize
- [ ] 新建 `scripts/sanitize_repo_samples.py`
- [ ] 支持 `--check`
- [ ] 支持 `--apply`

### 7.2 duplicates
- [ ] 新建 `scripts/suggest_duplicates.py`
- [ ] 只建议，不自动 merge

### 7.3 reviewed promotion
- [ ] 新建 `scripts/promote_reviewed_skill.py`
- [ ] 只允许显式 `--src --dst`
- [ ] promotion 前自动跑 validation

### 7.4 demo install
- [ ] 新建 `scripts/install_demo_workspace.py`
- [ ] 仅安装 production/meta/index

验收：
- [ ] 新 CLI 都符合治理优先的哲学

---

## 批次 8：测试与 CI

### 8.1 测试文件
- [ ] `tests/test_indexer.py`
- [ ] `tests/test_inventory.py`
- [ ] `tests/test_seed_validation.py`
- [ ] `tests/test_production_validation.py`
- [ ] `tests/test_prune_seed_examples.py`

### 8.2 现有测试迁移
- [ ] 保留/重命名 `test_build_agents_md_index.py`
- [ ] 确保模块化后仍通过

### 8.3 CI
- [ ] 可选新增 GitHub Actions / 本地 make target

验收：
- [ ] pytest 全绿
- [ ] 治理规则具备自动回归保护

---

## 当前建议的开工顺序

### 第一波（立刻动手）
- [ ] implementation checklist 落仓
- [ ] meta 治理文件落仓
- [ ] `scripts/skillbank/` 基础骨架
- [ ] `build_agents_md_index.py` 模块化
- [ ] `review_inventory.py` 首版
- [ ] `SkillBank/README.md` 修正

### 第二波（止血）
- [ ] inventory 报告
- [ ] 生产树坏路径清单
- [ ] seed allowlist 初版
- [ ] 生成新的 AGENTS index

### 第三波（真正清仓）
- [ ] prune seed
- [ ] clean production tree
- [ ] migrate legacy
- [ ] 补测试

---

## 本清单完成标准

- [ ] 有治理文件
- [ ] 有 inventory 脚本
- [ ] 有基础 validation
- [ ] 有 seed 收口动作
- [ ] 有 production 清理动作
- [ ] 有 legacy 收口
- [ ] 有测试兜底

一句话：

**先把“仓长得像个治理仓”做出来，再把“脚本会治理”补齐。**
