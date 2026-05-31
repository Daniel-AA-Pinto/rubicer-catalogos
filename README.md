# Repositório de conteúdo — Catálogos Rubicer

Este repositório alimenta a app Flutter com catálogos PDF. **Não edite `manifests/catalogs.json` à mão** — é gerado automaticamente.

## Estrutura

```
catalogs/          ← coloque aqui os PDFs
manifests/         ← manifest gerado pela GitHub Action
scripts/           ← script de geração
```

## Adicionar um catálogo

1. Copie o PDF para `catalogs/nome-do-catalogo.pdf`
2. Faça commit e push para `main`
3. A GitHub Action gera/atualiza `manifests/catalogs.json` (1–2 min)
4. Na app, puxe para atualizar a lista e toque no catálogo para transferir

## Atualizar um catálogo

Substitua o ficheiro PDF em `catalogs/` com o mesmo nome. O hash SHA-256 muda e a app re-faz o download automaticamente.

## Remover um catálogo

Apague o PDF de `catalogs/` e faça push. O manifest é atualizado e a app remove o item da lista.

## Configuração na app

Em `lib/config/app_config.dart`, defina `githubOrg` para o seu utilizador ou organização GitHub antes de publicar a app.

## Gerar manifest localmente

```bash
python3 scripts/generate_manifest.py
```
