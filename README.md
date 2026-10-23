# Escola Sabatina — Estudo da Lição (PWA)

## Publicar no GitHub Pages
1. Envie **todos** os arquivos (inclusive `data/`, `tools/` e `.github/`) para um repositório.
2. Settings → Pages → *Deploy from a branch* → `main` / `(root)`.
3. Abra `https://SEU-USUARIO.github.io/NOME-DO-REPO/` e use "Adicionar à tela inicial".

## Atualização automática
- **No app:** a cada abertura com internet ele procura o trimestre vigente no repositório Adventech/sabbath-school-lessons (pela data de hoje) e baixa a lição nova sozinho. Ao mudar de trimestre, seu progresso e grifos do anterior são arquivados e o novo começa zerado. O botão ⤓ → "Atualizar" força a busca.
- **Capas:** o workflow `.github/workflows/atualizar.yml` roda todo dia, copia as capas do CPB mais para `img/` e renova `data/licao.json`. Rode-o uma vez em *Actions → Atualizar lição e capas → Run workflow*.

## Uso offline
Toque em ⤓: baixe a lição e as versões da Bíblia (ACF, AA, NVI). Capas e versículos já vistos também ficam guardados.

## Aviso
O texto da lição pertence à Associação Geral e à CPB, assim como as capas. Verifique as condições de uso antes de divulgar publicamente.
