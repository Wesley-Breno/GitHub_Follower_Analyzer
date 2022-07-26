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
        > Dê follow nas pessoas que voce nao segue de volta, ou dê unfollow nas pessoas que nao ti seguem de volta

        OBS: Para usar as funcoes follow() e unfollow(), o nome de usuario deve corresponder ao mesmo email e senha.
    """

    def __init__(self, usuario):
        self.usuario = usuario
        self.seguidores = []  # Pessoas que seguem o usuario
        self.seguindo = []  # Pessoas que o usuario segue

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
                self.seguidores.append(usuario.text)

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
                self.seguindo.append(usuario.text)

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

    def unfollow(self, email, senha):
        """
        Funcao que entra na conta e deixa de seguir as pessoas que nao
        seguem o usuario informado.

        :param email:  Email do usuario
        :param senha: Senha do usuario
        :return: None
        """
        if len(self.seguidores) == 0 and len(self.seguindo) == 0:  # Se o programa ainda nao analisou os seguidores
            self.get_seguindo()  # Pegando quem o usuario segue
            self.get_seguidores()  # Pegando os seguidores do usuario

        nao_me_segue_de_volta = []  # Lista onde ficara as pessoas que nao seguem o usuario de volta

        for segue in self.seguindo:
            if segue not in self.seguidores:  # Se a pessoa que o usuario segue nao seguir ele
                nao_me_segue_de_volta.append(segue)

        if len(nao_me_segue_de_volta) > 0:  # Se tiver alguem que nao segue o usuario de volta
            url = r'https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsignup%3Fref_cta%3DSign%2Bup' \
                  r'%26ref_loc' \
                  r'%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home '

            site = webdriver.Chrome()

            # Fazendo login
            site.get(url)  # Entrando no site
            sleep(2)  # Esperando 2secs para a pagina carregar
            site.find_element(By.NAME, 'login').send_keys(email)  # Colocando o email
            site.find_element(By.NAME, 'password').send_keys(senha)  # Colocando a senha
            site.find_element(By.NAME, 'commit').click()  # Clicando em logar

            cont = 0  # Contador para saber quantas pessoas deixou de seguir
            for nao_me_segue in nao_me_segue_de_volta:  # Entrando no perfil de cada pessoa que nao segue de volta
                site.get(f'https://github.com/{nao_me_segue}')
                sleep(1)
                site.find_element(By.CSS_SELECTOR,
                                  '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > '
                                  'div.Layout-sidebar > div > div.js-profile-editable-replace > '
                                  'div.d-flex.flex-column > div.flex-order-1.flex-md-order-none > div > div > span > '
                                  'form:nth-child(2) > input.btn.btn-block').click()  # Clicando em unfollow
                cont += 1
                print(f'Voce deixou de seguir \033[;31m>\033[m {nao_me_segue} \033[;31m<\033[m')

            print(f'\nVoce deixou de seguir \033[;31m{cont}\033[m contas que nao lhe seguiam de volta.\n')

        else:
            print('\n\t\033[;37mNao foi encontrado nenhuma pessoa que nao segue voce de volta.\033[m\n')

    def follow(self, email, senha):
        """
        Funcao que entra na conta do usuario informado e segue as pessoas que ele nao segue de volta.

        :param email: Email do usuario
        :param senha: Senha do usuario
        :return: None
        """
        if len(self.seguidores) == 0 and len(self.seguindo) == 0:
            self.get_seguindo()
            self.get_seguidores()

        nao_sigo_de_volta = []  # Lista onde ficara as pessoas que o usuario nao segue de volta

        for seguem in self.seguidores:
            if seguem not in self.seguindo:  # Se a pessoa que segue o usuario nao for seguida por ele
                nao_sigo_de_volta.append(seguem)

        if len(nao_sigo_de_volta) > 0:  # Se tiver alguem que o usuario nao segue de volta
            url = r'https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsignup%3Fref_cta%3DSign%2Bup' \
                  r'%26ref_loc' \
                  r'%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home '

            site = webdriver.Chrome()

            # Fazendo login
            site.get(url)  # Entrando no site
            sleep(2)  # Esperando 2secs para a pagina carregar
            site.find_element(By.NAME, 'login').send_keys(email)  # Colocando o email
            site.find_element(By.NAME, 'password').send_keys(senha)  # Colocando a senha
            site.find_element(By.NAME, 'commit').click()  # Clicando em logar

            cont = 0  # Contador que vai contar quantas pessoas o usuario seguiu de volta
            for nao_sigo in nao_sigo_de_volta:  # Para cada pessoa que o usuario nao segue de volta
                sleep(1)
                site.get(f'https://github.com/{nao_sigo}')  # Entrando no perfil da pessoa
                sleep(2)
                site.find_element(By.CSS_SELECTOR, '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div '
                                                   '> div.Layout-sidebar > div > div.js-profile-editable-replace > '
                                                   'div.d-flex.flex-column > div.flex-order-1.flex-md-order-none > '
                                                   'div > div > span > form:nth-child(1) > '
                                                   'input.btn.btn-block').click()  # Clicando em seguir
                cont += 1
                print(f'Voce comecou a seguir \033[;32m>\033[m {nao_sigo} \033[;32m<\033[m')

            print(f'\nVoce acaba de seguir \033[;32m{cont}\033[m contas que voce nao seguia de volta\n')

        else:
            print('\n\t\033[;37mNao foi encotrado nenhuma pessoa que voce nao segue de volta.\033[m\n')

    def mostrar_nao_sigo_de_volta(self):
        """
        Mostrando na tela as pessoas que o usuario nao segue de volta.
        :return: None
        """
        if len(self.seguidores) == 0 and len(self.seguindo) == 0:  # Verificando se seguidores/segue ja foram analisados
            self.get_seguindo()
            self.get_seguidores()

        print('\n\n\t\tPessoas que voce nao segue de volta\n')
        cont = 0  # Contador para saber se teve alguem que o usuario nao segue de volta
        for seguidor in self.seguidores:
            if seguidor not in self.seguindo:
                cont += 1
                print(f'\033[;31m>\033[m {seguidor}')

        if cont == 0:  # Se nao tiver alguem que o usuario nao siga de volta
            print('\n\t\t\033[;37mParece que voce ja segue todos de volta...\033[m\n')

    def mostrar_nao_seguem_de_volta(self):
        """
        Mostrando na tela as pessoas que nao seguem o usuario de volta
        :return: None
        """
        if len(self.seguidores) == 0 and len(self.seguindo) == 0:
            self.get_seguindo()
            self.get_seguidores()

        print('\n\n\t\tPessoas que nao ti seguem de volta\n')
        cont = 0
        for sigo in self.seguindo:
            if sigo not in self.seguidores:
                cont += 1
                print(f'\033[;31m>\033[m {sigo}')

        if cont == 0:
            print('\n\t\t\033[;37mParece que todos ja ti seguem de volta...\033[m\n')


if __name__ == '__main__':
    werli = AnalisaSeguidores('Wesley-Breno')
    print('\033[;37mAnalisando seguidores...\033[m')
    werli.mostrar_nao_sigo_de_volta()
    werli.mostrar_nao_seguem_de_volta()
    werli.unfollow('Aqui ficaria o email do usuario', 'Aqui ficaria a senha do usuario')
    werli.follow('Aqui ficaria o email do usuario', 'Aqui ficaria a senha do usuario')
