import os
import subprocess
import json
import sys

if not os.path.exists('./Dados'):
    print("\033[93mParece ser o primeiro uso da aplicação, muito obrigado!\nFaça uma requisição manual para autoconfiguração\033[0m")
    resposta = 'n'

else:
    print("\033[1mDeseja importar uma lista de cidades?\033[0m")
    resposta = input()

if not (resposta.startswith("S") or resposta.startswith("Y") or resposta.startswith("s") or resposta.startswith("y")):
    print("\n\033[1mInsira o estado:\033[0m")
    estado = input()
    with open('estado.txt', 'w') as file:
        file.write(estado)
    print("\n\033[1mInsira a cidade:\033[0m")
    cidade = input()
    with open('cidades.txt', 'w') as file:
        file.write(cidade)

with open('cidades.txt', 'r') as file:
    listaCidades = file.read().splitlines()

for cidade in listaCidades:
    with open('estado.txt' , 'r') as file:
        estado = file.read()

    estado = estado.lower().replace('-',' ').replace('á','a').replace('â','a').replace('ã','a').replace('é','e')
    estado = estado.replace('ê','e').replace('í','i').replace('ó','o').replace('ô','o').replace('ú','ú').title()
    estado = estado.replace('Da', 'da').replace('Do','do').replace('De','de').replace('No', 'no').replace('Na','na').replace('Em','em')

    cidade = cidade.lower().replace('-',' ').replace('á','a').replace('â','a').replace('ã','a').replace('é','e')
    cidade = cidade.replace('ê','e').replace('í','i').replace('ó','o').replace('ô','o').replace('ú','ú').title()
    cidade = cidade.replace('Da', 'da').replace('Do','do').replace('De','de').replace('No', 'no').replace('Na','na').replace('Em','em')

    if not os.path.exists(os.path.join("Dados", estado, cidade)):
        os.makedirs(os.path.join("Dados", estado, cidade))

    estado = estado.replace(' ', r'%20')
    cidade = cidade.replace(' ', r'%20')


    with open('arvore/comercial', 'r') as file:
        comercial = file.read()

    comercial = comercial.replace(r'Rio%20Grande%20do%20Sul', estado).replace(r'Porto%20Alegre', cidade).replace(r'curl ', r'curl -s ')
    resultado = subprocess.check_output(comercial, shell=True, text=True)

    if r'<span>1015</span>' in resultado:
        raise Exception("\n\033[93mErro:Vivareal temporariamente o baniu de acessar seu servidor.\nCaso persista, use VPN. Error 1015.\033[0m")

    pagina = resultado.replace("\"totalCount\"", "\n"+"\"totalCount\"")
    pagina = pagina.replace(",", "\n")

    var = pagina.split("\n")
    for line in var:
            if line.startswith("\"totalCount\""):
                total=line.split(",\"")[0].replace("\"totalCount\":","").replace(r'}','')
                print("\nNúmero total de imóveis para", cidade.replace(r'%20', ' ')+":",'\033[93m'+total+'\033[0m')
                break

    if int(total)>10000:
        print("O número supera 10000\nDividindo por categorias")
        lista = [
            "consultorio",
            "galpao",
            "imovel",
            "lote",
            "ponto",
            "predio",
            "sala"
            ]

        for linha in lista:
            with open(f"arvore/categorias/{linha}", 'r') as file:
                categoria = file.read()
            categoria = categoria.replace(r'Rio%20Grande%20do%20Sul', estado).replace(r'Porto%20Alegre', cidade).replace(r'curl ', r'curl -s ')
            resultado = subprocess.check_output(categoria, shell=True, text=True)

            pagina = resultado.replace("\"totalCount\"", "\n"+"\"totalCount\"")
            pagina = pagina.replace(",", "\n")

            desdeNumeroResultado = 0
            var = pagina.split("\n")
            for line in var:
                    if line.startswith("\"totalCount\""):
                        totalCategorais=line.split(",\"")[0].replace("\"totalCount\":","").replace(r'}','')
                        print("Número total de imóveis para a categoria",linha+":",totalCategorais)
                        if int(totalCategorais)>10000:
                            print("O número novamente supera 10000\nDividindo por área")
                            with open(f"arvore/categorias/area/{linha}", 'r') as file:
                                categoriaArea = file.read()

                            desdeArea = 0
                            mini = 0
                            maxi = 100
                            acumuladorTotalCategoraisarea = 0
                            for _ in range(int(int(totalCategorais)/110)):
                                print(mini,"e",maxi)
                                if (acumuladorTotalCategoraisarea == int(totalCategorais)):
                                    break

                                if _ == 0:
                                    categoriaArea = categoriaArea.replace(r'Rio%20Grande%20do%20Sul', estado).replace(r'Porto%20Alegre', cidade).replace(r'curl ', r'curl -s ')
                                    categoriaArea = categoriaArea.replace(r'Min=55', f"Min={mini}").replace(r'Max=115', f"Max={maxi}")
                                else:
                                    categoriaArea = categoriaArea.replace(f"Min={mini}", f"Min={maxi+1}").replace(f"Max={maxi}", f"Max={maxi+2}")
                                    mini = maxi + 1
                                    maxi = maxi + 2
                                print(categoriaArea.split('SALE')[0])
                                print(mini,"novamente",maxi)

                                resultado = subprocess.check_output(categoriaArea, shell=True, text=True)

                                pagina = resultado.replace("\"totalCount\"", "\n"+"\"totalCount\"")
                                pagina = pagina.replace(",", "\n")

                                var = pagina.split("\n")
                                for line in var:
                                        if line.startswith("\"totalCount\""):
                                            totalCategoriasArea=line.split(",\"")[0].replace("\"totalCount\":","").replace(r'}','')
                                            print("O número total de imóveis para a área de", mini, "a", maxi, "é:", totalCategoriasArea)
                                            break
                                i=1.05
                                j=0.95
                                while not (8000 <= int(totalCategoriasArea) <= 10000) and (int(totalCategorais) > (acumuladorTotalCategoraisarea+int(totalCategoriasArea))):
                                    while int(totalCategoriasArea) < 8000  and (int(totalCategorais) > (acumuladorTotalCategoraisarea+int(totalCategoriasArea))):
                                        categoriaArea = categoriaArea.replace(f"Min={mini}", f"Min={mini}").replace(f"Max={maxi}", f"Max={int(maxi*i)}")
                                        maxi = int(maxi*i)
                                        print("Área máxima:", maxi)
                                        print("Área mínima:", mini)
                                        if int(totalCategoriasArea) < 6000:
                                            i = 1.3
                                            if maxi > 10000:
                                                i = 8.5
                                        else:
                                            i = 1.05
                                        resultado = subprocess.check_output(categoriaArea, shell=True, text=True)

                                        pagina = resultado.replace("\"totalCount\"", "\n"+"\"totalCount\"")
                                        pagina = pagina.replace(",", "\n")

                                        var = pagina.split("\n")
                                        for line in var:
                                                if line.startswith("\"totalCount\""):
                                                    totalCategoriasArea=line.split(",\"")[0].replace("\"totalCount\":","").replace(r'}','')
                                                    print("Número de imóveis encontrados:",totalCategoriasArea,"-- menor")
                                                    break

                                    while int(totalCategoriasArea) > 10000:
                                        categoriaArea = categoriaArea.replace(f"Min={int(mini)}", f"Min={mini}").replace(f"Max={int(maxi)}", f"Max={int(maxi*j)}")
                                        maxi = int(maxi*j)
                                        print("Área máxima:", maxi)
                                        if int(totalCategoriasArea) > 20000:
                                            j = 0.7
                                        else:
                                            j = 0.95
                                        resultado = subprocess.check_output(categoriaArea, shell=True, text=True)

                                        pagina = resultado.replace("\"totalCount\"", "\n"+"\"totalCount\"")
                                        pagina = pagina.replace(",", "\n")

                                        var = pagina.split("\n")
                                        for line in var:
                                                if line.startswith("\"totalCount\""):
                                                    totalCategoriasArea=line.split(",\"")[0].replace("\"totalCount\":","").replace(r'}','')
                                                    print("Imóveis encontrados:",totalCategoriasArea,"-- maior")
                                                    break

                                else:
                                    print("Chegou!\nNúmero de imóveis:",totalCategoriasArea)
                                    acumuladorTotalCategoraisarea = acumuladorTotalCategoraisarea + int(totalCategoriasArea)
                                    desde = 0
                                    print(mini, maxi)
                                    print(categoriaArea.split('SALE')[0])
                                    print(mini, maxi)
                                    for desde in range(int(int(totalCategoriasArea)/110)+1):
                                        print(desdeNumeroResultado)
                                        pronto=categoriaArea.replace(r'from=', r'from='+str(desde*110)).replace(r'size=36', r'size=110')
                                        resultado = subprocess.check_output(pronto, shell=True, text=True)

                                        if r'"search":{"result":{"listings":[]' not in resultado.split('displayAddressType')[0]:
                                            with open('Dados/'+estado.replace(r'%20', ' ')+'/'+cidade.replace(r'%20', ' ')+'/'+linha+'-area'+str(desdeNumeroResultado)+'.json', 'w') as salvar:
                                                salvar.write(resultado)
                                                desdeNumeroResultado+=1
                                        else:
                                                print("Término com o arquivo",linha+str(desdeArea-1)+'.json')
                                                break
                                    print("Fim")

                        else:
                            desde = 0
                            for desde in range(90):
                                pronto = categoria.replace(r'from=', r'from='+str(desde*110)).replace(r'size=36', r'size=110')
                                pronto = pronto.replace(r'curl -s', r'curl').replace(r'curl', r'curl -s')
                                resultado = subprocess.check_output(pronto, shell=True, text=True)

                                if r'"search":{"result":{"listings":[]' not in resultado.split('displayAddressType')[0]:
                                    with open('Dados/'+estado.replace(r'%20', ' ')+'/'+cidade.replace(r'%20', ' ')+'/'+linha+str(desde)+'.json', 'w') as salvar:
                                        salvar.write(resultado)
                                else:
                                        print("Término com o arquivo",linha+str(desde-1)+'.json')
                                        break
                        break

    else:
        desde = 0
        for desde in range(90):
            pronto=comercial.replace(r'from=', r'from='+str(desde*110)).replace(r'size=36', r'size=110')
            resultado = subprocess.check_output(pronto, shell=True, text=True)

            if r'"search":{"result":{"listings":[]' not in resultado.split('displayAddressType')[0]:
                with open('Dados/'+estado.replace(r'%20', ' ')+'/'+cidade.replace(r'%20', ' ')+'/comercial-geral'+str(desde)+'.json', 'w') as salvar:
                    salvar.write(resultado)
            else:
                    print("Término com o arquivo",'comercial-geral'+str(desde-1)+'.json')
                    break


    diretorio = os.listdir('./Dados/'+estado.replace('%20',' ')+'/'+cidade.replace('%20',' '))

    headers = True
    for arquivoJson in diretorio:
        with open('./Dados/'+estado.replace('%20',' ')+'/'+cidade.replace('%20',' ')+'/'+arquivoJson, 'r') as file:
            try:
                dados = json.load(file)
            except json.decoder.JSONDecodeError as error:
                print("\033[93mErro: Certifique-se de que a cidade já não foi processada\033[0m")
            caminho = dados["search"]["result"]["listings"]

        with open('./Dados/'+estado.replace('%20',' ')+'/'+cidade.replace('%20',' ')+'/'+cidade.replace('%20',' ')+'.csv', 'a') as file:
            if headers == True:
                file.write("Anúncio, ID, Tipo, Preço, Imovel, Link, Área, CEP, Estado, Cidade, Bairro, Rua, Número, Latitude, Longitude")
                headers = False
            for num, caminho in enumerate(caminho):
                try:
                    try:
                        anuncio = caminho["listing"]["title"]
                    except KeyError:
                        anuncio = " "
                    try:
                        idd = caminho["listing"]["id"]
                    except KeyError:
                        idd = " "
                    try:
                        tipo = caminho["listing"]["pricingInfos"][0]["businessType"]
                    except KeyError:
                        tipo = " "
                    except KeyError:
                        area = " "
                    except IndexError:
                        area = " "
                    try:
                        preco = caminho["listing"]["pricingInfos"][0]["price"]
                    except KeyError:
                        preco = " "
                    except KeyError:
                        area = " "
                    except IndexError:
                        area = " "
                    try:
                        imovel = caminho["listing"]["unitTypes"][0]
                    except KeyError:
                        imovel = " "
                    except KeyError:
                        area = " "
                    except IndexError:
                        area = " "
                    try:
                        link = caminho["link"]["href"]
                    except KeyError:
                        link = " "
                    try:
                        area = caminho["listing"]["usableAreas"][0]
                    except KeyError:
                        area = " "
                    except IndexError:
                        area = " "
                    try:
                        cep = caminho["listing"]["address"]["zipCode"]
                    except KeyError:
                        cep = " "
                    try:
                        estadoConversor = caminho["listing"]["address"]["state"]
                    except KeyError:
                        estadoConversor = " "
                    try:
                        cidadeConversor = caminho["listing"]["address"]["city"]
                    except KeyError:
                        cidadeConversor = " "
                    try:
                        bairro = caminho["listing"]["address"]["neighborhood"]
                    except KeyError:
                        bairro = " "
                    try:
                        rua = caminho["listing"]["address"]["street"]
                    except KeyError:
                        rua = " "
                    try:
                        numero = caminho["listing"]["address"]["streetNumber"]
                    except KeyError:
                        numero = " "
                    try:
                        latitude = caminho["listing"]["address"]["point"]["lat"]
                    except KeyError:
                        latitude = " "
                    try:
                        longitude = caminho["listing"]["address"]["point"]["lon"]
                    except KeyError:
                        longitude = " "
                    file.write(f"\n\"{anuncio}\", {idd}, {tipo}, {preco}, {imovel}, {link}, {area}, {cep}, {estadoConversor}, {cidadeConversor}, {bairro}, {rua}, {numero}, {latitude}, {longitude}")
                except KeyError:
                    print("\033[93mErro no anúncio", num+'\033[0m')
    print("\rArquivo\033[93m "+cidade.replace('%20',' ')+'.csv\033[0m criado com sucesso\r')
