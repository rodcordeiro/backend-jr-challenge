import requests
import json
from datetime import datetime
from decimal import Decimal


payload = json.load(open("request.txt",'r'))


##Funçoes para validar o payload
def parcelamento(parcelamento):
    if parcelamento <=12:
        return True
    else:
        return False

def parcelas(data_compra,valor_compra,desconto,parcelamento):
    valor_parcela = round(((valor_compra-(valor_compra*desconto))/parcelamento),2)
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
    		"valor": valor_parcela,
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
response={
 "transacao_success": "boolean",
 "cartao_credito_mascarado": "xxxx",
 "total_parcelas": 0,
 "pagamentos": [
 	{
		"data_pagamento": "yyyy-mm-dd",
		"valor": 000.00,
		"parcela": 0
	}
 ],
 "valor_compra": 000.00,
 "valor_pagamento": 000.00,
 "percentual_repasse": "0%"
}

def validar(payload):
    response['cartao_credito_mascarado'] = payload["cartao_credito"][-4:]
    response['total_parcelas']=payload['parcelamento']
    if bandeira(payload['bandeira']):
        response["percentual_repasse"] = f"{(bandeira(payload['bandeira'])*100)}%"
        if parcelamento(payload['parcelamento']):
            response['pagamentos']=parcelas(payload["data_compra"],payload["valor_compra"],bandeira(payload['bandeira']),payload['parcelamento'])
            response['valor_compra']=payload['valor_compra']
            response['valor_pagamento']=payload['valor_compra']-(payload['valor_compra']*bandeira(payload['bandeira']))
        else:
            return False
    else:
        return False

    response["transacao_success"] = True
    return response


print(json.dumps(validar(payload)))
