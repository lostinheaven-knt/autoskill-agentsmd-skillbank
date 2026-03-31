# autoskill-agentsmd-skillbank 治理化改造实施文档（V2）

> 状态：proposal / implementation-ready
> 
> 目标：把 `autoskill-agentsmd-skillbank` 从“旧的 AutoSkill 批量炼丹实验仓”改造成“以 `workspace_coder/SkillBank` 为示范蓝本的治理优先 SkillBank 参考仓”。

---

## 1. 背景与结论

当前仓库存在三个核心问题：

1. `skill-seeds/` 样例过多，且混入私有、敏感、workspace-specific 内容
2. `SkillBank/skills/` 中存在 imported / legacy / private-ish / duplicated 内容，无法作为 production 示范
3. 脚本链路偏向“自动导入 → 自动补全 → 自动 promotion → 自动 merge”，与目前 SkillBank 治理原则冲突

因此，本次改造不再延续旧的“pipeline-first”路线，而改为：

- **少量 seed 示例**
- **严格 production / seed / draft 分层**
- **自动化脚本只做盘点、校验、脱敏、建议，不做激进自动 promotion**
- **以 `workspace_coder/SkillBank` 当前治理风格为标准样板**

---

## 2. 目标与非目标

## 2.1 目标

本次改造完成后，仓库应满足：

1. `SkillBank/skills/` 只保留 production-grade、可示范的技能
2. `SkillBank/seed_openclaw_skills/` 只保留少量外部下载、通用、已脱敏 seed
3. `AGENTS.md` 的 SkillBank index 只索引 production leaves
4. repo 提供治理型脚本：inventory / validate / sanitize / suggest / reviewed-promotion
5. README / 技术文档的心智模型与目录现实一致

## 2.2 非目标

本次改造**不追求**：

1. 自动把全部 seed 变成 production
2. 自动 LLM 补 skill 文本并作为可信产物
3. 自动 canonical merge 所有相似技能
4. 保留所有历史实验路径的兼容性
5. 把 repo 做成大型 skill 备份仓

---

## 3. 总体设计原则

1. **治理优先于产量**：宁可少，不要脏
2. **示范优先于归档**：这是参考仓，不是素材垃圾场
3. **production 必须可信**：能被索引，就要敢被自动阅读
4. **seed 必须显式标状态**：不能让人把矿石当成成品
5. **自动化以保守为先**：脚本给建议、报告、校验；promotion 需要显式审核
6. **目录语义要稳定**：路径一看就能知道角色，不出现 imported/raw/tmp/legacy 混杂污染

---

## 4. 目标目录结构

改造后的目录结构如下：

```text
autoskill-agentsmd-skillbank/
├── AGENTS.md
├── README.md
├── TECHNICAL_SPEC.md
├── docs/
│   └── skillbank-governance-v2-implementation.md
├── SkillBank/
│   ├── README.md
│   ├── skills/                         # production-grade skills only
│   ├── seed_openclaw_skills/           # 少量外部通用、已脱敏 seed
│   ├── drafts/                         # 人工整理中的候选
│   ├── meta/
│   │   ├── production-skill-checklist.md
│   │   ├── seed-status-conventions.md
│   │   ├── retained-seed-allowlist.yml
│   │   ├── taxonomy.yml
│   │   └── inventory.schema.json
│   ├── skill.template.md
│   └── .trash/
├── scripts/
│   ├── skillbank/
│   │   ├── __init__.py
│   │   ├── paths.py
│   │   ├── inventory.py
│   │   ├── detectors.py
│   │   ├── sanitize.py
│   │   ├── validators.py
│   │   ├── taxonomy.py
│   │   ├── indexer.py
│   │   └── reports.py
│   ├── build_agents_md_index.py
│   ├── review_inventory.py
│   ├── prune_seed_examples.py
│   ├── sanitize_repo_samples.py
│   ├── validate_seed_status.py
│   ├── validate_production_skills.py
│   ├── suggest_duplicates.py
│   ├── promote_reviewed_skill.py
│   ├── install_demo_workspace.py
│   └── _legacy/
│       ├── pipeline_init.py
│       ├── llm_fill_drafts.py
│       ├── dedupe_merge_skills.py
│       ├── import_seeds_to_drafts.py
│       └── promote_drafts.py
└── tests/
    ├── test_indexer.py
    ├── test_inventory.py
    ├── test_seed_validation.py
    ├── test_production_validation.py
    └── test_prune_seed_examples.py
```

---

## 5. 目录语义定义

## 5.1 `SkillBank/skills/`

职责：

- 只放 production-grade skill
- 只放可索引、可示范、可信任的 leaf
- 必须结构清晰、边界明确、无敏感私货

约束：

- 不允许出现 `imported/`、`raw/`、`legacy/`、`tmp/` 等过渡路径
- 不允许出现明显 diary / personal / private brand / admin URL / account-specific 内容
- 必须通过 production validation

## 5.2 `SkillBank/seed_openclaw_skills/`

职责：

- 存放少量 seed 示例
- 用于展示“原始 seed 长什么样、如何标状态”
- 只保留外部下载的通用 skill 样例

约束：

- 数量保持小规模，建议 5~8 个
- 每个 seed 必须显式标 status
- 敏感 seed 必须标 `SENSITIVE`
- workspace 私有 skill 原则上不进公开示范仓

## 5.3 `SkillBank/drafts/`

职责：

- 正在人工审阅/改造中的候选 skill
- 允许不完整，但不允许无限堆积

约束：

- 尽量少量
- 超过一个治理周期未推进的，移入 `.trash/`

## 5.4 `SkillBank/.trash/`

职责：

- 存放本次治理中退役、隔离、待观察内容
- 保留迁移 traceability

约束：

- 按日期分组
- README/文档不把 `.trash/` 当成有效运行面

---

## 6. 生产分类规范（taxonomy）

建议生产路径以稳定分类树组织：

```yaml
analysis:
  - finance
coding:
  - refactor
debugging:
  - first-15-min
media:
  - image
  - video
ops:
  - feishu
  - github
misc: []
```

生产路径示例：

- `analysis/finance/a-stock-quick-research`
- `coding/refactor/safe-refactor`
- `media/image/image-read`
- `ops/feishu/feishu-doc`
- `ops/github/github-cli`

禁止作为 production 路径示范的模式：

- `imported/openclaw-agents-skills/...`
- `product/genstore/genstore-operation`
- `426345955d8e/...`
- `superpowers-raw/...`

---

## 7. 改造范围：保留 / 重写 / 退休

## 7.1 保留并模块化

### `scripts/build_agents_md_index.py`

保留原因：

- 是最稳定、最有价值的核心功能之一
- 与治理化之后的仓库仍然高度一致

改造要求：

- 只索引 `SkillBank/skills/`
- 核心逻辑迁入 `scripts/skillbank/indexer.py`
- CLI 保持简单：`--print` / `--write`

---

## 7.2 重写为保守型工具

### 旧：`dedupe_merge_skills.py`
### 新：`suggest_duplicates.py`

新职责：

- 识别重复候选组
- 输出建议报告
- 不自动 merge canonical
- 不自动移动 production skill

### 旧：`promote_drafts.py`
### 新：`promote_reviewed_skill.py`

新职责：

- 显式输入 `--src` 与 `--dst`
- promotion 前必须跑 production validation / sensitive detection
- 不做 bulk promotion

### 旧：`install_into_openclaw_workspace.py`
### 新：`install_demo_workspace.py`

新职责：

- 安装演示版 SkillBank 到指定 workspace
- 只复制 production / meta，seed 作为可选项
- 注入 AGENTS index
- 不再承担种子归档工作

---

## 7.3 退休并移入 `_legacy/`

以下脚本不再作为推荐路径：

- `pipeline_init.py`
- `llm_fill_drafts.py`
- `import_seeds_to_drafts.py`
- `dedupe_merge_skills.py`
- `promote_drafts.py`

处理方式：

- 移入 `scripts/_legacy/`
- 顶部加注释：`legacy experiment only; not recommended for governed workflow`
- README 不再宣传这些脚本

理由：

- 它们代表旧的“自动炼丹流水线”心智，不适合作为治理示范

---

## 8. 新增模块设计（`scripts/skillbank/`）

## 8.1 `paths.py`

职责：统一路径入口。

建议函数签名：

```python
from pathlib import Path


def repo_root() -> Path: ...
def skillbank_root() -> Path: ...
def skills_root() -> Path: ...
def seed_root() -> Path: ...
def drafts_root() -> Path: ...
def trash_root() -> Path: ...
def meta_root() -> Path: ...
def reports_root() -> Path: ...
```

---

## 8.2 `inventory.py`

职责：扫描仓库中的所有 skill-like 目录，输出统一 inventory。

建议数据结构：

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

Role = Literal["production", "seed", "draft", "trash", "unknown"]

@dataclass
class SkillEntry:
    path: Path
    rel_path: str
    role: Role
    has_skill_md: bool
    title: Optional[str]
    status_label: Optional[str]
    source_guess: Optional[str]
    has_scripts: bool
    has_references: bool
    has_assets: bool
    sensitive_hits: list[str]
    notes: list[str]
```

建议函数：

```python
def scan_skillbank() -> list[SkillEntry]: ...
def classify_role(path: Path) -> Role: ...
def read_status_label(skill_md: Path) -> str | None: ...
def extract_title(skill_md: Path) -> str | None: ...
```

---

## 8.3 `detectors.py`

职责：检测敏感信号与坏示范信号。

建议检测项：

- 邮箱
- token / password-like 值
- private/admin URL
- 私有域名
- 人名/记录人/来源人等日记痕迹
- “成功经验”“记录人”“来源人”等 diary 信号
- 店铺名/账号名等业务身份痕迹
- 环境变量中的业务密码名，如 `GENSTORE_PASSWORD`

建议数据结构：

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Finding:
    path: Path
    kind: str
    line_no: int
    excerpt: str
    severity: str   # info / warn / high
```

建议函数：

```python
def scan_text(text: str, path: Path) -> list[Finding]: ...
def scan_file(path: Path) -> list[Finding]: ...
def scan_tree(root: Path) -> list[Finding]: ...
```

---

## 8.4 `sanitize.py`

职责：基于 detector 的结果生成脱敏建议，必要时执行保守替换。

建议能力：

- `plan_sanitization(path)`：返回替换建议
- `apply_sanitization(path)`：执行安全替换
- 对不适合自动替换的内容，仅返回：`move_to_trash`

建议函数：

```python
def plan_file(path: Path) -> list[dict]: ...
def apply_file(path: Path, plan: list[dict]) -> None: ...
def can_auto_fix(finding: Finding) -> bool: ...
```

替换映射建议：

- 邮箱 → `user@example.com`
- admin URL → `https://admin.example.com/...`
- 私有店铺名 → `sample-store`
- 个人记录人 → `internal-operator`
- chat URL / conversation URL → `https://example.com/conversation/...`

---

## 8.5 `validators.py`

职责：统一 production / seed 校验逻辑。

建议数据结构：

```python
from dataclasses import dataclass

@dataclass
class ValidationIssue:
    level: str   # error / warn
    code: str
    message: str

@dataclass
class ValidationResult:
    ok: bool
    issues: list[ValidationIssue]
```

建议函数：

```python
def validate_production_skill(skill_dir: Path) -> ValidationResult: ...
def validate_seed_skill(skill_dir: Path) -> ValidationResult: ...
def validate_repo_production_tree(root: Path) -> ValidationResult: ...
```

### production 校验规则

至少包含：

- frontmatter 合法
- `name` / `description` 明确
- 单一职责
- workflow 清晰
- guardrails / gotchas 存在
- progressive disclosure 合理
- 无 TODO-heavy
- 无敏感 / diary / private-ish 内容
- 有 verification path

### seed 校验规则

至少包含：

- 有显式 status label
- status label 在约定值内：`PROMOTED` / `RAW` / `INCOMPLETE` / `SENSITIVE`
- 命中敏感信号时必须包含 `SENSITIVE`
- 不得被 AGENTS index 引入

---

## 8.6 `taxonomy.py`

职责：分类与路径合法性判断。

建议函数：

```python
def load_taxonomy(path: Path) -> dict: ...
def is_valid_production_leaf(rel_path: str, taxonomy: dict) -> bool: ...
def suggest_target_path(title: str, domain_hint: str | None = None) -> str: ...
```

---

## 8.7 `indexer.py`

职责：DocIndex 构造与注入。

建议函数：

```python
def find_leaf_paths(root: Path) -> list[str]: ...
def build_index_text(leaf_paths: list[str]) -> str: ...
def inject_index(agents_md: Path, index_text: str) -> tuple[str, bool]: ...
```

要求：

- 结果稳定排序
- 只索引 `SkillBank/skills/`
- 不索引 seed / drafts / trash

---

## 8.8 `reports.py`

职责：统一 markdown/json 报告输出。

建议函数：

```python
def write_json_report(path: Path, data: dict | list) -> None: ...
def write_markdown_report(path: Path, title: str, sections: list[dict]) -> None: ...
```

---

## 9. 新增 CLI 设计

## 9.1 `scripts/review_inventory.py`

作用：全仓盘点。

CLI：

```bash
python scripts/review_inventory.py --write
python scripts/review_inventory.py --print
```

输出：

- `reports/skillbank-inventory.json`
- `reports/skillbank-inventory.md`

字段建议：

- 路径
- 角色（production / seed / draft / trash）
- 是否有 `SKILL.md`
- status label
- sensitive hits
- source_guess
- action suggestion（keep / sanitize / retire / promote / move-to-trash）

---

## 9.2 `scripts/prune_seed_examples.py`

作用：按 allowlist 保留少量 seed 示例，其他移入 `.trash/`。

CLI：

```bash
python scripts/prune_seed_examples.py --dry-run
python scripts/prune_seed_examples.py --apply
```

配置：

- `SkillBank/meta/retained-seed-allowlist.yml`

行为：

- 只保留 allowlist 内 seed
- 其余移动到 `SkillBank/.trash/<date>-seed-prune/`

---

## 9.3 `scripts/sanitize_repo_samples.py`

作用：检查并脱敏保留下来的 seed 示例。

CLI：

```bash
python scripts/sanitize_repo_samples.py --check
python scripts/sanitize_repo_samples.py --apply
```

输出：

- `reports/sanitize-findings.json`
- `reports/sanitize-plan.md`

---

## 9.4 `scripts/validate_seed_status.py`

作用：校验 `seed_openclaw_skills/` 是否符合状态规范。

CLI：

```bash
python scripts/validate_seed_status.py
```

退出码：

- 0：全部通过
- 非 0：存在缺失状态标签 / 敏感状态不一致 / seed 结构异常

---

## 9.5 `scripts/validate_production_skills.py`

作用：校验 production tree 是否合规。

CLI：

```bash
python scripts/validate_production_skills.py
```

检查项：

- 是否存在脏路径
- 是否存在 TODO-heavy skill
- 是否存在私有/敏感/日记化内容
- 是否存在不合 taxonomy 的路径

---

## 9.6 `scripts/suggest_duplicates.py`

作用：输出重复技能建议组。

CLI：

```bash
python scripts/suggest_duplicates.py --write
python scripts/suggest_duplicates.py --print
```

输出：

- `reports/duplicate-suggestions.json`
- `reports/duplicate-suggestions.md`

重要约束：

- 不自动 merge
- 不自动 rewrite canonical

---

## 9.7 `scripts/promote_reviewed_skill.py`

作用：人工审核后的单点 promotion。

CLI：

```bash
python scripts/promote_reviewed_skill.py \
  --src SkillBank/drafts/ops/feishu/feishu-im-send-fallback \
  --dst SkillBank/skills/ops/feishu/feishu-im-send-fallback \
  --apply
```

执行流程：

1. 校验 source 存在
2. 跑 production validation
3. 跑 sensitive detector
4. 校验目标路径是否合 taxonomy
5. 若通过，则复制到 production
6. 重建 AGENTS index

---

## 9.8 `scripts/install_demo_workspace.py`

作用：向 demo/test workspace 安装治理后的 SkillBank。

CLI：

```bash
python scripts/install_demo_workspace.py --workspace ~/.openclaw/workspace_tester --dry-run
python scripts/install_demo_workspace.py --workspace ~/.openclaw/workspace_tester --apply
```

行为：

- 复制 `SkillBank/skills/` 与 `SkillBank/meta/`
- 可选复制 `seed_openclaw_skills/`
- 注入 AGENTS index
- 不归档 seed，不执行 pipeline 初始化

---

## 10. 配置文件设计

## 10.1 `SkillBank/meta/retained-seed-allowlist.yml`

建议内容：

```yaml
max_seed_examples: 8
retain:
  - feishu-doc
  - feishu-drive
  - feishu-perm
  - feishu-wiki
  - github-cli
  - image-read
  - video-read
  - image-generate
```

规则：

- 数量有限制
- 只保留通用、外部、已脱敏 skill

---

## 10.2 `SkillBank/meta/taxonomy.yml`

建议内容：

```yaml
analysis:
  finance:
    - a-stock-quick-research
coding:
  refactor:
    - safe-refactor
debugging:
  first-15-min: []
media:
  image:
    - image-read
    - image-generate
  video:
    - video-read
    - video-generate
ops:
  feishu:
    - feishu-doc
    - feishu-drive
    - feishu-perm
    - feishu-wiki
  github:
    - github-cli
misc: {}
```

用途：

- 校验路径合法性
- 约束 production 树分类风格

---

## 10.3 `SkillBank/meta/inventory.schema.json`

用途：

- 约束 `review_inventory.py` 输出结构
- 供后续 CI / tooling 读取

最低字段：

- `rel_path`
- `role`
- `has_skill_md`
- `status_label`
- `sensitive_hits`
- `suggested_action`

---

## 11. 分阶段实施计划

## Phase 0：基线盘点与冻结

目标：看清家底，不直接大拆。

任务：

1. 新建分支：`cleanup/skillbank-governance-v2`
2. 新建 `docs/` 与 `reports/`
3. 运行 inventory 草稿脚本或临时盘点脚本
4. 产出当前 inventory + sensitive findings
5. 标出：
   - 应保留 production
   - 应保留 seed
   - 应退役路径
   - 应隔离的敏感项

完成标志：

- 有一份 inventory 报告可作为后续迁移依据

---

## Phase 1：目录角色重构

目标：先把语义摆正。

任务：

1. `skill-seeds/` 退役为旧结构
2. 新建 `SkillBank/seed_openclaw_skills/`
3. 新建 `SkillBank/.trash/`
4. 将 `skills_seeded/` 评估后移除或并入 `.trash/`
5. 修订 `SkillBank/README.md`，明确三层角色

完成标志：

- 仓库中 production / seed / draft / trash 角色边界明确

---

## Phase 2：裁剪 seed 示例

目标：让 seed 回到“少量通用示例”的定位。

任务：

1. 编写 `retained-seed-allowlist.yml`
2. 将非 allowlist 项移至 `.trash/<date>-seed-prune/`
3. 对剩余 seed 逐个补 status label
4. 跑一次 sensitive scan
5. 对保留样例进行脱敏或替换

建议直接移出的典型内容：

- `genstore-operation`
- `a-stock-research`（若仍偏私有）
- `feishu-api-operation`（若仍有私有痕迹）
- 任何 workspace 私有导出
- diary-heavy / business-coupled seed

完成标志：

- `seed_openclaw_skills/` 中仅保留少量通用 seed
- 所有 seed 具备明确状态标签

---

## Phase 3：清理 production 树

目标：让 production 成为真正好示范。

任务：

1. 清理 `imported/`、`legacy/`、`superpowers-raw/` 等坏示范路径
2. 移出 `product/genstore/genstore-operation`
3. 清理重复 leaf
4. 重建 taxonomy 对应路径
5. 重写 AGENTS index

完成标志：

- production tree 无明显脏路径
- AGENTS index 只指向可信 production leaves

---

## Phase 4：脚本层治理化改造

目标：替换旧的自动炼丹思路。

任务：

1. 建立 `scripts/skillbank/` 模块层
2. 模块化 `build_agents_md_index.py`
3. 新增：
   - `review_inventory.py`
   - `prune_seed_examples.py`
   - `sanitize_repo_samples.py`
   - `validate_seed_status.py`
   - `validate_production_skills.py`
   - `suggest_duplicates.py`
   - `promote_reviewed_skill.py`
4. 将 legacy scripts 移入 `_legacy/`

完成标志：

- README 推荐命令全部切换到治理型脚本

---

## Phase 5：文档与技术规范同步

目标：避免目录改了，文档还活在旧世界。

任务：

1. 重写 `README.md`
2. 更新 `TECHNICAL_SPEC.md`：
   - 删除 pipeline-first 心智
   - 替换为 governance-first
3. 补充 `production-skill-checklist.md`
4. 补充 `seed-status-conventions.md`
5. 加入 taxonomy / allowlist / inventory schema 文档

完成标志：

- 文档与实际目录/脚本一致

---

## Phase 6：测试与验收

目标：把治理规则落成自动检查。

任务：

1. 编写：
   - `test_indexer.py`
   - `test_inventory.py`
   - `test_seed_validation.py`
   - `test_production_validation.py`
   - `test_prune_seed_examples.py`
2. 运行 `pytest -q`
3. 修复全部失败项
4. 可选增加 CI

完成标志：

- pytest 全绿
- CI 能挡住治理回退

---

## 12. 文件级改动清单

## 12.1 新建

- `docs/skillbank-governance-v2-implementation.md`
- `SkillBank/meta/production-skill-checklist.md`
- `SkillBank/meta/seed-status-conventions.md`
- `SkillBank/meta/retained-seed-allowlist.yml`
- `SkillBank/meta/taxonomy.yml`
- `SkillBank/meta/inventory.schema.json`
- `scripts/skillbank/__init__.py`
- `scripts/skillbank/paths.py`
- `scripts/skillbank/inventory.py`
- `scripts/skillbank/detectors.py`
- `scripts/skillbank/sanitize.py`
- `scripts/skillbank/validators.py`
- `scripts/skillbank/taxonomy.py`
- `scripts/skillbank/indexer.py`
- `scripts/skillbank/reports.py`
- `scripts/review_inventory.py`
- `scripts/prune_seed_examples.py`
- `scripts/sanitize_repo_samples.py`
- `scripts/validate_seed_status.py`
- `scripts/validate_production_skills.py`
- `scripts/suggest_duplicates.py`
- `scripts/promote_reviewed_skill.py`
- `scripts/install_demo_workspace.py`
- `tests/test_indexer.py`
- `tests/test_inventory.py`
- `tests/test_seed_validation.py`
- `tests/test_production_validation.py`
- `tests/test_prune_seed_examples.py`

## 12.2 重写

- `README.md`
- `TECHNICAL_SPEC.md`
- `SkillBank/README.md`
- `AGENTS.md` 中 SkillBank index 内容
- `scripts/build_agents_md_index.py`

## 12.3 迁移到 `_legacy/`

- `scripts/pipeline_init.py`
- `scripts/llm_fill_drafts.py`
- `scripts/import_seeds_to_drafts.py`
- `scripts/dedupe_merge_skills.py`
- `scripts/promote_drafts.py`

## 12.4 目录清理

- `skill-seeds/` → 退役，不再作为推荐结构
- `SkillBank/skills_seeded/` → 评估后迁入 `.trash/`
- `SkillBank/skills/` 下 imported/private/legacy leaf → 清理或迁出

---

## 13. 风险与回滚策略

## 13.1 风险

1. 误删仍有参考价值的 seed
2. 过度脱敏导致示例失去可读性
3. taxonomy 调整导致 AGENTS index 大范围变化
4. 测试覆盖不足导致旧坏路径回流

## 13.2 风险控制

1. 所有移除先移到 `.trash/`，不直接删除
2. 先 `--dry-run`，再 `--apply`
3. 任何 production path 改动后必须重建 index 并跑测试
4. 对留存 seed 逐个做人审

## 13.3 回滚

- 所有结构性迁移在单独分支完成
- `.trash/` 保留完整迁移 traceability
- 若 production tree 清理过头，可从 `.trash/` 恢复

---

## 14. 验收标准（Definition of Done）

## 14.1 仓库结构

- `SkillBank/skills/` 只剩 production-grade skill
- `SkillBank/seed_openclaw_skills/` 只剩少量通用、已脱敏 seed
- `drafts/` 数量可控，角色明确
- `.trash/` 接收退役内容，便于追溯

## 14.2 索引

- `AGENTS.md` 只索引 production leaves
- 不出现 `imported/`、`genstore-operation`、`superpowers-raw/` 等坏示范路径

## 14.3 脚本

- 推荐脚本全部是治理型脚本
- 不再推荐 bulk promote / LLM fill / auto merge canonical

## 14.4 文档

- README 与 TECHNICAL_SPEC 均体现 governance-first 路线
- meta 中存在 checklist / conventions / allowlist / taxonomy / schema

## 14.5 测试

- pytest 全绿
- 至少覆盖 index / inventory / seed validation / production validation / prune seed 四类规则

---

## 15. 推荐实施顺序（最小可用路径）

如果希望最短路径先落地，建议按以下顺序做：

### 第 1 批（止血）

1. 写入本实施文档
2. 新建 meta 治理文件
3. 清理 production index 中的坏示范路径
4. 大砍 seed 示例

### 第 2 批（立规矩）

5. 新建 inventory / validators / indexer 模块
6. 新增 `review_inventory.py`
7. 新增 `validate_seed_status.py`
8. 新增 `validate_production_skills.py`

### 第 3 批（工具化）

9. 新增 `prune_seed_examples.py`
10. 新增 `sanitize_repo_samples.py`
11. 新增 `suggest_duplicates.py`
12. 新增 `promote_reviewed_skill.py`

### 第 4 批（收口）

13. 重写 README / TECHNICAL_SPEC
14. 迁移 legacy scripts
15. 补测试和 CI

---

## 16. 最终拍板

这个仓库接下来不应该再示范“怎么把一堆 seed 自动炼成 production”。

它应该示范的是：

- 怎么给 SkillBank 分层
- 怎么让 seed 不污染 production
- 怎么让 production 小而可信
- 怎么用保守脚本做治理，而不是用激进脚本做幻觉式自动化

一句话版：

**从“自动炼丹实验仓”，改造成“SkillBank 治理示范仓”。**

这才跟这几天我们在 `workspace_coder/SkillBank` 上形成的治理方向一致。 
