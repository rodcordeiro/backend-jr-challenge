# -*-coding: utf-8 -*-

import flask
from flask import request, jsonify
import json
from datetime import datetime
from datetime import date
from decimal import Decimal

payload = {
 "nome": "Fulano da Silva",
 "cartao_credito": "5476045573597563",
 "data_compra": "2020-02-14",
 "valor_compra": 1000.00,
 "parcelamento": 4,
 "bandeira": "MASTER",
 "operacao": "CREDITO"
}


def parcelamento(parcelamento):
    if parcelamento <=12:
        return True
    else:
        return False

def parcelas(data_compra,valor_compra,desconto,parcelamento):
    valor_parcela = round(((valor_compra-(valor_compra*desconto))/parcelamento),2)
    parcelas = []
    data = datetime.strptime(payload['data_compra'],'%Y-%m-%d').date()
    mes = data.month
    ano = data.year
    parcela = 0
    for parcela in range(parcelamento):
        mes = mes+1
        if mes >12:
            mes =1
            ano = ano +1
        parcela = parcela +1
        parcelas.append({
    		"data_pagamento": f"{ano}-{mes}-{data.day}",
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
    erro = ''
    today = date.today()
    data = datetime.strptime(payload['data_compra'],'%Y-%m-%d').date()
    if data < today:
        erro ='Data de compra menor que data atual'
    response['cartao_credito_mascarado'] = payload["cartao_credito"][-4:]
    response['total_parcelas']=payload['parcelamento']
    if bandeira(payload['bandeira']):
        response["percentual_repasse"] = f"{(bandeira(payload['bandeira'])*100)}%"
        if parcelamento(payload['parcelamento']):
            response['pagamentos']=parcelas(payload["data_compra"],payload["valor_compra"],bandeira(payload['bandeira']),payload['parcelamento'])
            response['valor_compra']=payload['valor_compra']
            response['valor_pagamento']=round(payload['valor_compra']-(payload['valor_compra']*bandeira(payload['bandeira'])),2)
        else:
            erro = 'Parcelamento maior que 12x'
    else:
        return False

    response["transacao_success"] = True
    if erro:
        return erro
    else:
        return response




app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/',methods = ['GET'])
def home():
    return """
    <h1>Olá, bem vindo a minha API de transações.</h1>
    <p>
        Esta API foi desenvolvida para validação de transações financeiras efetuadas por cartão de crédito ou débito. Preencha os dados da transação abaixo para validar.
    </p>
    <form action='/transaction' method='post'>
        <input name='nome' type='text' placeholder='Insira aqui o nome'><br>
        <input name='cartao' type='text' placeholder='Insira o número do cartão'><br>
        <input type='date' name='data'><br>
        <input type='number' step='0.01' min='0.01' name='valor' placeholder='Qual o valor da compra'><br>
        <input type='number' name='parcelamento' placeholder='Total de parcelas'><br>
        <select name='bandeira'>
            <option>MASTER</option>
            <option>VISA</option>
            <option>AMEX</option>
        </select><br>
        <input type='text' name='operacao' placeholder='CREDITO ou DEBITO'>
        <input type='submit'>
    </form>
    """

@app.route('/transaction',methods = ['GET'])
def homeII():
    return """
    <h1>Olá, bem vindo a minha API de transaçõe>
    <p>
        Esta API foi desenvolvida para validaçã>
    </p>
    <form action='/transaction' method='post'>
        <input name='nome' type='text' placehol>
        <input name='cartao' type='text' placeh>
        <input type='date' name='data'><br>
        <input type='number' step='0.01' min='0>
        <input type='number' name='parcelamento>
        <select name='bandeira'>
            <option>MASTER</option>
            <option>VISA</option>
            <option>AMEX</option>
        </select><br>
        <input type='text' name='operacao' plac>
        <input type='submit'>
    </form>
    """

@app.route('/transaction',methods=['POST'])
def transacao():
    dads = {
     "nome": "Fulano da Silva",
     "cartao_credito": "5476045573597563",
     "data_compra": "2020-02-14",
     "valor_compra": 1000.00,
     "parcelamento": 4,
     "bandeira": "MASTER",
     "operacao": "CREDITO"
    }

    payload['nome'] = request.form['nome']
    payload['cartao_credito'] = request.form['cartao']
    payload['data_compra'] = str(request.form['data'])
    payload['valor_compra'] = float(request.form['valor'])
    payload['parcelamento'] = int(request.form['parcelamento'])
    payload['bandeira'] = request.form['bandeira']
    payload['operacao'] = request.form['operacao']
    return validar(payload)



app.run()
