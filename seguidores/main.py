import requests  # Chamando o modulo requests para pegar os dados do site
from bs4 import BeautifulSoup  # Chamando a classe BeautifulSoup para manipular o HTML dos dados que foram pegados
from selenium import webdriver  # Chamando o driver para percorrer pelos seguidores/seguindo
from selenium.webdriver.common.by import By  # By para clicar na proxima pagina de seguidores/seguindo
from time import sleep  # Importando funcao sleep para deixar a pagina carregar


class AnalisaSeguidores:
    """
    Classe que analisa os seguidores de uma pessoa com base no nome de usuario dela.
        > Informe o nome de usuario
        > Espere o programa coletar todos os seguidores/seguindo deste usuario
        > Escolha uma das opcoes da funcao menu()
    """
    def __init__(self, usuario):
        self.usuario = usuario
        self._seguidores = []  # Pessoas que seguem o usuario
        self._seguindo = []  # Pessoas que o usuario segue

    def get_seguidores(self):
        """
        Vai entrar no site da GitHub no perfil do usuario informado, e colocar
        em uma lista cada pessoa que ele é seguido.
        :return: None
        """
        url = f'https://github.com/{self.usuario}?page=1&tab=followers'

        while True:
            dados = requests.get(url)  # Pegando dados do site onde ficam os seguidores
            html = BeautifulSoup(dados.text, 'html.parser')  # Pegando o texto HTML para poder manipular

            for usuario in html.select('.Link--secondary.pl-1'):  # Para cada seguidor
                self._seguidores.append(usuario.text)

            try:  # Tenta ir para a proxima pagina de seguidores
                proxima_pagina = webdriver.Chrome()
                proxima_pagina.get(url)
                proxima_pagina.find_element(By.XPATH,
                                            '//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[51]/div/a').click()

            except:  # Se nao tiver mais seguidores para mostrar
                proxima_pagina.close()
                break

            else:  # Se ainda tiver seguidores para mostrar
                sleep(1)  # Espera a pagina carregar
                url = proxima_pagina.current_url  # Trocando a URL para a pagina seguinte de seguidores
                proxima_pagina.close()  # Fechando a pagina

    def get_seguindo(self):
        """
        Vai entrar no site da GitHub no perfil do usuario informado, e colocar
        em uma lista cada pessoa que ele segue.
        :return: None
        """
        url = f'https://github.com/{self.usuario}?page=1&tab=following'

        while True:
            dados = requests.get(url)  # Pegando dados do site onde ficam as pessoas que o usuario segue
            html = BeautifulSoup(dados.text, 'html.parser')  # Pegando o texto HTML para poder manipular

            for usuario in html.select('.Link--secondary.pl-1'):  # Para cada pessoa que o usuario segue
                self._seguindo.append(usuario.text)

            try:  # Tenta ir para a proxima pagina de pessoas que o usuario segue
                proxima_pagina = webdriver.Chrome()
                proxima_pagina.get(url)
                proxima_pagina.find_element(By.XPATH,
                                            '//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[51]/div/a').click()

            except:  # Se nao tiver mais seguidores para mostrar
                proxima_pagina.close()
                break

            else:  # Se ainda tiver seguidores para mostrar
                sleep(1)  # Espera a pagina carregar
                url = proxima_pagina.current_url  # Trocando a URL para a pagina seguinte de pessoas que o usuario segue
                proxima_pagina.close()  # Fechando a pagina

    def menu(self):
        """
        Mostra o menu para executar uma das opcoes mostradas
        :return: None
        """
        while True:
            try:
                deseja = int(input("""
    Escolha uma das opcoes
    [ 1 ] - Ver as pessoas que seguem voce e voce nao segue
    [ 2 ] - Ver as pessoas que voce segue mas elas nao seguem voce

    Escolha: """))

            except:
                print('\n\n\t\t[\033[;31mERRO\033[m]: Por favor, tente novamente.\n\n')

            else:
                if deseja == 1:  # Se o usuario desejou ver as pessoas que seguem ele mas ele nao segue.

                    print('\n\nPessoas que voce nao segue de volta;')
                    for seguidor in self._seguidores:  # Para cada seguidor
                        if seguidor not in self._seguindo:  # Se o seguidor nao estiver sendo seguido pelo usuario
                            print(f'\033[1;31m►\033[m {seguidor}')

                    break

                elif deseja == 2:  # Se o usuario desejou ver as pessoas que segue mas nao seguem ele

                    print('\n\nPessoas que nao ti seguem de volta;')
                    for segue in self._seguindo:  # Pra cada pessoa que o usuario segue
                        if segue not in self._seguidores:  # Se a pessoa seguida nao estiver na lista de seguidores
                            print(f'\033[1;31m►\033[m {segue}')

                    break

                else:
                    print('\n\n\t\t[\033[;31mERRO\033[m]: Por favor, tente novamente.\n\n')


if __name__ == '__main__':
    werli = AnalisaSeguidores('Wesley-Breno')
    print('\033[;37mAnalisando seguidores...\033[m')
    werli.get_seguindo()
    werli.get_seguidores()
    werli.menu()
