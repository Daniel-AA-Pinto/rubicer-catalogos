# Repositório de conteúdo — Catálogos Rubicer

Este repositório alimenta a app Flutter com catálogos PDF. **Não edite `manifests/catalogs.json` à mão** — é gerado automaticamente.

## Estrutura

```
catalogs/          ← PDFs
covers/            ← imagens de capa (mesmo nome do PDF)
manifests/         ← manifest gerado pela GitHub Action
scripts/           ← script de geração
```

## Adicionar um catálogo

1. Copie o PDF para `catalogs/nome-do-catalogo.pdf`
2. Copie a capa para `covers/nome-do-catalogo.jpg` (ou `.png`)
3. Opcional: crie `covers/nome-do-catalogo.title` com o título a mostrar na grelha
4. Faça commit e push para `main`
5. A GitHub Action gera/atualiza `manifests/catalogs.json` (1–2 min)
6. Na app, puxe para atualizar e toque na categoria

Exemplo:

```
catalogs/01.LAMINAS-RUBICER.2026.pdf
covers/01.LAMINAS-RUBICER.2026.jpg
covers/01.LAMINAS-RUBICER.2026.title   ← opcional, ex.: Lâminas
```

## Atualizar um catálogo

Substitua o PDF e/ou a capa em `catalogs/` e `covers/` com o mesmo nome. O hash SHA-256 muda e a app re-faz o download automaticamente.

## Remover um catálogo

Apague o PDF (e capa opcional) e faça push. O manifest é atualizado e a app remove o item da lista.

## Configuração na app

Em `lib/config/app_config.dart`, defina `githubOrg` para o seu utilizador ou organização GitHub.

## Gerar manifest localmente

```bash
python3 scripts/generate_manifest.py
```
