# Editando Superset

Esse arquivo serve para demonstrar como fazer edições no superset.
Recomendo ler antes o arquivo "CONTRIBUTIND.md" para saber como setar seu ambiente de desenvolvimento.

## incubator-superset

* [IN-798](https://github.com/facilit/incubator-superset/commit/e6c6a310c0e2447bd14e0898a04dd3654a837ef8): no arquivo `superset/views/core.py`, é feito os principais 
roteamentos da aplicação. Boa parte das funções em python que são chamadas ao entrar em uma página se encontram lá.
Como exemplo e também para deixar registrado, a função `dashboard()` é chamada ao entrar em um endereço de um dashboard, e é nela que é feita o tratamento atual
para fazer acessos em dashboards publicados selecionados, além do redirecionamento caso o usuário acesse um dashboard que não existe ou que não tenha acesso.
Este chamado também é responsável por acrescentar suporte a JS nas paginas de dashboards do superset. A forma que funciona é que é inserido no HTML de todos os dashboards
um link de um Google Tag Manager, e lá é feito a configuração do JS. Ambas as soluções não são ideais, e é possível explorar jeitos melhores no futuro


## superset-ui

* [IN-777](https://github.com/facilit/superset-ui/commit/ddffa2f0d8f81699c9612379ff532ad5eb3fd3f7): no arquivo `plugins/legacy-plugin-chart-country-map/src/CountryMap.js`, é feito a configuração do chart CountryMap. Esse commit serve de exemplo para mostrar como inserir um mapa novo no chart.

* [chore: removing metric from country map](https://github.com/facilit/superset-ui/commit/069cf44849deee27d735ccb9cac066aed0f565ae): este commit mostra como fazer com que a métrica não apareça nos CountryMap. Essa mudança afeta o superset à nivel geral, então todos os Country Maps ficam sem a métrica.

* [chore: changing country map's default background color](https://github.com/facilit/superset-ui/commit/fe8a8eaad942d22f0e375fee781010716ef68edb): este commit mostra como mudar a cor de fundo de areas não pintadas no Country Map.

# Tutoriais

## Sumário

- [Adicionando novo mapa](#adicionando-novo-mapa)


### Adicionando novo mapa

1. Gere um arquivo do tipo .geojson do mapa selecionado. Cada região do mapa deve ter atrelado um código chamado 'ISO' de formato AA-000. Por exemplo, no Brasil, temos que o ISO dos estados são de BR-001 a BR-026.
2. No repositório `superset-ui`, adicionar dentro do diretório `plugins/legacy-plugin-chart-country-map/src/countries/` o arquivo gerado.
3. No arquivo `plugins/legacy-plugin-chart-country-map/src/countries.js`, adicionar linha de import para o arquivo adicionado, na forma `import <nome_país> from 'file-loader!./countries/<nome_país>.geojson'`;
4. No mesmo arquivo, adicionar `<nome_país>` no array `countries`.

### Adicionando novo arquivo à aplicação

* No repositório `git-facilit`, no arquivo `superset/app.py`, basta dar import dentro da função `init_views` no arquivo desejado.


#A parte de gerar um mapa está desatualizada!
