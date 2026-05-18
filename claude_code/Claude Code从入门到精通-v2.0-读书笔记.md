# Claude Code 从入门到精通 v2.0 读书笔记

> 用途：这份笔记按原书 §04 到 §10 的重点整理，目标是方便复习、备课和带别人实操。它不是逐字摘录，而是把原书里的核心建议、注意事项、团队案例和可演示流程整理成“能讲、能做、能复盘”的版本。

## 总览：这本书后半部分真正想教什么

前几章解决的是“怎么装、怎么跑第一个项目”，从 §04 开始，重点就变了：你不再只是让 Claude Code 写几行代码，而是在学习一种新的工作方式。

核心主线可以压缩成一句话：

> 把临时对话沉淀成上下文，把重复流程沉淀成自动化，把单个 AI 助手扩展成一组可协作的 Agent。

学习顺序建议：

1. 先掌握 §04 的工作流：Plan、Auto、权限、会话管理。
2. 再建立 §05 的项目记忆：CLAUDE.md 和自动记忆。
3. 接着训练 §06 的对话能力：具体描述、控制上下文、让 Claude 采访你。
4. 然后用 §07 的扩展机制固化流程：Skills、Hooks、MCP、Plugins、Slash Commands。
5. 最后进入 §08 和 §09：多 Agent 并行，以及从零做完整产品。
6. §10 是心智模型：别只优化 prompt，要构建 Context 和 Harness。

---

## §04 核心工作流：别让 Claude Code 只是“快一点的编辑器”

### 本章核心

§04 讲的是日常使用 Claude Code 的底层习惯。真正拉开效率差距的不是“Claude 会不会写代码”，而是你是否会选择正确的工作模式。

这一章要记住五件事：

- **Plan 模式**：先讨论方案，不碰代码。
- **Auto 模式**：减少审批疲劳，但保留危险操作拦截。
- **权限管理**：用 `/permissions` 把安全命令白名单化。
- **Git 工作流**：让 Claude 帮你 commit、PR、worktree 并行。
- **会话管理**：及时 `/clear`、`/compact`、`/btw`，避免上下文污染。

### 1. Plan 模式：把纠结留在动手之前

Plan 模式的本质是“只规划，不执行”。Claude 可以读文件、理解项目、提出实现方案，但不会修改文件、安装包、运行命令。

适合使用 Plan 模式的情况：

- 第一次接触一个新项目。
- 要做架构调整、重构、复杂功能。
- 你自己也不确定实现路径。
- 涉及数据库、认证、支付、部署等高风险模块。

不太需要 Plan 模式的情况：

- 改 typo。
- 补一个简单测试。
- 重复性、低风险、你已经很熟悉的操作。

推荐工作流：

1. 进入 Plan 模式：按两次 `Shift+Tab`，或使用对应的 Plan 入口。
2. 描述需求，让 Claude 先读代码并给方案。
3. 反复讨论方案，比如“第三步换成 xxx 库”“不要动数据库 schema”“先兼容旧接口”。
4. 用编辑器写最终执行指令，把确认过的约束放进去。
5. 切回执行模式，让 Claude 按计划实现。

可演示示例：

```text
请先进入 Plan 模式，不要修改任何文件。

目标：把当前项目的用户登录从邮箱密码改成 GitHub OAuth。

请先完成：
1. 阅读现有认证相关代码。
2. 找出需要修改的文件。
3. 给出迁移方案，包括数据表、API、前端入口和回滚风险。
4. 明确哪些步骤需要我确认后才能执行。
```

讲课提醒：Plan 模式不是“慢”，而是把返工前置。边写边改会浪费上下文、token 和人的注意力。

### 2. Auto 模式：更安全的自动驾驶

Claude Code 默认会对很多操作请求确认。初期这是好事，但用久之后会出现审批疲劳。原书提到内部数据里大量权限请求会被用户直接批准，这意味着用户已经不认真看提示了。

Auto 模式的目标是：低风险操作自动通过，高风险操作继续拦截。

它大致有两层防御：

- **输入层**：检测 Claude 读取到的内容里是否存在 prompt injection，比如文件里写着“忽略之前指令”。
- **输出层**：在执行操作前判断风险，低风险放行，可疑操作进入更深的评估。

Auto 模式会特别警惕这些行为：

- 范围升级：你说“清理旧分支”，Claude 却想删除远程分支。
- 凭证探索：遇到认证错误后，Claude 自己去翻环境变量和 token。
- 绕过安全检查：预检失败后改用 `--skip-verify`。
- 数据外泄：未经允许创建公开 gist、上传代码或发送敏感信息。

对比 `--dangerously-skip-permissions`：

| 方式 | 特点 | 适合场景 |
| --- | --- | --- |
| Auto 模式 | 有 AI 风险分类器，危险操作仍会拦截 | 日常开发 |
| `/permissions` 白名单 | 你明确指定哪些命令可自动执行 | 团队协作、长期项目 |
| `--dangerously-skip-permissions` | 基本跳过权限保护 | 完全隔离的沙箱或 CI |

核心建议：日常开发优先用 Auto 或 `/permissions`，不要把全权限跳过当成常规工作方式。

### 3. 权限管理：把“可以做什么”写成团队规则

`/permissions` 是更精细的权限管理方式。你可以预授权安全命令，避免每次确认。

常见白名单：

```text
npm test
npm run lint
npm run typecheck
git status
git diff
git log
```

不建议随便白名单化：

```text
rm -rf *
git push --force
git reset --hard
curl ... | bash
任何会读取 ~/.ssh、~/.aws、.env 的命令
```

团队实践：

- 把权限配置保存到 `.claude/settings.json`。
- 提交到 Git，让团队共享同一套规则。
- 初期保持严格，跑过几个项目后再逐步放宽。

可讲案例：Boris 的做法不是全开 Auto，也不是跳过权限，而是用 `/permissions` 建立细粒度白名单。这更适合团队，因为安全边界是明确、可审查、可复用的。

### 4. Git 操作：让 Claude Code 接管版本管理的低价值环节

Claude Code 不是简单帮你执行 `git` 命令，它能理解当前分支、变更文件、diff 和 commit 意图。

适合让 Claude 做的 Git 操作：

- 读 diff，总结当前改动。
- 生成 commit message。
- 执行 `git add` 和 `git commit`。
- 生成 PR 描述。
- 根据 review 意见修改代码。

示例：

```text
请查看当前 git diff，帮我总结改动，并生成一个清晰的英文 commit message。
如果改动里有明显不该提交的调试代码，请先指出，不要直接 commit。
```

Git Worktrees 是并行工作的基础。每个 worktree 是同一仓库的独立工作目录，可以在不同分支上运行不同 Claude session。

适合场景：

- 一个 session 修 bug。
- 一个 session 写测试。
- 一个 session 做 UI。
- 一个 session 做 code review。

关键原则：多个 Claude session 不要同时操作同一个分支。

### 5. Computer Use 与 Voice Mode：交互边界正在扩大

原书把 Computer Use 和 Voice Mode 放在 §04，是为了说明 Claude Code 不再只活在终端文本里。

Computer Use 的价值：

- 可以看屏幕截图。
- 可以操作 GUI。
- 适合调试 Chrome 扩展、检查 UI、处理只有后台界面的系统。

限制：

- 慢，每一步都要截图、分析、操作。
- 精细拖拽、复杂表格选择不稳定。
- 不适合实时交互或游戏测试。

Voice Mode 的价值：

- 脑暴时比打字快。
- 描述布局、空间关系和视觉需求更自然。
- 适合启动任务和快速交互。

限制：

- 嘈杂环境识别率下降。
- 长技术需求仍然建议打字。
- 最适合短指令，如“跑一下测试”“把这个函数重命名”“看看这个文件的问题”。

教学讲法：Voice 负责表达意图，Computer Use 负责操作屏幕。二者结合后，AI 编程的门槛会从“会命令行”继续下降到“能说清楚想要什么”。

### 6. 会话管理：上下文干净，输出才稳定

三个重要命令：

| 命令 | 作用 | 适合场景 |
| --- | --- | --- |
| `/clear` | 清空当前对话历史 | 换任务、跑偏重来 |
| `/compact` | 把当前对话压缩成摘要 | 长任务中途释放上下文 |
| `/btw` | 开侧链问题 | 问不相关问题，不污染主任务 |

使用原则：

- 一个会话只做一类任务。
- 换任务就 `/clear`。
- 长任务中途用 `/compact`，但要意识到压缩是有损的。
- 不相关小问题用 `/btw`。

命令速查表：

| 操作 | 命令/快捷键 | 说明 |
| --- | --- | --- |
| 进入 Plan 模式 | `Shift+Tab × 2` | 先讨论方案，不动代码 |
| 切回执行模式 | `Shift+Tab` | 从规划切回执行 |
| 打开编辑器写长 prompt | `Ctrl+G` | 用编辑器组织复杂指令 |
| 查看上下文 | `/context` | 看当前窗口还剩多少空间 |
| 恢复上次会话 | `claude --continue` | 终端关掉后继续上次会话 |
| 恢复指定会话 | `claude --resume` | 回到某个历史会话 |
| 回滚对话/代码 | `Esc × 2` / `/rewind` | 改坏了时撤回 |

会话管理和六个坑其实是一件事：它们都在提醒你，Claude Code 的质量很大程度上取决于你有没有把任务、上下文和验收边界分开。

### 7. 六个坑：本质上都是会话管理问题

**坑 1：一个会话什么都塞**

表现：修 bug、写功能、重构、写文档全在一个 session 里做。

修法：一个 session 聚焦一个任务。做完就 `/clear` 或开新窗口。

**坑 2：反复纠正，越改越偏**

表现：Claude 错了，你纠正；又错，再纠正；第三次更乱。

修法：纠正两次还不行，直接 `/clear`，用更具体的初始 prompt 重新开始。

**坑 3：看起来对就接受**

表现：代码输出很合理，但没跑测试、没打开页面、没验证边界情况。

修法：每轮改动都实际运行一次。让 Claude 也知道验证标准。

**坑 4：过度微操**

表现：每改一行都插手，最后你在用 Claude 做传统编程。

修法：关注完整任务的结果。除非明显跑偏，不要打断中间过程。

**坑 5：需求模糊**

表现：“帮我优化一下”“让页面好看点”。

修法：给可验证目标，比如“把 API 响应从 2 秒优化到 500ms 内，优先检查数据库查询和缓存”。

**坑 6：不写 CLAUDE.md**

表现：每次新会话都重新解释项目背景。

修法：进入 §05，把项目规则沉淀成 CLAUDE.md。

补一层更实用的对应关系：

| 坑 | 本质问题 | 优先用哪个工具修 |
| --- | --- | --- |
| 一个会话什么都塞 | 上下文过载 | `/clear`，新开会话 |
| 反复纠正，越改越偏 | 任务定义不清 | 重新 Plan，再执行 |
| 看起来对就接受 | 没有验证回路 | 每轮改动后跑测试/打开页面 |
| 过度微操 | 人在替 Claude 写代码 | 关注结果，不盯过程 |
| 需求模糊 | 输入质量不够 | 让 Claude 采访你，补 SPEC |
| 不写 CLAUDE.md | 没有长期记忆 | 把规则写进项目上下文 |

---

## §05 CLAUDE.md：给 AI 一张地图

### 本章核心

CLAUDE.md 是 Claude Code 每次进入项目都会读的文件。它不是项目百科，而是“你和 AI 的协作契约”。

最重要的判断标准：

> Claude 自己能从代码里读出来的，不要写；Claude 猜不到但必须遵守的，要写。

### 1. CLAUDE.md 为什么重要

没有 CLAUDE.md，Claude 像一个刚加入项目的新同事，需要自己摸索项目结构、开发命令、代码风格和常见坑。

有了 CLAUDE.md，它一进来就知道：

- 项目技术栈。
- 常用开发命令。
- 测试和 lint 怎么跑。
- 哪些文件不能动。
- 哪些历史坑不能再踩。
- 团队约定和架构边界。

原书里把它类比成“宪法”。宪法的特点不是长，而是短、原则清晰、约束明确。

### 2. 写护栏，不写手册

新手最容易把 CLAUDE.md 写成百科全书：每个目录介绍一遍，每个函数解释一遍，每个 API 参数贴进去。这样会吃掉大量上下文，反而降低 Claude 的工作质量。

应该写：

- 自定义命令。
- 与默认习惯不同的代码风格。
- 测试命令和验证方式。
- 架构决策和不可变约束。
- 开发环境里的特殊坑。
- Claude 曾经犯过、你不希望它再犯的错误。

不应该写：

- “这是一个 React 项目”这类 Claude 可从代码读出的信息。
- “写整洁代码”“遵循最佳实践”这类空话。
- 完整 API 文档。
- 每个文件的逐一说明。
- 频繁变化、需要不断同步的信息。

可直接套用的 CLAUDE.md 示例：

```md
# Project Guide

## Tech Stack
- Next.js 15 App Router + TypeScript
- Tailwind CSS
- PostgreSQL + Drizzle ORM
- Better Auth for authentication

## Commands
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`
- Type check: `pnpm typecheck`
- Lint: `pnpm lint`

## Code Style
- Use function components, not class components.
- Use Tailwind classes, do not add standalone CSS files unless asked.
- Prefer server components by default.
- Use named exports.

## Project Rules
- Do not install new dependencies without explicit approval.
- Do not edit `drizzle.config.ts` unless the task is database migration.
- After changing Drizzle schema, run `pnpm db:generate`.
- If environment variables change, restart the dev server.

## Common Pitfalls
- Better Auth session checks live in middleware. Do not duplicate them inside page components.
- API routes must use try/catch and return structured JSON errors.
```

### 3. 常见反模式

反模式 1：用 `@` 引用大文档。

问题：被 `@` 引用的文件会被完整塞进上下文。长文档每次都加载，会浪费空间。

更好的写法：

```md
遇到 FooBarError 时，阅读 `docs/troubleshooting.md` 的相关章节。
不要默认加载整个文档。
```

反模式 2：只写“永远不要做 X”。

问题：当 Claude 判断必须做 X 时，它会卡住或绕路。

更好的写法：

```md
不要使用 `--skip-verify` 绕过检查。
如果 pre-commit 失败，先修复 lint/test 错误；修不了时向用户说明原因并等待确认。
```

反模式 3：用 CLAUDE.md 解释复杂 CLI。

如果某个命令复杂到需要写几段说明，说明命令本身该被封装。

更好的做法：写一个脚本或 wrapper，让 Claude 只记住清晰入口。

```md
数据库重置请使用 `pnpm db:reset:dev`，不要手写迁移清理命令。
```

### 4. 层级结构：全局、项目、子目录

CLAUDE.md 可以分层：

| 层级 | 路径 | 放什么 |
| --- | --- | --- |
| 全局级 | `~/.claude/CLAUDE.md` | 个人通用偏好 |
| 项目级 | `./CLAUDE.md` | 项目规则，建议提交到 Git |
| 子目录级 | `./src/CLAUDE.md` | monorepo 或模块专属规则 |

使用建议：

- 全局文件放个人偏好，例如 commit message 用英文、优先 TypeScript。
- 项目文件放团队规则，必须可共享。
- 子目录文件放特定模块规则，比如前端、后端、移动端各自约束。

### 5. Auto Memory：自动记住个人偏好

除了手写 CLAUDE.md，Claude Code 还有自动记忆系统。你在对话里纠正它，例如：

```text
以后这个项目的 commit message 都用英文。
测试文件统一放在 tests 目录。
```

Claude 可能会把这些偏好保存到项目记忆里。它和 CLAUDE.md 的区别：

| 项目 | CLAUDE.md | Auto Memory |
| --- | --- | --- |
| 维护方式 | 你主动写 | Claude 自动维护 |
| 适合内容 | 团队共享规则 | 个人偏好和历史纠正 |
| 是否进 Git | 通常提交 | 通常本地保存 |
| 结构 | 有组织 | 更零散 |

最佳实践：团队规则写 CLAUDE.md，个人习惯交给 Auto Memory。

### 6. 迭代飞轮：越用越好的系统

CLAUDE.md 不应该一次写完，而应该从空文件开始，随着真实错误迭代。

推荐节奏：

1. 第一周：只写项目架构、开发命令、测试命令。
2. 第二周：把 Claude 犯过的错记录成规则。
3. 第一个月：沉淀 20 到 30 条真实护栏，输出质量明显提升。
4. 之后：定期删掉过时规则，保持精简。

团队案例：

- Boris 团队的 CLAUDE.md 大约 2500 tokens，约 100 行。
- 他们会在 code review 时让 Claude 把新规则加入 CLAUDE.md。
- Mitchell Hashimoto 给 Ghostty 搭 AI 工作流时，配置文件里的每一行都对应 Agent 过去犯过的一次错。

教学总结：

> 好的 CLAUDE.md 不是资料库，而是错误免疫系统。每踩一次坑，就给系统加一条抗体。

---

## §06 进阶对话技巧：别研究咒语，要提高信息质量

### 本章核心

Claude Code 不是搜索引擎，也不是只吃关键词的工具。你要做的不是写“神奇 prompt”，而是提供清晰目标、有效上下文和可验证标准。

### 1. 怎么说话 Claude 才听得懂

官方实践里最有用的三条：

**原则 1：具体化**

差：

```text
做个登录功能。
```

好：

```text
在 `src/auth/` 下新增 GitHub OAuth 登录。
使用 Better Auth，参考现有 Google 登录实现。
先不要改数据库 schema，除非你确认当前 user 表不够用。
```

**原则 2：指向已有模式**

差：

```text
做一个新的日历组件。
```

好：

```text
请阅读 `src/components/UserWidget.tsx` 的写法，
按照同样的组件结构、状态处理和样式风格，
新增 `CalendarWidget.tsx`。
```

**原则 3：描述症状，不要替 Claude 猜原因**

差：

```text
token 刷新逻辑有问题，帮我修。
```

好：

```text
用户 session 超时后再次登录会失败。
请检查 `src/auth/` 下的登录、token refresh 和 session middleware 流程，
先定位原因，再给修复方案。
```

为什么这么做：你猜的原因可能错，Claude 能读完整代码库，让它先定位更可靠。

### 2. Context Engineering：信息不是越多越好

Context 包括：

- 你的当前 prompt。
- 对话历史。
- CLAUDE.md。
- Claude 读过的文件。
- 你粘贴的截图。
- 命令输出、日志、网页内容。

误区：信息越多越好。

实际情况：上下文太多会让模型迷失重点。尤其在 monorepo 中，一个新会话光基础配置就可能吃掉大量 tokens。

控制上下文的做法：

- 用 `@src/utils/auth.ts` 指定关键文件，而不是让 Claude 全项目乱搜。
- UI 问题直接粘贴截图。
- 日志可以通过 pipe 输入，比如 `cat error.log | claude`。
- API 文档给 URL，不要复制整篇。
- 定期用 `/context` 查看上下文占用。
- 换任务时 `/clear`。

教学提醒：上下文管理就是给 Claude 准备“会议材料”。材料不是越厚越好，而是越相关越好。

### 3. 让 Claude 采访你

做大功能时，不要一上来写长需求。更好的方式是让 Claude 先当需求分析师。

示例：

```text
我想做一个团队周报生成工具。
请先不要写代码，先像产品经理一样采访我。
你需要问清楚目标用户、核心流程、输入输出、权限、分享方式、部署环境和成功标准。
采访完成后，把结论整理成 SPEC.md。
```

Claude 通常会问：

- 目标用户是谁？
- 核心功能有哪些？
- 是否需要登录？
- 数据从哪里来？
- 是否需要分享？
- 并发量多大？
- 部署在哪里？
- 有没有设计参考？

关键动作：采访结束后，开一个新会话，把整理好的 `SPEC.md` 喂给新 Claude 执行。

原因：采访过程会消耗大量上下文，新会话从干净 spec 开始，执行更稳定。

### 4. 把 Claude 当高级工程师提问

Claude Code 不只是写代码工具，也是代码库导航员。

你可以问：

```text
这个项目的 logging 是怎么工作的？
```

```text
如果我要新增一个 API endpoint，应该模仿哪个文件？
```

```text
请追踪 `useAuth` hook 的调用链，说明登录状态从哪里来、在哪里更新。
```

```text
`src/lib/db.ts` 和 `src/utils/database.ts` 有什么区别？为什么有两个？
```

团队案例：Boris 团队的新成员入职时，不是先读一堆可能过时的 wiki，而是直接问 Claude Code，让它基于当前代码解释系统。

### 5. 多轮对话策略

**紧密反馈循环**

不要等 Claude 写完 500 行再看。发现方向偏了，越早纠正成本越低。

**两次纠正不行，换条路**

如果你连续纠正两次 Claude 还是不理解，通常不是继续补丁式解释，而是 `/clear` 后重新写一个更好的初始 prompt。

**换任务就清上下文**

写完前端组件后去改数据库 schema，最好开新会话或 `/clear`。不同任务需要不同上下文，旧对话会变成噪音。

**用 subagent 做调研**

调研类任务，比如“看看这个库怎么用”“分析竞品实现方式”，可以交给 subagent。调研结果回到主会话，中间过程不污染主上下文。

### 6. 三个提问原则

可以把 §06 压缩成三个课堂原则：

1. **给目标**：Claude 需要知道你想达成什么。
2. **给边界**：哪些文件、技术栈、行为不能动。
3. **给验收标准**：什么情况算完成。

可复用 prompt 模板：

```text
目标：
我要实现 [具体功能]。

上下文：
- 相关文件：[文件路径]
- 可参考模式：[文件路径或已有功能]
- 技术约束：[框架/库/版本/团队规则]

边界：
- 不要修改：[文件或模块]
- 不要新增依赖，除非先说明原因并等我确认。

验收标准：
- [测试命令] 通过。
- [用户流程] 可以完成。
- 输出前请总结改了哪些文件，以及还有什么风险。
```

---

## §07 扩展能力：Skills、Hooks 与 MCP

### 本章核心

当你发现自己第三次对 Claude 说同样的话，就应该把它变成扩展能力。

三种机制的区别：

| 机制 | 本质 | 确定性 | 解决什么问题 |
| --- | --- | --- | --- |
| Skills | Markdown 指令包 | 高，但不是 100% | 教 Claude 怎么做事 |
| Hooks | 生命周期脚本 | 100% 触发 | 强制检查和自动化 |
| MCP | 外部工具连接器 | 取决于工具 | 连接数据库、API、Slack、Figma 等 |

一句话记忆：

> Skills 教方法，Hooks 立规矩，MCP 接世界。

### 1. 为什么需要扩展

如果你每天都要重复这些话：

- “提交前先跑 lint。”
- “新建组件按这个目录结构。”
- “查数据库后再回答。”
- “修 bug 先复现，再写测试，再改代码。”

说明这些内容不该继续停留在 prompt 里。它们应该被沉淀成 skill、hook、command 或 MCP。

### 2. Skills：最值得先学的扩展

Skills 是最容易上手的扩展。通常是在 `.claude/skills/` 下创建一个目录，里面放 `SKILL.md`。

两类 Skills：

| 类型 | 用途 | 例子 |
| --- | --- | --- |
| 知识型 | 告诉 Claude 项目规则 | API 规范、组件规范、代码风格 |
| 工作流型 | 告诉 Claude 按步骤做事 | 修 bug、review PR、发版 checklist |

判断标准：一件事每天做超过一次，就值得写成 skill 或 command。

示例：修 bug 工作流 skill

```md
---
name: fix-issue
description: 修复 bug 时使用，要求先复现、再定位、再测试、最后总结。
---

# Bug Fix Workflow

1. 先阅读用户提供的问题描述，不要马上改代码。
2. 找到最小复现路径，优先运行已有测试或手动复现。
3. 定位相关文件，说明根因。
4. 修改代码，保持改动范围最小。
5. 为该 bug 添加或更新测试。
6. 运行 lint、typecheck 和相关测试。
7. 输出：根因、修改文件、验证结果、剩余风险。
```

如果某个 skill 有副作用，比如发消息、创建 issue、部署，可以配置为只能手动调用，避免 Claude 自动触发。

### 3. Hooks：不是建议，是强制

CLAUDE.md 和 Skills 本质上仍然是“建议”。长对话后期或上下文压缩后，Claude 可能忘记。

Hooks 是平台层面的强制机制，在特定生命周期节点触发 shell 脚本。Claude 不能跳过。

常见 Hook：

| Hook | 触发时机 | 适合做什么 |
| --- | --- | --- |
| PreToolUse | 调用工具前 | 拦截危险操作 |
| PostToolUse | 工具调用后 | 自动格式化、跑 lint |
| PermissionDenied | 权限被拒后 | 记录、通知、替代方案 |
| PostCompact | 上下文压缩后 | 重新注入关键规则 |
| Stop | Claude 准备停下时 | 无人值守任务继续推进 |

实用案例：

- 编辑文件后自动跑 eslint。
- commit 前自动跑测试。
- 权限请求交给脚本判断，低风险自动批准。
- 上下文压缩后把关键规则重新注入。
- 批处理任务中 Claude 停下询问“是否继续”时自动继续。

示例配置：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx eslint --fix $CLAUDE_FILE_PATH"
      }
    ],
    "PostCompact": [
      {
        "matcher": "*",
        "command": "cat .claude/restore-rules.md"
      }
    ]
  }
}
```

更实用一点的写法：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "pnpm lint --fix \"$CLAUDE_FILE_PATH\""
      }
    ],
    "PermissionDenied": [
      {
        "matcher": "*",
        "command": "node scripts/log-denied-action.js"
      }
    ]
  }
}
```

教学提醒：不要强行手写复杂 hook。可以直接让 Claude 生成：

```text
Write a hook that runs eslint after every file edit.
Put the config in `.claude/settings.json`.
Explain what risk this hook introduces before editing.
```

如果要演示一个最小可用的 Hook，最常见的就是“编辑后自动格式化 + 提交前自动检查”：

```bash
# 编辑后自动修复格式
npx eslint --fix "$CLAUDE_FILE_PATH"

# 提交前做最终校验
pnpm lint && pnpm test
```

### 4. MCP：让 Claude 看到外面的世界

MCP 是 Model Context Protocol，可以把外部服务接到 Claude Code。

常见 MCP：

| MCP | 能力 | 典型用途 |
| --- | --- | --- |
| Slack MCP | 搜索、发送 Slack 消息 | 自动同步进度、回复 bug |
| GitHub MCP | 操作 repo、Issue、PR | 自动项目管理 |
| Database MCP | 查询数据库 | 不用复制 SQL 结果 |
| Figma MCP | 读取设计稿 | 从设计稿生成代码 |
| Sentry MCP | 获取线上错误 | 自动定位 bug |

团队案例：

Boris 的经典用法是接 Slack MCP。有人在 Slack 报 bug 后，Claude 可以读取描述、定位代码、尝试修复、提交 PR，再回 Slack 贴 PR 链接。这个流程把“沟通、定位、修复、反馈”串成了闭环。

常见安装命令：

```bash
# Slack
claude mcp add slack -npx -y @modelcontextprotocol/server-slack

# GitHub
claude mcp add github -npx -y @modelcontextprotocol/server-github

# 查看已安装的 MCP
claude mcp list
```

更贴近日常开发的理解：

- 需要看外部数据，就接 MCP。
- 需要自动触发固定动作，就用 Hook。
- 需要把一串步骤固化成“命令”，就用 Skill 或 Command。

### 5. Plugins：打包好的扩展包

Plugins 是 Skills、Hooks、MCP、agents 等能力的打包形式。

一个插件可能包括：

- 一个 skill：告诉 Claude 如何理解代码结构。
- 一个 hook：编辑后自动类型检查。
- 一个 MCP：连接语言服务器或外部服务。
- 一个 agent：专门做 review 或安全审计。

适合场景：团队希望一键安装一套标准工作流，而不是每个人手动配置。

### 6. Slash Commands：带预计算的快捷入口

Commands 通常放在 `.claude/commands/` 下。和 Skills 的区别是：Command 可以先运行 shell 命令，把预计算结果塞进 prompt。

选择指南：

- 需要 Claude “知道什么”：用 Skill。
- 需要 Claude “先做一串事再回答”：用 Command。

示例：`/catchup`

用途：新会话开始时，让 Claude 读取当前分支变化并恢复上下文。

可以预计算：

- 当前分支名。
- `git status`。
- 最近 commit。
- 当前 diff 摘要。

然后让 Claude 基于这些信息继续工作。

### 7. 三种扩展机制的协作

完整自动化 bug 修复流水线：

1. Slack MCP 收到 bug 报告。
2. `fix-issue` Skill 指导 Claude 按标准流程定位、复现、修复。
3. PostToolUse Hook 在每次编辑后自动格式化和跑测试。
4. GitHub MCP 创建 PR。
5. Slack MCP 回到原频道通知“已修复，PR 在这里”。

教学总结：

> 单独一个扩展是工具，组合起来才是工作流。

### 8. 扩展能力速查

| 机制 | 典型入口 | 你该怎么用 |
| --- | --- | --- |
| Skills | `.claude/skills/*/SKILL.md` | 把重复流程写成标准步骤 |
| Hooks | `.claude/settings.json` | 把关键动作变成强制执行 |
| MCP | `.mcp.json` / `claude mcp add` | 把外部系统接进来 |
| Plugins | `/plugin` | 一键安装成套能力 |
| Commands | `.claude/commands/*` | 预计算结果后再交给 Claude |

命令速查：

```bash
# 查看或安装插件
/plugin

# 安装 Slack MCP
claude mcp add slack -npx -y @modelcontextprotocol/server-slack

# 查看已安装的 MCP
claude mcp list
```

---

## §08 多 Agent 协作：从“一个 AI 助手”到“一支 AI 团队”

### 本章核心

Claude Code 最被低估的能力不是写代码快，而是可以并行。一个人只开一个 session 时，大量时间都在等 Claude 执行。多个 session 并行后，你的角色会从“亲自写”变成“分配任务、审查结果、合并产出”。

### 1. Git Worktrees：并行的基础设施

并行的前提是隔离。多个 Claude session 如果同时改同一个目录、同一个分支，很容易互相覆盖。

Git Worktree 解决这个问题：

- 同一个仓库可以有多个工作目录。
- 每个目录在不同分支上。
- 每个 Claude session 在自己的目录里工作。
- 最后通过 PR 或 merge 合并。

适合分工：

- Session A：主功能。
- Session B：测试。
- Session C：UI。
- Session D：代码审查。
- Session E：文档和部署。

实践建议：

- 从 2 个 session 开始，不要一上来开 10 个。
- 每个 session 给明确角色。
- 每个 session 一个分支。
- 每 15 到 20 分钟扫一眼进度，及时纠偏。

### 2. Subagents：给主 session 叫一个帮手

Subagent 适合当前任务里的专门子任务，比如：

- 安全审查。
- 性能分析。
- 测试补全。
- 文档总结。
- 调研第三方库。

Subagents 的核心价值不是“专业分工”，而是**独立上下文**。

主 session 的上下文很宝贵。让 subagent 去调研，可以避免把大量搜索过程、临时推理和无关文件塞进主上下文。

适合说法：

```text
Use a subagent to research how the current authentication flow works.
Return only the relevant files, data flow, and risks to the main session.
Do not modify files during research.
```

### 3. Agent Teams：让 Agent 自己协调

Agent Teams 更进一步：多个 agent 可以互相通信、分工和协调。

经典模式 1：Writer / Reviewer

1. Writer Agent 实现功能。
2. Reviewer Agent 审查代码，指出问题。
3. Writer 根据反馈修改。
4. 主人类只审最终结果。

好处：写代码的 agent 容易陷入自己的思路，reviewer 能从另一个角度发现问题。

经典模式 2：AI 版 TDD

1. Test Agent 根据需求先写测试。
2. Implementation Agent 写实现让测试通过。
3. Reviewer Agent 检查覆盖率和边界情况。

复杂任务可能走四阶段协调：

| 阶段 | 作用 |
| --- | --- |
| Research | 多个 worker 并行调研代码库 |
| Synthesis | coordinator 综合发现，生成规格 |
| Implementation | worker 按规格修改代码 |
| Verification | 验证测试、lint、功能结果 |

### 4. Fan-out：批处理的人海战术

Fan-out 适合对大量文件做同类操作，例如：

- 迁移 50 个 React 类组件到函数组件。
- 批量修复 lint 规则。
- 给一批 API route 加错误处理。
- 批量更新文档格式。

可以用非交互模式或 `/batch`。

使用 `/batch` 的典型流程：

1. 交互式规划：Claude 分析项目，列出要处理的文件。
2. 你确认计划。
3. Claude 启动多个 agent 并行处理。
4. 汇总成功和失败。
5. 你重点处理少数失败案例。

注意：Fan-out 很强，但也很容易批量制造问题。一定要先限定范围，并要求每个 agent 验证自己的改动。

### 5. 团队实际案例

Anthropic 内部团队用法：

- 数据基础设施团队：用 Claude Code 调试 Kubernetes 集群，读取日志、分析错误栈、定位根因。
- 安全团队：让 Claude 跟踪复杂控制流，生成请求从入口到数据库的调用链路。
- 营销团队：批量生成广告文案和素材变体，人类负责选择和微调。
- 法务团队：非工程师律师用 Claude Code 搭了电话树系统，并上线使用。

这些案例说明：Claude Code 的使用者不再只是工程师。只要能描述目标、判断结果，就能借助它构建工作流。

### 6. 我自己摸索出来的几条经验

- 从 2 个 session 开始，一个主任务，一个辅助任务。
- 每个 session 角色清楚，不要都做“随便什么”。
- 一切用 Git 分支隔离。
- 不要完全放羊，定期 review。
- 复杂任务先 Plan，再并行。
- 合并前一定跑测试。

可讲授总结：

> 多 Agent 不是让你少负责，而是让你从执行者变成协调者。你的核心工作变成拆任务、定义验收、审查结果。

---

## §09 从零构建一个完整产品

### 本章核心

§09 用“AI 周报助手”把前面所有能力串起来。重点不是这个项目本身，而是完整产品的构建方法。

项目目标：

> 连接 GitHub，获取本周 commits，用 AI 总结成可分享的周报页面，把原来每周半小时的工作缩短到十秒。

这个案例适合教学，因为它同时覆盖：

- 需求分析。
- Next.js 项目初始化。
- OAuth。
- API 调用。
- AI 总结。
- UI 打磨。
- Skills、MCP、Hooks。
- 部署和 CI/CD。

### 1. Phase 0：先别急着写代码

最重要的经验：不要想到产品就立刻让 Claude 写代码。

先让 Claude 采访你：

```text
我想做一个 AI 周报助手。
请先不要写代码，先采访我，帮我澄清产品需求。
你需要问清楚：
1. 目标用户是谁。
2. 核心流程是什么。
3. GitHub 数据怎么获取。
4. 周报应该包含哪些信息。
5. 是否需要登录和分享。
6. 部署在哪里。
7. 什么算第一个版本完成。

采访结束后，请整理成 `SPEC.md`。
```

`SPEC.md` 是整个项目的锚点。后续开发所有分歧都回到它。

为什么采访后要开新 session：

- 需求分析过程上下文很长。
- 执行开发需要干净上下文。
- 新 session 读取 `SPEC.md` 和 `CLAUDE.md` 就够了。

### 2. Phase 1：项目初始化

新 session 开始，创建项目骨架：

```text
根据 `SPEC.md` 初始化项目。
技术栈：Next.js 15 App Router + TypeScript + Tailwind。
先创建基础目录结构、安装必要依赖，并生成初始 CLAUDE.md。
不要实现业务功能。
```

初始化后立刻配置 CLAUDE.md：

```md
# AI Weekly Report

## Project Overview
AI-powered weekly report generator.
Connects to GitHub, summarizes weekly commits, and generates shareable report pages.

## Tech Stack
- Next.js 15 App Router + TypeScript
- Tailwind CSS
- NextAuth.js for GitHub OAuth
- Anthropic SDK for summarization

## Code Style
- Use server components by default.
- API routes live in `app/api/`.
- Prefer named exports.
- Always use try/catch in API routes.

## Testing
- Run `npm run lint` before committing.
- Test API routes with curl before building UI.
```

### 3. Phase 2：正式开发

先用 Plan 模式讨论架构：

```text
请进入 Plan 模式。
根据 SPEC.md 设计实现方案，不要修改文件。
请说明：
1. API routes 如何拆。
2. GitHub OAuth 如何接。
3. commit 数据如何获取。
4. AI 总结接口如何设计。
5. 前端页面如何拆组件。
6. 每一步如何验证。
```

确认计划后执行：

```text
Plan looks good. Now implement it step by step.
Start with GitHub OAuth, then commit fetching API, then AI summarization.
After each module, stop and show how to verify it.
```

每个模块都要验证：

| 模块 | 验证方式 |
| --- | --- |
| GitHub OAuth | 打开浏览器，确认能跳转授权并回调 |
| Commit API | 用 curl 请求 API，看是否返回真实 commits |
| AI 总结 | 用真实 commit 数据生成周报，检查是否有幻觉 |
| 页面 | 走完整流程：登录、获取、总结、分享 |

核心提醒：Claude 写代码快，验证更要快。不要让它连续写 10 个文件后才发现第二个文件就错了。

### 4. Phase 3：让它好看起来

产品开发顺序建议：

1. 先跑通最小功能。
2. 再打磨 UI。
3. 最后做响应式和细节。

UI 迭代最好用截图：

```text
这是当前页面截图。
请改善视觉层级和布局，但不要改变功能。
重点检查：
1. 主操作按钮是否明显。
2. 周报内容是否便于阅读。
3. 移动端是否可用。
4. 不要引入新的 UI 库。
```

截图反馈比文字描述更准确。Claude 能直接看到间距、颜色、层级和拥挤问题。

### 5. Phase 4：扩展能力实战

把重复流程变成 Skill：

```md
---
name: weekly-report
description: Generate a weekly GitHub report and prepare it for sharing.
---

# Weekly Report Workflow

1. Confirm the user is authenticated with GitHub.
2. Fetch commits from the current week.
3. Summarize commits into sections:
   - Shipped
   - Fixed
   - In progress
   - Risks or blockers
4. Generate a shareable report page.
5. If Slack MCP is available, ask before posting to the team channel.
6. Return the report URL and a short summary.
```

接 Slack MCP：

```text
Add a Slack MCP server so the generated report can be posted to `#team-updates`.
Use a bot token from environment variables.
Do not hardcode secrets.
```

加 Hook：

```text
Add a hook that runs lint before git commit.
If lint fails, block the commit and show the errors.
```

这样项目就从“能用”变成“有自动化工作流”。

### 6. Phase 5：部署上线

部署阶段可以让 Claude 做：

- 配置 Vercel。
- 设置环境变量 checklist。
- 创建 GitHub Actions。
- 生成 PR review 工作流。
- 部署后走完整用户流程验证。

部署验证 checklist：

- GitHub OAuth 回调 URL 正确。
- 环境变量线上可用。
- 登录流程能完成。
- commit 数据能获取。
- AI 总结接口不超时。
- 分享页面可访问。
- 错误状态有提示。

### 7. 我自己踩出来的几条经验

**经验 1：需求拆小，每次只给一步**

不要一次丢完整产品需求。先登录，再数据，再核心逻辑，再 UI，再部署。

**经验 2：先跑通最小功能**

小猫补光灯案例的重点不是技术，而是产品策略：第一个版本只有“打开 App，屏幕变白，亮度拉满”。先验证真实需求，再加色温、滑块、定时拍照。

**经验 3：验证比开发更重要**

Claude 一小时能写很多代码，不验证的话，错误会以更大成本爆发。

**经验 4：不要在一个 session 里做太多不相关的事**

推荐 session 划分：

- Session 1：项目初始化和基础架构。
- Session 2：核心后端逻辑。
- Session 3：前端页面和交互。
- Session 4：测试和 bug 修复。
- Session 5：部署和 CI/CD。

**经验 5：产品感知才是最大杠杆**

Claude Code 可以帮你写代码、调 UI、配部署，但不能替你判断：

- 目标用户是谁。
- 解决什么真实问题。
- 哪些功能必须做。
- 哪些功能应该砍。
- 什么体验才算好。

### 8. 我踩过的坑，你别踩了

| 陷阱 | 表现 | 解决方案 |
| --- | --- | --- |
| 需求膨胀 | 做着做着不断加功能 | 回到 SPEC.md，不在规格内的放 todo |
| 上下文污染 | session 变长后 Claude 开始忘结构 | 及时开新 session |
| 不验证就继续 | 连续生成很多文件，后面才发现前面错 | 每完成一个模块立即验证 |
| 环境变量混乱 | 本地能跑，部署后 undefined | CLAUDE.md 写清变量，部署前 checklist |
| 过度依赖 AI 判断 | Claude 说“最好”就采纳 | AI 给方案，人做决策 |

---

## §10 心智模型与持续进化

### 本章核心

工具会变，命令会变，但协作模型不会很快过时。§10 最重要的一句话：

> 把时间花在构建 Context 和 Harness 上，而不是反复优化 Prompt。

### 1. 三层模型：你的时间该花在哪

Claude Code 的能力可以分成三层：

| 层次 | 是什么 | 回报 |
| --- | --- | --- |
| Prompt | 你每次输入的话 | 一次性回报 |
| Context | Claude 进入任务前已经看到的信息 | 复利回报 |
| Harness | 自动化环境和工具链 | 指数回报 |

把它翻成更直白的话：

| 层次 | 你在做什么 | 最值得投入的东西 |
| --- | --- | --- |
| Prompt | 临时对话 | 表达清楚目标 |
| Context | 长期记忆 | CLAUDE.md、SPEC.md、项目规则 |
| Harness | 固化流程 | Skills、Hooks、MCP、CI/CD |

Prompt 层：

- “帮我修这个 bug。”
- “加一个登录页。”
- “优化这个组件。”

Context 层：

- CLAUDE.md。
- SPEC.md。
- 项目文件结构。
- Git 状态。
- 测试命令。
- 历史规则。

Harness 层：

- Skills。
- Hooks。
- MCP。
- Agent Teams。
- 自动化 CI/CD。
- 定时任务。

比喻：

> Prompt 是你开口说话，Context 是你提前准备好的材料，Harness 是你搭好的舞台。

初学者常把时间都花在 Prompt 层。高手会把重复信息沉淀到 Context，把重复动作沉淀到 Harness。

再补一句实战版：

> 如果一个问题每周都会出现，就不要再把它留在 Prompt 层。

### 2. 引擎盖下的 Claude Code

理解内部机制不是为了炫技，而是为了更好协作。

Claude Code 的核心循环是 TAOR：

1. Think：思考当前状态。
2. Act：调用工具执行动作。
3. Observe：观察工具返回结果。
4. Repeat：没完成就继续循环。

这解释了几个常见现象：

- Claude 有时“绕路”，因为它是在边观察边调整，不是一次性执行脚本。
- 需求模糊时，它不知道停止条件，就会改来改去。
- 给明确验证标准可以让循环更快收敛。

示例停止条件：

```text
完成标准：
1. `npm test` 通过。
2. 登录流程在浏览器里可完成。
3. 不修改数据库 schema。
完成后停止，不要继续做额外优化。
```

Claude Code 的能力可以抽象成四个原语：

| 原语 | 典型工具 |
| --- | --- |
| Read | Read、Grep、Glob |
| Write | Edit、Write |
| Execute | Bash |
| Connect | MCP、WebFetch |

Bash 是万能适配器，所以 Claude Code 能适配几乎任何技术栈。

### 3. 上下文压缩：为什么长对话会“遗忘”

长会话快满时，系统会把历史压缩成摘要。压缩是有损的。

会丢失的通常是：

- 具体措辞。
- 早期边角要求。
- 语气里的暗示。
- 中间推理细节。

多次压缩后，早期信息会越来越模糊。

应对方式：

- 关键规则写入 CLAUDE.md。
- 关键需求写入 SPEC.md。
- 长任务中途让 Claude 总结当前状态。
- 换阶段开新 session。
- 用 PostCompact Hook 重新注入关键规则。

### 4. 权限系统：不只是 Yes/No

Auto 模式不是简单全放行。系统会把操作风险分为 LOW、MEDIUM、HIGH。

一般规律：

- 读文件通常低风险。
- 写配置文件可能中高风险。
- 删除、推送、读取敏感路径高风险。

一些敏感文件会被额外保护，例如：

- `.gitconfig`
- `.bashrc`
- `.zshrc`
- `~/.ssh`
- `~/.aws/credentials`

权限提示中的解释可能是实时生成的，所以每次措辞会不同。这不是不稳定，而是系统在针对当前操作解释风险。

配合会话管理时，最实用的顺序通常是：

1. 先用 Plan 模式确认边界。
2. 再用 `/permissions` 白名单掉安全命令。
3. 然后用 Auto 模式执行日常任务。
4. 任务切换时 `/clear`。
5. 每个模块跑完立刻验证。

### 5. 自动记忆维护

Claude Code 会整理记忆文件，过程大致包括：

1. 审阅现有内容。
2. 提取新的有用信息。
3. 合并重复条目。
4. 修剪过长部分。

长期使用后，你会感觉 Claude 越来越懂你。原因不只是模型更聪明，而是你的偏好、规则和项目上下文被逐步沉淀了。

### 6. 身份在变：从写代码到构建产品

原书里最重要的心智转变：

> 你的工作重心正在从“怎么写”变成“写什么”。

Claude Code 能解决大量“怎么实现”的问题，但不能替你完全决定：

- 产品方向。
- 用户需求。
- 核心体验。
- 功能取舍。
- 质量标准。

代码能力仍然重要，但重要性从“亲手写每一行”转向：

- 能否说清楚需求。
- 能否判断架构方案。
- 能否 review 输出质量。
- 能否设计验证方式。
- 能否定义产品体验。

### 7. 持续进化：怎么跟上更新

原书提醒：Claude Code 迭代很快，具体命令可能几个月后就变。

不要试图追踪每个小更新。更值得关注的是方向：

1. 自主性持续增强：从逐步指令到自主规划执行。
2. 上下文窗口持续扩大：Claude 能看到更大的项目。
3. 协作模式持续丰富：从单 Agent 到 Subagents 到 Agent Teams。

学习策略：

- 每月花 30 分钟看一次 changelog。
- 关注官方最佳实践，而不是零散技巧。
- 把时间花在构建真实项目上。
- 遇到卡点再回头查手册。

### 8. 最后的复习清单

如果只记 10 条：

1. 复杂任务先 Plan，再执行。
2. 日常开发用 Auto 或 `/permissions`，不要默认跳过所有权限。
3. 一个 session 只做一类任务。
4. 换任务就 `/clear`。
5. CLAUDE.md 写护栏，不写百科。
6. Claude 犯过的错，要沉淀成规则。
7. 大功能先让 Claude 采访你，生成 SPEC.md。
8. 每完成一个模块就验证。
9. 重复三次的流程，要变成 Skill、Hook、Command 或 MCP。
10. 你的核心价值从写代码转向定义目标、拆任务、审结果和做产品判断。

---

## 附录：教学用演示脚本

### 演示 1：Plan 模式拆一个功能

```text
请进入 Plan 模式，不要修改文件。

我要给当前项目增加“导出 PDF”功能。
请先阅读相关页面和 API，提出实现方案。
要求：
1. 不新增付费依赖。
2. 先支持服务端生成。
3. 说明哪些文件要改。
4. 给出验证方式。
```

讲解点：先让 Claude 思考方案，人类负责约束和取舍。

### 演示 2：把错误沉淀到 CLAUDE.md

```text
你刚才忘了在修改 schema 后运行类型生成。
请把这条经验整理成一条简短规则，加入 CLAUDE.md。
要求：
1. 只写 Claude 下次需要记住的规则。
2. 不要写长解释。
3. 放在 Common Pitfalls 下。
```

讲解点：每次纠正都应该变成系统记忆。

### 演示 3：让 Claude 采访你

```text
我想做一个课程报名小工具。
先不要写代码，请采访我。
你的目标是把模糊想法整理成 SPEC.md。
采访完成前不要给实现方案。
```

讲解点：先把需求质量提高，再进入开发。

### 演示 4：上下文管理

```text
请总结当前任务状态，包括：
1. 已完成什么。
2. 还剩什么。
3. 关键文件。
4. 下一步建议。

总结后我会开新 session 继续。
```

讲解点：长对话不要硬撑，阶段性总结再切新会话。

### 演示 5：Writer / Reviewer 多 Agent 思路

```text
请把任务分成两个角色：
1. Writer：实现功能。
2. Reviewer：只审查 Writer 的输出，不直接改代码。

需求：给订单列表增加状态筛选。
要求 Writer 完成后，Reviewer 从正确性、边界情况、测试覆盖和代码风格四方面 review。
```

讲解点：多 Agent 的价值是分工和相互校验，不是盲目堆数量。
