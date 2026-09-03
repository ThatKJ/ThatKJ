<div align="center">

# Kirtan Joshi

### `systems • open source • ai • robotics`

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=19&duration=2600&pause=900&color=58A6FF&center=true&vCenter=true&width=700&lines=Building+systems+that+observe%2C+decide%2C+and+act.;Computer+Vision+%C3%97+Systems+%C3%97+Open+Source;Turning+real+bugs+into+upstream+pull+requests.;Learning+Rust+by+contributing.;GSoC+2027+is+the+target." alt="Typing SVG" />
</a>

<br/>

<a href="https://github.com/ThatKJ">
  <img src="https://img.shields.io/badge/GitHub-ThatKJ-181717?style=flat-square&logo=github&logoColor=white" />
</a>
<a href="https://linkedin.com/in/kirtan-joshi2412">
  <img src="https://img.shields.io/badge/LinkedIn-Kirtan_Joshi-0A66C2?style=flat-square&logo=linkedin&logoColor=white" />
</a>
<a href="https://twitter.com/kirtan026832614">
  <img src="https://img.shields.io/badge/X-@kirtan026832614-000000?style=flat-square&logo=x&logoColor=white" />
</a>
<a href="mailto:kirtan120007@gmail.com">
  <img src="https://img.shields.io/badge/Email-kirtan120007%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" />
</a>

</div>

---

```text
$ whoami

Kirtan Joshi
Computer Science @ Newton School of Technology, Bangalore

I build systems that observe, decide, act —
and make it obvious when they fail.

Currently:
  → building computer-vision + control systems
  → contributing to real open-source codebases
  → going deeper into Rust, C++ and Python
  → working toward GSoC 2027
```

---

## 01 / Open Source

I'm learning large codebases the way I think they should be learned:

> **open the codebase → reproduce the bug → trace the system → change the smallest correct thing → test it → explain it upstream**

### Recent upstream work

<table>
<tr>
<td width="100%" valign="top">

### ⚡ Zed

[`zed-industries/zed#63611`](https://github.com/zed-industries/zed/pull/63611)

Fixed fallback behavior for files that have an image extension but aren't actually valid images, allowing the workspace to fall back to the editor correctly.

`Rust` `async APIs` `workspace` `image viewer` `regression tests`

</td>
</tr>

<tr>
<td width="100%" valign="top">

### 🔥 HADES CLI

[`PareekshithPalat/HADES_CLI#32`](https://github.com/PareekshithPalat/HADES_CLI/pull/32)

Restored native terminal text selection and copying by removing unnecessary global mouse capture from the TUI.

`Rust` `Ratatui` `Crossterm` `terminal behavior`

</td>
</tr>

<tr>
<td width="100%" valign="top">

### 🔥 HADES CLI

[`PareekshithPalat/HADES_CLI#30`](https://github.com/PareekshithPalat/HADES_CLI/pull/30)

Worked on cross-platform conversation import/export across HADES, ChatGPT, Claude and generic Markdown formats.

`Rust` `storage` `serialization` `CLI`

</td>
</tr>
</table>

```text
The goal isn't to collect contribution squares.

The goal is to become useful inside codebases
I didn't create.
```

**Target → Google Summer of Code 2027**

---

## 02 / Building

<table>
<tr>
<td width="50%" valign="top">

### 📡 [FSOC](https://github.com/ThatKJ/FSOC)

**Vision-based tracking and control for mobile free-space optical terminals.**

A closed-loop system built around:

`camera → detection → tracking error → controller → actuation → observation`

The project includes deterministic simulation, synthetic camera rendering, beacon detection, PID control, telemetry, benchmarking and acceptance validation.

**C++20 · OpenCV · CMake · Computer Vision · Control Systems**

</td>

<td width="50%" valign="top">

### 💸 [Margin402](https://github.com/ThatKJ/margin402)

**Outcome-underwriting infrastructure for autonomous agents.**

Instead of paying for every failed AI-service attempt, an agent buys a **verified outcome at a fixed price**.

Margin402 selects providers, makes x402 payments, verifies results, retries when necessary and manages the economics of delivering the final outcome.

**TypeScript · Next.js · Algorand · x402 · Redis**

[Live →](https://margin402.vercel.app)

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 🎓 [Next Bench](https://github.com/ThatKJ/next-bench)

**A student-first university discovery platform.**

Search institutions, explore structured education profiles, manage personal goals and keep target universities in one workspace.

**Next.js · React · TypeScript · Supabase · PostgreSQL**

[Live →](https://next-bench-dev.vercel.app)

</td>

<td width="50%" valign="top">

### ⚡ [GEC Platform](https://github.com/ThatKJ/gec-platform)

**Energy intelligence and forecasting platform.**

Built around monitoring electricity consumption, forecasting usage and surfacing where energy is being wasted.

**TypeScript · Data · Forecasting · Web**

</td>
</tr>
</table>

<details>
<summary><b>More things I've built ↓</b></summary>

<br/>

* 🎮 [**ring-escape**](https://github.com/ThatKJ/ring-escape) — timing game built in Python
* 🧠 [**awoken.in**](https://github.com/ThatKJ/awoken.in) — AI + business intelligence platform
* 🛠️ [**FolderPrettifier**](https://github.com/ThatKJ/FolderPrettifier) — lightweight developer utility
* ✈️ [**Airline Reservation System**](https://github.com/ThatKJ/Airline-Reservation-System) — reservation system project
* 🌐 [**Portfolio**](https://github.com/ThatKJ/Portfolio) — personal portfolio

</details>

---

## 03 / What I'm learning now

```rust
struct CurrentFocus {
    systems: ["Rust", "C++"],
    intelligence: ["Python", "Computer Vision", "AI"],
    engineering: [
        "reading large codebases",
        "debugging from first principles",
        "testing",
        "open-source contribution",
    ],
}
```

I'm especially interested in systems that look like this:

```text
              ┌───────────────┐
              │  PERCEPTION   │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │   DECISION    │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │ CONTROL / ACT │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │  OBSERVATION  │
              └───────┬───────┘
                      │
                      └────────────→ repeat
```

Robotics, autonomous agents and developer tooling all eventually become some version of:

**observe → reason → act → verify**

---

## 04 / Stack

<div align="center">

### Languages

<img src="https://skillicons.dev/icons?i=cpp,rust,python,ts,js,java&perline=6" />

<br/>

### Web / Backend / Data

<img src="https://skillicons.dev/icons?i=nextjs,react,nodejs,postgres,supabase,docker&perline=6" />

<br/>

### Tools

<img src="https://skillicons.dev/icons?i=git,github,vscode,linux,vercel&perline=6" />

</div>

<br/>

```text
Current systems focus → Rust + C++
Current AI focus      → Python + Computer Vision
Current OSS focus     → debugging real issues in large codebases
```

---

## 05 / GitHub

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=ThatKJ&show_icons=true&hide_border=true&theme=transparent&rank_icon=github&include_all_commits=true" />

<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=ThatKJ&layout=compact&hide_border=true&theme=transparent&langs_count=6" />

</div>

---

## 06 / How I like to build

```text
understand the problem
        │
        ▼
understand the system
        │
        ▼
build the smallest correct version
        │
        ▼
measure what actually happened
        │
        ▼
find what breaks
        │
        ▼
make the system better
        │
        └──────────────→ repeat
```

I'm not trying to collect 50 technologies.

I'm trying to get unusually good at **understanding systems I didn't write, finding where reality disagrees with the assumptions, and fixing the right layer.**

Today that shows up as:

`computer vision` · `control systems` · `AI agents` · `developer tools` · `open source`

Tomorrow, probably something harder.

---

<div align="center">

### Build things. Break assumptions. Read the source.

<sub>Computer Science · Bangalore · Systems · Open Source</sub>

<br/><br/>

<a href="https://github.com/ThatKJ?tab=repositories"><b>repositories</b></a>
  ·   <a href="https://github.com/pulls?q=is%3Apr+author%3AThatKJ"><b>pull requests</b></a>
  ·   <a href="mailto:kirtan120007@gmail.com"><b>contact</b></a>

<br/><br/>

<sub>working toward GSoC 2027</sub>

</div>
