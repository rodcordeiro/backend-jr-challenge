# Backend Jr Challenge #

Estamos acabando de desenvolver nosso novo portal de transações online da StarPay e você vai nos ajudar nessa missão!
Nessa integração, entre nosso financeiro e o Portal de Estabelecimentos, precisamos validar as transações e informar como será feito o pagamento aos estabelecimentos que realizaram a transação!

Quando a sua API receber um determinado payload (logo abaixo), você deve validar as seguintes regras.

#### Regras de negócio ####
- A data da compra não pode ser menor que o dia de hoje
- Não podem ser feitos parcelamentos maiores que 12x

Esse desafio tem como objetivo testar seu domínio sobre APIs: organização, boas práticas conhecimento em frameworks e suas tecnologias.

### Não esqueça de preencher o nosso formulário ###

* [Backend Jr](https://docs.google.com/forms/d/1lx8dFBgbKQc4HK0vyuPxX1iu61p-vKrRQPH1krGfwvU)



### Qual o objetivo? ###

* Desenvolver uma API
* Recebendo um request /POST em um recurso com nome "/transaction"
	- Sua URL deverá ficar algo como: "http://localhost:3000/transaction"
* Será enviado um payload de requisição
* A API precisa ser capaz de interpretar essa requisição
* Realizar as transformações e validações necessárias
* Devolver para o solicitante o resultado

### Payloads ###
##### Request #####
```json
{
 "nome": "Fulano da Silva",
 "cartao_credito": "5476045573597563",
 "data_compra": "2020-02-14",
 "valor_compra": 1000.00,
 "parcelamento": 4,
 "bandeira": "MASTER",
 "operacao": "CREDITO"
}
```

##### Response #####
```json
{
 "transacao_success": true,
 "cartao_credito_mascarado": "7563",
 "total_parcelas": 4,
 "pagamentos": [
 	{
		"data_pagamento": "2020-03-14",
		"valor": 237.5,
		"parcela": 1
	},
	{
		"data_pagamento": "2020-04-14",
		"valor": 237.5,
		"parcela": 2
	},
	{
		"data_pagamento": "2020-05-14",
		"valor": 237.5,
		"parcela": 3
	},
	{
		"data_pagamento": "2020-06-14",
		"valor": 237.5,
		"parcela": 4
	}
 ],
 "valor_compra": 1000,
 "valor_pagamento": 950,
 "percentual_repasse": "5%"
}
```
- Se todos os campos estiverem OK, a transação foi bem sucedida
- A quantidade de pagamentos, vai depender do total de parcelas
- Cada bandeira dá um percentual de desconto diferente, segundo a tabela:
	- MASTERCARD: 5%
	- VISA: 3%	
	- AMEX: 4.9%

### Ferramentas que devem ser utilizadas? ###

Pode ser usada a linguagem que você achar melhor, mas iremos precisar executar o seu código, então tente deixar o mais simples possível, com uma simples instrução de como rodar seu projeto.

### Como nos mandar o desafio? ###

Se tiver uma conta no GitHub, pode apenas mandar o link do repositório.

Se não conhecer Git, pode nos mandar por email.
