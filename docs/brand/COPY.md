# Agent Kit — textos prontos para publicar

Tudo aqui é texto limpo, sem assinatura de ferramenta. Copie e cole. Imagens em `docs/brand/social/<en|pt>/`.

---

## Repositório (GitHub → About)

**Descrição (EN, 321 caracteres; o GitHub aceita até 350):**
> Just talk, it codes. Open-source skills and hooks that make AI coding agents (Claude Code, Codex, Cursor) follow a real plan, fix their own small mistakes without asking, and watch your CI on a lighter model. 51 skills: spec, TDD, code review, security, performance, app cloning. No slash commands, no prompt engineering.

**Descrição curta alternativa (EN, 149):**
> Just talk, it codes. Skills + hooks that make AI coding agents follow the plan, self-heal small errors and watch your CI. Claude Code, Codex, Cursor.

**Website:** `https://github.com/lucasouzadev/agent-kit-skill#readme` (ou o seu site, se tiver)

**Topics (20, o máximo do GitHub):**
`claude-code` `claude-code-plugin` `claude-skills` `agent-skills` `ai-agents` `coding-agent` `agents-md` `claude-md` `cursor` `codex` `ai-coding` `vibe-coding` `no-code` `developer-tools` `context-engineering` `self-healing` `github-actions` `tdd` `react-native` `prompt-engineering`

**Comando para aplicar tudo de uma vez** (no seu terminal, com o `gh` logado):
```bash
gh repo edit lucasouzadev/agent-kit-skill \
  --description "Just talk, it codes. Skills + hooks that make AI coding agents follow the plan, self-heal small errors and watch your CI. Claude Code, Codex, Cursor." \
  --homepage "https://github.com/lucasouzadev/agent-kit-skill#readme" \
  --add-topic claude-code,claude-code-plugin,claude-skills,agent-skills,ai-agents,coding-agent,agents-md,claude-md,cursor,codex \
  --add-topic ai-coding,vibe-coding,no-code,developer-tools,context-engineering,self-healing,github-actions,tdd,react-native,prompt-engineering
```
Se o repositório já tiver topics antigos que não quer manter, remova antes com `--remove-topic <nome>`.

**Imagem de preview (Settings → General → Social preview):** envie `docs/assets/social-preview.png` (1280×640).

---

## Bio / linha única

- **PT:** Agent Kit — só conversa, ele programa. Skills open-source que fazem agentes de IA seguirem o plano, se corrigirem sozinhos e vigiarem seu CI.
- **EN:** Agent Kit — just talk, it codes. Open-source skills that make AI coding agents follow the plan, fix themselves and watch your CI.

---

## Post de lançamento — LinkedIn (PT)

Agentes de IA escrevem código rápido. O problema é que ignoram metade das regras que a gente escreve para eles.

Criei o **Agent Kit**, um pacote open-source de skills e hooks para Claude Code, Codex e Cursor que resolve isso:

→ **Uma trilha de 9 etapas que o agente segue de verdade.** Os hooks repetem o plano a cada sessão e não deixam o agente encerrar sem provar que testou.
→ **Ele conserta a própria bagunça.** Simulador travou, cache velho, teste quebrado pela própria mudança: resolve sozinho, sem parar para perguntar.
→ **Fica de olho no seu CI.** Depois de cada push, um modelo mais leve acompanha o GitHub Actions em segundo plano e corrige o que quebrou.
→ **Sem comandos.** Na primeira mensagem ele se apresenta no seu idioma, faz uma pergunta e conduz o resto. Serve até para quem não programa.

São 51 skills, incluindo spec, TDD, code review, segurança, performance e um pacote para recriar apps do zero.

É grátis: github.com/lucasouzadev/agent-kit-skill

#IA #DesenvolvimentoDeSoftware #OpenSource #ClaudeCode #DevTools

## Launch post — LinkedIn (EN)

AI coding agents write code fast. They also ignore half the rules we give them.

I built **Agent Kit**, an open-source pack of skills and hooks for Claude Code, Codex and Cursor that fixes that:

→ **A 9-step track the agent actually follows.** Hooks repeat the plan every session and won't let the agent wrap up without proof it tested.
→ **It fixes its own mess.** Crashed simulator, stale cache, a test its own change broke: handled, without stopping to ask.
→ **It keeps an eye on your CI.** After every push, a lighter model watches GitHub Actions in the background and fixes what broke.
→ **No commands.** On the first message it introduces itself in your language, asks one question and leads the rest. Works even if you don't code.

51 skills, including spec, TDD, code review, security, performance and a pack to rebuild apps from scratch.

Free: github.com/lucasouzadev/agent-kit-skill

#AI #SoftwareEngineering #OpenSource #ClaudeCode #DevTools

---

## Thread — X / Threads (PT)

1/ Seu agente de IA lê o CLAUDE.md… e ignora metade. Fiz um kit open-source que obriga ele a seguir o plano. 🧵
2/ Uma trilha de 9 etapas: entender → planejar → seu "sim" → construir → se corrigir → verificar → vigiar o CI → fechar. Os hooks repetem isso em toda sessão.
3/ Se ele mexeu em arquivos e tentou encerrar sem provar que testou, um hook manda ele voltar. Sem prova, não acabou.
4/ Erro pequeno? Simulador travou, cache velho, teste quebrado. Ele resolve sozinho com um modelo mais leve, sem te perguntar nada.
5/ Depois do push, outro agente leve acompanha o GitHub Actions em segundo plano e corrige o que quebrou na branch.
6/ E sem comandos: na primeira mensagem ele se apresenta no seu idioma e faz uma pergunta. Você só conversa.
7/ 51 skills, grátis, para Claude Code, Codex e Cursor → github.com/lucasouzadev/agent-kit-skill

## Thread — X / Threads (EN)

1/ Your AI agent reads CLAUDE.md… and ignores half of it. I made an open-source kit that makes it follow the plan. 🧵
2/ A 9-step track: understand → plan → your "yes" → build → self-heal → verify → watch CI → close. Hooks repeat it every session.
3/ If it changed files and tries to wrap up without proof it tested, a hook sends it back. No proof, not done.
4/ Small error? Crashed simulator, stale cache, broken test. It fixes it with a lighter model, no questions asked.
5/ After the push, another light agent watches GitHub Actions in the background and fixes what broke on the branch.
6/ And no commands: on the first message it introduces itself in your language and asks one question. You just talk.
7/ 51 skills, free, for Claude Code, Codex and Cursor → github.com/lucasouzadev/agent-kit-skill

---

## Carrossel / posts — legendas (use com as imagens 01–06)

| Imagem | PT | EN |
|---|---|---|
| 01 | Você fala o que quer. Ele planeja, constrói e testa. Sem prompt, sem comando. | You say what you want. It plans, builds and tests. No prompts, no commands. |
| 02 | Na primeira mensagem ele se apresenta, faz uma pergunta e conduz o resto. Nada de decorar comandos com "/". | On the first message it introduces itself, asks one question and leads the rest. Nothing to memorize. |
| 03 | Simulador travou? Cache velho? Teste quebrado pela própria mudança? Ele resolve sozinho e só te conta depois. | Crashed simulator? Stale cache? A test its own change broke? It fixes it and tells you after. |
| 04 | Depois de cada push, um modelo mais leve acompanha seu CI em segundo plano e corrige o que quebrou. | After every push, a lighter model watches your CI in the background and fixes what broke. |
| 05 | 9 etapas, nenhuma pulada. Os hooks não deixam o agente encerrar sem provar que testou. | 9 steps, none skipped. Hooks won't let the agent wrap up without proof it tested. |
| 06 | Grátis e open source. Funciona com Claude Code, Codex e Cursor. Link na bio. | Free and open source. Works with Claude Code, Codex and Cursor. Link in bio. |

**Hashtags (escolha 5–8):** #IA #AI #OpenSource #ClaudeCode #Cursor #DevTools #Programação #NoCode #VibeCoding #GitHub
