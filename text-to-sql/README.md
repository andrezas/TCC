# Instalar dependências

```
pip3 install -r requirements.txt
```

# Executar Container

```
docker run -d --name 'licon-db' -p 1433:1433 -d registry.gitlab.com/lsi-ufcg/tce-ac/glassfish/modelolicon:licon_db_dev_11112024
```

# Executar Liquiabse

```
cd pyliquibase && pyliquibase update
```

# Remover Container

```
docker rm -vf licon-db
```

# Link do LICON

```
http://150.165.75.163/licon/#/cadastros-consulta/licitacao

Tipo: Admin
Usuario: admin.sistemas
Senha: LKLls4Qu0P3dwP0X

Tipo: Jurisdicionado
Usuario: 99999999998
Senha: X4kmMkelGWWAwYRO
```

# processos

- LICITACAO
  - data publicacao, data abertura, ANO, VALOR_ESTIMADO, VALOR_ADJUDICADO, LICITANTES, NATUREZA DO OBJETO, MODALIDADE DA LICITAÇÃO, FONTES DE RECURSOS
- DISPENSA
- CARONA
- CONTRATO
- INEXIGIBILIDADE

# tabelas de licitantes dos processos

LICITACAO

- LICITACAO_LICITANTE (GUARDA TODOS OS LICITANTES QUE PARTICIPAM DA LICITAÇÃO)
- VENCEDOR_LICITACAO (GUARDA TODOS OS LICITANTES QUE VENCERAM NA LICITAÇÃO E RESPECTIVAMENTE SÃO PARTICIPANTES)

DISPENSA

- DISPENSA_LICITANTE

INEXIGIBLIDADE

- INEXIGIBILIDADE_LICITANTE

CARONA

- CARONA_LICITANTE

CONTRATO

- CONTRATO_LICITANTE

SELECT ANO_LICITACAO, VALOR_ADJUDICADO, ml.NOME as MODALIDE
FROM LICITACAO l JOIN MODALIDADE_LICITACAO ml ON ml.ID_MODALIDADE_LICITACAO = l.ID_MODALIDADE_LICITACAO_NOVA;
