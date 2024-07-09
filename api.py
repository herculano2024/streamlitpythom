import streamlit as st
import requests
from streamlit.components.v1 import html

def get_token(api_key, client_id, client_secret):
    url = f"https://api.godigibee.io/pipeline/braskem/v1/api-token?apikey={api_key}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'token-oauth',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        st.error(f"Falha ao obter o token. Status Code: {response.status_code}, Response: {response.text}")
        return None

def consulta_pedagio(api_key, token, cnpj, doc_transporte):
    url = f"https://api.godigibee.io/pipeline/braskem/v1/consulta-pedagio?apikey={api_key}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'CNPJ': cnpj,
        'DOC_TRANSPORTE': doc_transporte
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return response.json()

def format_result(data):
    valor_total_pedagio = data.get('ValorTotalPed')
    if valor_total_pedagio is not None:
        valor_total_pedagio = f"R$ {float(valor_total_pedagio):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    return f"""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
        }}
        .blue-bg {{
            background-color: #0056b3;
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .gray-bg {{
            background-color: #f8f9fa;
            text-align: center;
            padding: 20px;
            border-radius: 8px;
        }}
        .centered {{
            text-align: center;
            padding: 20px;
        }}
        .label-title {{
            color: black;
            font-weight: bold;
        }}
        .value-title {{
            color: #0056b3;
            font-weight: bold;
        }}
        .card-header {{
            background-color: #343a40;
            color: white;
            border-radius: 8px 8px 0 0;
        }}
        .list-group-item {{
            font-size: 16px;
            line-height: 1.5;
        }}
    </style>
    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-md-6 offset-md-3">
                <div class="card blue-bg">
                    <div class="card-body">
                        <div class="container gray-bg centered">
                            <div class="row">
                                <div class="col">
                                    <h5 class="label-title">Total do Pedágio</h5>
                                    <h5 class="value-title" id="valorTotalPed">{valor_total_pedagio}</h5>
                                </div>
                                <div class="col">
                                    <h5 class="label-title">Número de Eixos</h5>
                                    <h5 class="value-title">{data.get('NumeroEixos')}</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        Detalhes do Pedágio
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item"><strong>Data de Criação:</strong> {data.get('DataCriacao')}</li>
                            <li class="list-group-item"><strong>Número da Nota Fiscal:</strong> {data.get('NumeroNotaFiscal')}</li>
                            <li class="list-group-item"><strong>Número do Transporte:</strong> {data.get('NumeroTransporte')}</li>
                            <li class="list-group-item"><strong>Placa do Cavalo:</strong> {data.get('PlacaCavalo')}</li>
                            <li class="list-group-item"><strong>Pedido Vale Pedágio:</strong> {data.get('PedidoValePed')}</li>
                            <li class="list-group-item"><strong>Número do Vale Pedágio:</strong> {data.get('NumeroValePed')}</li>
                            <li class="list-group-item"><strong>Quantidade de Cupons:</strong> {data.get('QtdeCupons')}</li>
                            <li class="list-group-item"><strong>Itinerário:</strong> {data.get('Itinerario')}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-md-12 text-center">
                <button onclick="copyToClipboard()" class="btn btn-primary">Copiar Total do Pedágio</button>
                <p id="copyMessage" style="display:none;">Valor copiado</p>
            </div>
        </div>
    </div>
    <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("valorTotalPed").innerText;
            navigator.clipboard.writeText(copyText).then(function() {{
                var copyMessage = document.getElementById("copyMessage");
                copyMessage.style.display = "block";
                setTimeout(function() {{
                    copyMessage.style.display = "none";
                }}, 2000);
            }}, function(err) {{
                console.error('Failed to copy text: ', err);
            }});
        }}
    </script>
    """

def main():
    st.title("Consulta de Pedágio - Braskem")

    cnpj_options = [
        '17799438001156',
        '17799438000346',
        '17799438000508',
        '17799438000184',
        '17799438001318'
    ]
    cnpj = st.selectbox('Selecione o CNPJ', cnpj_options)
    doc_transporte = st.text_input('DOC_TRANSPORTE')

    if st.button('Consultar'):
        if not cnpj or not doc_transporte:
            st.error("Por favor, preencha todos os campos.")
            return

        api_key = '0zNDZtPILsLDslv04FCnNkjRIpiWBkFi'
        client_id = '0zNDZtPILsLDslv04FCnNkjRIpiWBkFi'
        client_secret = '0zNDZtPILsLDslv04FCnNkjRIpiWBkFi'

        token = get_token(api_key, client_id, client_secret)
        if not token:
            return

        st.success("Token obtido com sucesso!")

        result = consulta_pedagio(api_key, token, cnpj, doc_transporte)
        if 'error' in result:
            st.error(result['error'])
        else:
            formatted_result = format_result(result.get('body', {}))
            html(formatted_result, height=800)

if __name__ == '__main__':
    main()
