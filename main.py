import requests  # Chamando o modulo requests para pegar os dados do site
from bs4 import BeautifulSoup  # Chamando a classe BeautifulSoup para manipular o HTML dos dados que foram pegados
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions # Chamando o driver para percorrer pelos seguidores/seguindo
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.common.by import By  # By para clicar na proxima pagina de seguidores/seguindo
from time import sleep  # Importando funcao sleep para deixar a pagina carregar


def get_followers(name_user: str) -> list:
    """
    Vai entra no perfil do usuario informado, e colocar em uma lista cada seguidor.
    :return: Retorna uma lista com os nomes dos seguidores do usuario.
    """
    cont = 1
    seguidores = set()

    while True:
        url = f'https://github.com/{name_user}?page={cont}&tab=followers'
        dados = requests.get(url)  # Pegando dados do site onde ficam os seguidores
        html = BeautifulSoup(dados.text, 'html.parser')  # Pegando o texto HTML para poder manipular

        for nome in html.select('.d-inline-block.no-underline.mb-1'):  # para cada seguidor
            seguidores.add(nome.text.split('\n')[2])  # Adicionando nome do usuario segue voce

        cont += 1  # Contador responsavel para ir para a outra pagina de seguidores

        paginacao = html.select('.disabled.color-fg-muted')
        if str(*paginacao) == '<span class="disabled color-fg-muted">Next</span>':  # Se nao tiver mais usuarios para mostrar
            break

    return list(seguidores)


def get_following(name_user: str) -> list:
    """
    Vai entra no perfil do usuario informado, e colocar em uma lista cada pessoa que o usuario segue.
    :return: Retorna uma lista com o nome de usuario das pessoas que o usuario segue.
    """
    seguindo = set()
    cont = 1

    while True:
        url = f'https://github.com/{name_user}?page={cont}&tab=following'
        dados = requests.get(url)  # Pegando dados do site onde ficam os seguidores
        html = BeautifulSoup(dados.text, 'html.parser')  # Pegando o texto HTML para poder manipular

        for nome in html.select('.d-inline-block.no-underline.mb-1'):  # para cada pessoa que voce segue
            seguindo.add(nome.text.split('\n')[2])  # Adicionando nome do usuario que voce segue

        cont += 1  # Contador responsavel para ir para a outra pagina de pessoas que voce segue

        paginacao = html.select('.disabled.color-fg-muted')
        if str(*paginacao) == '<span class="disabled color-fg-muted">Next</span>':  # Se nao tiver mais usuarios para mostrar
            break

    return list(seguindo)


def follow(email: str, password: str) -> None:
    """
    Funcao responsavel por entrar na conta do usuario depois de guardar os seguidores e pessoas que o usuario segue em
    uma lista e assim ir dando follow nas pessoas que o usuario ainda nao segue de volta.
    :param email: Email do usuario
    :param password: Senha do usuario
    :return: None
    """
    nao_sigo_de_volta = []  # Lista onde ficara as pessoas que o usuario nao segue de volta

    for seguem in seguidores:
        if seguem not in seguindo:  # Se a pessoa que segue o usuario nao for seguida por ele
            nao_sigo_de_volta.append(seguem)

    if len(nao_sigo_de_volta) > 0:  # Se tiver alguem que o usuario nao segue de volta
        url = r'https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsignup%3Fref_cta%3DSign%2Bup' \
              r'%26ref_loc' \
              r'%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home '

        options = ChromeOptions()
        options.add_argument('--headless')
        service = ChromiumService(executable_path=ChromeDriverManager().install())
        driver = Chrome(service=service, options=options)

        # Fazendo login
        driver.get(url)  # Entrando no site
        sleep(2)  # Esperando 2secs para a pagina carregar
        driver.find_element(By.NAME, 'login').send_keys(email)  # Colocando o email
        driver.find_element(By.NAME, 'password').send_keys(password)  # Colocando a senha
        driver.find_element(By.NAME, 'commit').click()  # Clicando em logar

        cont = 0  # Contador que vai contar quantas pessoas o usuario seguiu de volta
        for nao_sigo in nao_sigo_de_volta:  # Para cada pessoa que o usuario nao segue de volta
            sleep(1)
            driver.get(f'https://github.com/{nao_sigo}')  # Entrando no perfil da pessoa
            sleep(2)
            try:
                driver.find_element(By.CSS_SELECTOR, '.btn.btn-block').click()  # Clicando em seguir
            except:
                continue
            else:
                cont += 1
                print(f'Voce comecou a seguir \033[;32m>\033[m {nao_sigo} \033[;32m<\033[m')

        print(f'\nVoce acaba de seguir \033[;32m{cont}\033[m contas que voce nao seguia de volta\n')

    else:
        print('\n\t\033[;37mNao foi encotrado nenhuma pessoa que voce nao segue de volta.\033[m\n')


def unfollow(email: str, password: str) -> None:
    """
    Funcao responsavel por entrar na conta do usuario depois de guardar os seguidores e pessoas que o usuario segue em
    uma lista e assim ir dando unfollow nas pessoas que nao seguem o usuario de volta.
    :param email:  Email do usuario
    :param password: Senha do usuario
    :return: None
    """
    nao_me_segue_de_volta = []  # Lista onde ficara as pessoas que nao seguem o usuario de volta

    for segue in seguindo:
        if segue not in seguidores:  # Se a pessoa que o usuario segue nao seguir ele
            nao_me_segue_de_volta.append(segue)

    if len(nao_me_segue_de_volta) > 0:  # Se tiver alguem que nao segue o usuario de volta
        url = r'https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsignup%3Fref_cta%3DSign%2Bup' \
              r'%26ref_loc' \
              r'%3Dheader%2Blogged%2Bout%26ref_page%3D%252F%26source%3Dheader-home '

        options = ChromeOptions()
        options.add_argument('--headless')
        service = ChromiumService(executable_path=ChromeDriverManager().install())
        driver = Chrome(service=service, options=options)

        # Fazendo login
        driver.get(url)  # Entrando no site
        sleep(2)  # Esperando 2secs para a pagina carregar
        driver.find_element(By.NAME, 'login').send_keys(email)  # Colocando o email
        driver.find_element(By.NAME, 'password').send_keys(password)  # Colocando a senha
        driver.find_element(By.NAME, 'commit').click()  # Clicando em logar

        cont = 0  # Contador para saber quantas pessoas deixou de seguir
        for nao_me_segue in nao_me_segue_de_volta:  # Entrando no perfil de cada pessoa que nao segue de volta
            driver.get(f'https://github.com/{nao_me_segue}')
            sleep(1)
            try:
                driver.find_element(By.CSS_SELECTOR, 'body > div.logged-in.env-production.page-responsive.page-profile '
                                                   '> div.application-main > main > '
                                                   'div.container-xl.px-3.px-md-4.px-lg-5 > div > div.Layout-sidebar '
                                                   '> div > div.js-profile-editable-replace > div.d-flex.flex-column '
                                                   '> div.flex-order-1.flex-md-order-none > div > div > span > '
                                                   'form:nth-child(2) > input.btn.btn-block').click()  # Clicando em
            # unfollow
            except:
                continue
            else:
                cont += 1
                print(f'Voce deixou de seguir \033[;31m>\033[m {nao_me_segue} \033[;31m<\033[m')

        print(f'\nVoce deixou de seguir \033[;31m{cont}\033[m contas que nao lhe seguiam de volta.\n')

    else:
        print('\n\t\033[;37mNao foi encontrado nenhuma pessoa que nao segue voce de volta.\033[m\n')


if __name__ == "__main__":
    seguidores = get_followers('Wesley-Breno')
    seguindo = get_following('Wesley-Breno')
    follow('SEU EMAIL AQUI', 'SUA SENHA AQUI')
    unfollow('SEU EMAIL AQUI', 'SUA SENHA AQUI')
