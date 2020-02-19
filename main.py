import requests
from datetime import datetime
import json
from decimal import Decimal


payload={
 "nome": "Fulano da Silva",
 "cartao_credito": "5476045573597563",
 "data_compra": "2020-02-14",
 "valor_compra": 1000.00,
 "parcelamento": 4,
 "bandeira": "MASTER",
 "operacao": "CREDITO"
}

##Funçoes para validar o payload
def parcelamento(parcelamento):
    if parcelamento <=12:
        return True
    else:
        return False
def parcelas(data_compra,valor_compra,desconto,parcelamento):
    valor = round(((valor_compra-(valor_compra*desconto))/parcelamento),2)
    parcelas = []
    date = datetime.strptime(payload['data_compra'],'%Y-%m-%d').date()
    mes = date.month
    ano = date.year
    parcela = 0
    for parcela in range(parcelamento):
        mes = mes+1
        if mes >12:
            mes =1
            ano = ano +1
        parcela = parcela +1
        parcelas.append({
    		"data_pagamento": f"{ano}-{mes}-14",
    		"valor": valor,
    		"parcela": parcela
    	})
    return parcelas

def bandeira(bandeira):
    if bandeira == "MASTER":
            return 0.05
    elif bandeira == "VISA":
            return 0.03
    elif bandeira == "AMEX":
            return 0.049
    else:
            return False


##Função que irá validar o payload
resposta={
 "transacao_success": "boolean",
 "cartao_credito_mascarado": "xxxx",
 "total_parcelas": 0,
 "pagamentos": [
 	{
		"data_pagamento": "oooo-03-14",
		"valor": 237.5,
		"parcela": 1
	}
 ],
 "valor_compra": 000.00,
 "valor_pagamento": 000.00,
 "percentual_repasse": "x%"
}

def validar(payload):
    resposta['cartao_credito_mascarado'] = payload["cartao_credito"][-4:]
    resposta['total_parcelas']=payload['parcelamento']
    if bandeira(payload['bandeira']):
        resposta["percentual_repasse"] = f"{(bandeira(payload['bandeira'])*100)}%"
        if parcelamento(payload['parcelamento']):
            resposta['pagamentos']=parcelas(payload["data_compra"],payload["valor_compra"],bandeira(payload['bandeira']),payload['parcelamento'])
            resposta['valor_compra']=payload['valor_compra']
            resposta['valor_pagamento']=payload['valor_compra']-(payload['valor_compra']*bandeira(payload['bandeira']))
        else:
            return False
    else:
        return False

    resposta["transacao_success"] = True
    return resposta


print(json.dumps(validar(payload)))
