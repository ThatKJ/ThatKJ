<img src="assets/hero.svg" width="100%" alt="Kirtan Joshi (@ThatKJ), Bangalore. I build software that has to work outside the demo. Now building Awoken, AI follow-up for real-estate sales teams.">

<p>
<a href="https://awoken.in"><b>awoken.in</b></a>&emsp;
<a href="https://linkedin.com/in/kirtan-joshi2412"><b>LinkedIn</b></a>&emsp;
<a href="mailto:kirtan120007@gmail.com"><b>Email</b></a>&emsp;
<a href="https://x.com/kirtan026832614"><b>X</b></a>&emsp;
<a href="https://github.com/search?q=author%3AThatKJ+is%3Apr+-user%3AThatKJ&type=pullrequests"><b>Pull requests</b></a>
</p>

CS student at Newton School of Technology. I take ideas from a rough sketch to something people can run, then check whether it actually works. Recent work has taken me from a C++ camera-control loop to AI agents that pay for outcomes over x402 to Rust terminal internals.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-work-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/h-work-light.svg">
  <img src="assets/h-work-dark.svg" width="100%" alt="Selected work">
</picture>

<p>
<a href="https://awoken.in"><img src="assets/card-awoken.svg" width="49%" alt="Awoken, early-stage venture. AI follow-up that brings unanswered real-estate leads back over WhatsApp, then hands warm buyers to sales. Next.js, TypeScript, Supabase."></a>
<a href="https://margin402.vercel.app"><img src="assets/card-margin402.svg" width="49%" alt="Margin402, hackathon prototype. An agent pays one fixed price for a verified result instead of paying for every failed attempt. Testnet run: contract $1.20, spent $1.28, $0.08 absorbed, verified 8 of 8 tests."></a>
<a href="https://github.com/ThatKJ/FSOC"><img src="assets/card-fsoc.svg" width="49%" alt="FSOC, simulation for Smart India Hackathon 2026. Camera-only pointing for a moving optical terminal in C++20. Simulated RMS pointing error falls from 6.45 degrees open loop to 0.55 degrees closed loop."></a>
<a href="https://gec-platform.vercel.app"><img src="assets/card-gec.svg" width="49%" alt="GEC Platform, interactive explainer. An ESP32 energy-monitoring rig explained through interactive 3D scenes, waveforms and a schematic."></a>
</p>

<sub>Source: <a href="https://github.com/ThatKJ/margin402">margin402</a>, <a href="https://github.com/ThatKJ/FSOC">FSOC</a>, <a href="https://github.com/ThatKJ/gec-platform">gec-platform</a>. FSOC was built with Team IRODOV for ISRO's SIH26169 problem statement; its numbers are recorded simulation results, and <a href="https://github.com/ThatKJ/FSOC#measured-results">the repo documents the tradeoffs</a>. Margin402's provider market is simulated; its payments are real Algorand Testnet transactions.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-oss-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/h-oss-light.svg">
  <img src="assets/h-oss-dark.svg" width="100%" alt="Open source: 3 merged, 2 open">
</picture>

<a href="https://github.com/search?q=author%3AThatKJ+is%3Apr+-user%3AThatKJ&type=pullrequests"><img src="assets/oss.svg" width="100%" alt="Merged: HADES CLI #32 (Rust), restored native text selection by removing global mouse capture. HADES CLI #30 (Rust), conversation import and export. awesome-ai-apps #317 (Python), closed a credentialed wildcard CORS hole. Open: Node.js #66376 (C++), backport of two V8 fixes for a WebAssembly wrapper lifetime race. LLMVault #44 (Python), brute-force guard for flag submissions."></a>

<details>
<summary><b>What changed in each pull request</b></summary>
<br>

**[HADES CLI #32](https://github.com/PareekshithPalat/HADES_CLI/pull/32)** (merged). The TUI enabled global mouse capture at startup even though every interaction is keyboard-driven, so terminals sent drags to the app instead of selecting text. Removed the capture on init and kept the cleanup on exit. Ratatui, Crossterm.

**[HADES CLI #30](https://github.com/PareekshithPalat/HADES_CLI/pull/30)** (merged). Added `/export` and `/import`. Exports Markdown or JSON; imports HADES exports, ChatGPT `conversations.json`, Claude transcripts and generic Markdown with format detection, then restores them into the active context. Spans the storage, core and TUI crates.

**[awesome-ai-apps #317](https://github.com/Arindam200/awesome-ai-apps/pull/317)** (merged). A FastAPI service paired a wildcard CORS origin with `allow_credentials=True`. Origins now come from an explicit allow-list that fails closed when unset, with regression tests for the edge cases raised in review.

**[Node.js #66376](https://github.com/nodejs/node/pull/66376)** (open). Backports two V8 fixes to `v24.x-staging`: a wrapper already marked as dying could be re-added to a `WasmCodeRefScope`, tripping a JIT allocation `CHECK`. An independent tester reported 0 crashes in 191 repro runs with the patch, versus 8 in 149 without.

**[LLMVault #44](https://github.com/CyberSunil/LLMVault/pull/44)** (open). Per-player, per-challenge attempt tracking, a 30-second cooldown after five misses, and HTTP 429 with `retry_after`. 19 tests.

</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-more-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/h-more-light.svg">
  <img src="assets/h-more-dark.svg" width="100%" alt="Other builds">
</picture>

| Project | What it is | Stack |
|---|---|---|
| [ChallanCheck](https://github.com/ThatKJ/challancheck) | Checks whether a traffic e-challan's photo actually shows the cited violation. A vision API observes; deterministic rules decide. | JavaScript, AWS Lambda, Rekognition |
| [Beacontra](https://github.com/ThatKJ/Beacontra) | Ranks marketplace listings for brand review by combining price, seller and reverse-image evidence. | TypeScript, SerpApi |
| [Intervu](https://github.com/ThatKJ/team-vector) | Adaptive interview engine: each answer updates a model of what the candidate knows and picks the next question. 48-hour team build. | Next.js, TypeScript, Supabase |
| [ring-escape](https://github.com/ThatKJ/ring-escape) | Arcade game: rotate concentric rings to guide a ball out of the maze. | Python, Pygame |
| [Portfolio](https://portfolio-kirtan.vercel.app) | Personal site. | React, Vite, Framer Motion |
| [FolderPrettifier](https://github.com/ThatKJ/FolderPrettifier) | Sorts a messy folder by file type without overwriting duplicates. | Python |
| [Airline Reservation System](https://github.com/ThatKJ/Airline-Reservation-System) | Terminal booking system with user and admin roles. School group project. | Python, MySQL |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-tools-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/h-tools-light.svg">
  <img src="assets/h-tools-dark.svg" width="100%" alt="Toolbox">
</picture>

<img src="assets/toolbox.svg" width="100%" alt="Languages: TypeScript, Python, C++, JavaScript, Rust. Product: Next.js, React, Tailwind, Three.js, Framer Motion. Vision: OpenCV DNN, ONNX, CMake. Data and infra: Supabase, PostgreSQL, Redis, MySQL, AWS Lambda. Agents and payments: x402, Algorand.">

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/h-how-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/h-how-light.svg">
  <img src="assets/h-how-dark.svg" width="100%" alt="How I work">
</picture>

<img src="assets/how.svg" width="100%" alt="Understand the problem, build the smallest useful version, test it against reality, fix the right layer, and repeat.">

That's why FSOC publishes its counterexamples next to its best numbers, Margin402 has a "what is real vs. simulated" table, and my pull requests start with the root cause.

<br>

<a href="mailto:kirtan120007@gmail.com"><img src="assets/footer.svg" width="100%" alt="Building something that has to work outside the demo? I'd like to hear about it. kirtan120007@gmail.com"></a>
