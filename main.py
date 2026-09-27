import math

import pygame
import sys


# ==========================================
# CONFIGURAÇÕES
# ==========================================

from config import (
    LARGURA,
    ALTURA,
    FPS,
    TITULO,
    VIDA_MAXIMA,
    ESCALA,
    TAMANHO_TILE
)


# ==========================================
# TELA INICIAL
# ==========================================

from tela_inicial import tela_inicial


# ==========================================
# CENAS
# ==========================================

from cenas import mostrar_cenas, mostrar_final, quebrar_texto


# ==========================================
# RECURSOS
# ==========================================

from recursos import (
    carregar_chao,
    carregar_parede,
    carregar_personagem,
    carregar_coracao,
    carregar_eren,
    carregar_pbrr,
    carregar_boss,
    carregar_boss6,
    carregar_boss7,
    carregar_arma,
    carregar_porta
)


# ==========================================
# JOGADOR
# ==========================================

from jogador import Jogador


# ==========================================
# EREN
# ==========================================

from eren import Eren


# ==========================================
# CORAÇÃO
# ==========================================

from coracao import Coracao


# ==========================================
# PBRR
# ==========================================

from PBRR import PBRR


# ==========================================
# BOSSES
# ==========================================

from bosses import GerenciadorBosses


# ==========================================
# INTERFACE
# ==========================================

from interface import Interface


# ==========================================
# MAPA
# ==========================================

from mapa import (
    desenhar_chao,
    desenhar_paredes,
    definir_mapa,
    obter_rect_porta,
    obter_rect_passagem_porta,
    definir_porta_aberta
)


# ==========================================
# CAIXA DE DIÁLOGO
# ==========================================

from caixa_dialogo import CaixaDialogo


# ==========================================
# SOMBRAS
# ==========================================

from sombra import SistemaSombras


# ==========================================
# INICIAR PYGAME
# ==========================================

pygame.init()


# ==========================================
# JANELA
# ==========================================

tela = pygame.display.set_mode(
    (
        0,
        0
    ),
    pygame.FULLSCREEN
)

fullscreen = True


# ==========================================
# TELA INTERNA DO JOGO
# ==========================================

tela_jogo = pygame.Surface(
    (
        LARGURA,
        ALTURA
    )
)
superficie_transicao = pygame.Surface((LARGURA, ALTURA))


# ==========================================
# TÍTULO
# ==========================================

pygame.display.set_caption(
    TITULO
)


# ==========================================
# FUNÇÃO FULLSCREEN
# ==========================================

def alternar_fullscreen():

    global tela
    global fullscreen

    fullscreen = not fullscreen

    if fullscreen:

        tela = pygame.display.set_mode(
            (
                0,
                0
            ),
            pygame.FULLSCREEN
        )

    else:

        tela = pygame.display.set_mode(
            (
                LARGURA,
                ALTURA
            ),
            pygame.RESIZABLE
        )


# ==========================================
# APRESENTAR TELA
# ==========================================

def apresentar_tela():

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    escala = min(
        largura_tela / LARGURA,
        altura_tela / ALTURA
    )

    novo_tamanho = (
        int(LARGURA * escala),
        int(ALTURA * escala)
    )

    tela_escalada = pygame.transform.scale(
        tela_jogo,
        novo_tamanho
    )

    tela.fill(
        (
            0,
            0,
            0
        )
    )

    tela.blit(
        tela_escalada,
        (
            (largura_tela - novo_tamanho[0]) // 2,
            (altura_tela - novo_tamanho[1]) // 2
        )
    )


class IndicadorInteracao:

    def __init__(self):
        self.sprites = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/particulas/E{indice}.png"
                ).convert_alpha(),
                (29, 29)
            )
            for indice in (1, 2)
        ]
        self.alvo = None
        self.progresso = 0.0
        self.ultimo_tempo = pygame.time.get_ticks()

    def atualizar(self, alvo):
        agora = pygame.time.get_ticks()
        delta = max(0, agora - self.ultimo_tempo)
        self.ultimo_tempo = agora
        self.alvo = alvo

        if alvo is not None:
            self.progresso = min(1.0, self.progresso + delta / 250)
        else:
            self.progresso = max(0.0, self.progresso - delta / 250)

    def desenhar(self, tela, personagem):
        if self.progresso <= 0:
            return

        agora = pygame.time.get_ticks()
        sprite = self.sprites[(agora // 800) % len(self.sprites)]
        tamanho = max(1, int(29 * self.progresso))
        sprite = pygame.transform.scale(sprite, (tamanho, tamanho))
        angulo = math.sin(agora / 350) * 20
        sprite = pygame.transform.rotate(sprite, angulo)
        sprite.set_alpha(int(255 * self.progresso))

        rect_personagem = personagem.pegar_sprite().get_rect(
            topleft=(personagem.x, personagem.y)
        )
        deslocamento_x = math.sin(agora / 420) * 3
        deslocamento_y = math.sin(agora / 510) * 3
        distancia_saida = 46 * self.progresso
        rect = sprite.get_rect(
            center=(
                int(rect_personagem.centerx + deslocamento_x),
                int(rect_personagem.centery + distancia_saida + deslocamento_y)
            )
        )
        tela.blit(sprite, rect)


# ==========================================
# CLOCK
# ==========================================

clock = pygame.time.Clock()


# ==========================================
# TELA INICIAL
# ==========================================

if not tela_inicial(tela):

    pygame.quit()
    sys.exit()


# ==========================================
# CENAS
# ==========================================

if not mostrar_cenas(tela):

    pygame.quit()
    sys.exit()


# ==========================================
# CARREGAR CHÃO
# ==========================================

chao = carregar_chao()


# ==========================================
# CARREGAR PAREDE
# ==========================================

parede = carregar_parede()


# ==========================================
# CARREGAR SPRITES DO JOGADOR
# ==========================================

(
    baixo,
    cima,
    esquerda,
    direita
) = carregar_personagem()


# ==========================================
# CARREGAR SPRITES DO EREN
# ==========================================

sprites_eren = carregar_eren()


# ==========================================
# CARREGAR CORAÇÃO
# ==========================================

sprites_coracao = carregar_coracao()


# ==========================================
# CARREGAR SPRITES DO PBRR
# ==========================================

(
    pbrr_frente,
    pbrr_costas,
    pbrr_esquerda,
    pbrr_direita
) = carregar_pbrr()


# ==========================================
# CRIAR PBRR
# ==========================================

pbrr = PBRR(
    pbrr_frente,
    pbrr_costas,
    pbrr_esquerda,
    pbrr_direita,
    LARGURA // 2,
    ALTURA // 2
)


# ==========================================
# CRIAR OUTROS BOSSES
# ==========================================

bosses = {
    "pbrr": pbrr
}

for identificador, pasta in (
    ("boss2", "boss2"),
    ("boss3", "boss3"),
    ("boss4", "boss4")
):
    bosses[identificador] = PBRR(
        *carregar_boss(pasta),
        LARGURA // 2,
        ALTURA // 2
    )

    if identificador == "boss4":
        sprite_ataque_boss4 = pygame.image.load(
            "assets/ataques/ataque4.png"
        ).convert_alpha()
        bosses[identificador].sprite_ataque_4 = pygame.transform.scale(
            sprite_ataque_boss4,
            (
                sprite_ataque_boss4.get_width() * ESCALA,
                sprite_ataque_boss4.get_height() * ESCALA
            )
        )
        bosses[identificador].sprite_ataque_4_seq = [
            bosses[identificador].sprite_ataque_4
        ]

bosses["boss2"].configurar_padrao_ataque("boss2")
bosses["boss3"].configurar_padrao_ataque("boss3")
bosses["boss4"].configurar_padrao_ataque("boss4")

(
    sprite_boss6_caindo,
    sprites_boss6_entrada,
    sprites_boss6_frente
) = carregar_boss6()
bosses["boss6"] = PBRR(
    sprites_boss6_frente,
    sprites_boss6_frente,
    sprites_boss6_frente,
    sprites_boss6_frente,
    LARGURA // 2,
    ALTURA // 2
)
bosses["boss6"].configurar_animacao_boss6(
    sprite_boss6_caindo,
    sprites_boss6_entrada,
    sprites_boss6_frente
)
bosses["boss6"].configurar_padrao_ataque("boss6")

bosses["boss7"] = PBRR(
    *carregar_boss7(),
    LARGURA // 2,
    ALTURA // 2
)
bosses["boss7"].configurar_padrao_ataque("boss6")

# ==========================================
# CRIAR JOGADOR
# ==========================================

jogador = Jogador(
    baixo,
    cima,
    esquerda,
    direita,
    largura_tela=LARGURA,
    altura_tela=ALTURA
)
indicador_interacao = IndicadorInteracao()

# ==========================================
# MAPA ATIVO E PORTA DE SAÍDA
# ==========================================

mapa_ativo = 1
definir_mapa(mapa_ativo)
porta_sprites = carregar_porta()
porta_sprite_selecionada = pygame.transform.scale(
    pygame.image.load("assets/porta/portaselected.png").convert_alpha(),
    (2 * TAMANHO_TILE, TAMANHO_TILE)
)
papel_final = pygame.transform.scale(
    pygame.image.load("assets/Documentos/Papel.png").convert_alpha(),
    (54, 54)
)
botao_normal = pygame.transform.scale(
    pygame.image.load("assets/botao/botao1.png").convert_alpha(),
    (23, 12)
)
botao_frames = [
    botao_normal,
    pygame.transform.scale(
        pygame.image.load("assets/botao/botao2.png").convert_alpha(),
        (23, 12)
    ),
    pygame.transform.scale(
        pygame.image.load("assets/botao/botao3.png").convert_alpha(),
        (23, 12)
    )
]
botao_selecionado = pygame.transform.scale(
    pygame.image.load("assets/botao/botaoselected.png").convert_alpha(),
    (23, 12)
)
rect_papel_final = papel_final.get_rect(
    center=(LARGURA // 2, ALTURA // 2)
)
rect_botao_final = botao_normal.get_rect(
    center=(LARGURA // 2, rect_papel_final.top - 2)
)
texto_papel_final = (
    "Incrompreensível! Inconcebível!\n"
    "Parastes-me, contudo não admitirei funesto fim.\n"
    "Consentirei com o extermínio das obras engendradas por ti, "
    "mas terá de carregar também o fim seu e de vosso feudatário."
)
papel_final_coletado = False
porta_estado = {
    "fase": "idle",
    "inicio": 0,
    "indice": 0,
    "finalizado": False,
}
botao_estado = {
    "animando": False,
    "inicio": 0
}


def atualizar_porta():
    global mapa_ativo, porta_estado

    agora = pygame.time.get_ticks()

    if porta_estado["fase"] == "abrindo":
        elapsed = agora - porta_estado["inicio"]
        porta_estado["indice"] = min(7, int((elapsed / 1000) * 8))
        if elapsed >= 1000:
            porta_estado["indice"] = 7
            definir_porta_aberta(True)
            porta_estado["fase"] = "aberta"
        return

    if porta_estado["fase"] == "aberta":
        rect_jogador = jogador.obter_rect()
        rect_passagem = obter_rect_passagem_porta()
        sobreposicao = rect_jogador.clip(rect_passagem)
        dentro_da_largura = (
            rect_jogador.left >= rect_passagem.left
            and rect_jogador.right <= rect_passagem.right
        )
        if dentro_da_largura and sobreposicao.height >= 3:
            porta_estado["fase"] = "fade_out"
            porta_estado["inicio"] = agora
        return

    if porta_estado["fase"] == "fade_out":
        elapsed = agora - porta_estado["inicio"]
        if elapsed >= 1000:
            mapa_ativo = 2
            definir_mapa(mapa_ativo)
            jogador.x = LARGURA // 2 - 25
            jogador.y = ALTURA - 120
            jogador.velocidade_x = 0
            jogador.velocidade_y = 0
            porta_estado["fase"] = "fade_in"
            porta_estado["inicio"] = agora
            porta_estado["indice"] = 7
        return

    if porta_estado["fase"] == "fade_in":
        if agora - porta_estado["inicio"] >= 1000:
            sprite_jogador = jogador.pegar_sprite()
            sprite_eren = eren.baixo[0]
            rect_jogador = sprite_jogador.get_rect(
                topleft=(jogador.x, jogador.y)
            )
            rect_eren = sprite_eren.get_rect()
            rect_eren.midright = rect_jogador.midleft
            eren.x, eren.y = rect_eren.topleft
            eren.direcao = "direita"
            eren.frame = 0
            eren.contador_animacao = 0
            eren.direcao_bloqueada = None
            eren.tempo_bloqueado = 0
            porta_estado["fase"] = "done"
            porta_estado["finalizado"] = True
        return


def desenhar_porta(tela):
    if mapa_ativo != 1:
        return

    rect = pygame.Rect(6 * TAMANHO_TILE, 0, 2 * TAMANHO_TILE, TAMANHO_TILE)
    if porta_estado["fase"] == "idle":
        distancia = pygame.Vector2(
            jogador.obter_rect().center
        ).distance_to(rect.center)
        sprite = (
            porta_sprite_selecionada
            if distancia <= 100
            else pygame.transform.scale(
                porta_sprites[0],
                (2 * TAMANHO_TILE, TAMANHO_TILE)
            )
        )
    else:
        sprite = pygame.transform.scale(
            porta_sprites[porta_estado["indice"]],
            (2 * TAMANHO_TILE, TAMANHO_TILE)
        )
    tela.blit(sprite, rect)


def desenhar_papel_final(tela):
    if mapa_ativo != 2:
        return

    if not papel_final_coletado:
        tela.blit(papel_final, rect_papel_final)

    if botao_estado["animando"]:
        indice = min(
            2,
            (pygame.time.get_ticks() - botao_estado["inicio"]) // 400
        )
        botao = botao_frames[indice]
    elif indicador_interacao.alvo == "botao":
        botao = botao_selecionado
    else:
        botao = botao_normal
    tela.blit(botao, rect_botao_final)


def desenhar_transicao(tela):
    fase = porta_estado["fase"]
    if fase not in ("fade_out", "fade_in"):
        return

    progresso = min(1.0, (pygame.time.get_ticks() -
                    porta_estado["inicio"]) / 1000)
    alpha = int(255 * (progresso if fase == "fade_out" else 1 - progresso))
    superficie_transicao.fill((0, 0, 0))
    superficie_transicao.set_alpha(alpha)
    tela.blit(superficie_transicao, (0, 0))


# ==========================================
# CRIAR ARMA NO CHÃO
# ==========================================

arma_base = carregar_arma()
arma = pygame.transform.scale(
    arma_base,
    (
        arma_base.get_width() * 4,
        arma_base.get_height() * 4
    )
)
arma_sprites_direcionais = {
    direcao: pygame.transform.scale(
        pygame.image.load(f"assets/arma/{arquivo}.png").convert_alpha(),
        (28, 28)
    )
    for direcao, arquivo in {
        (0, 1): "B",
        (1, 0): "D",
        (1, 1): "DB",
        (1, -1): "DC",
        (-1, 0): "E",
        (-1, 1): "EB",
        (-1, -1): "EC"
    }.items()
}
ARMA_OFFSETS_MAO = {
    (0, 1): (-13, 20),
    (1, 0): (23, 13),
    (1, 1): (20, 9),
    (1, -1): (15, 5),
    (-1, 0): (-23, 13),
    (-1, 1): (-20, 9),
    (-1, -1): (-15, 5)
}
arma_sprite_na_mao = arma_sprites_direcionais[(0, 1)]
arma_rect = arma.get_rect(
    center=(
        LARGURA // 2,
        ALTURA // 2 - 120
    )
)
arma_angulo = 0
arma_coletada = False


def atualizar_arma():
    global arma_angulo, arma_sprite_na_mao

    if arma_coletada:
        sprite_jogador = jogador.pegar_sprite()
        centro = pygame.Vector2(
            jogador.x + sprite_jogador.get_width() / 2,
            jogador.y + sprite_jogador.get_height() / 2
        )
        direcao = jogador.direcao_mira.copy()
        if direcao.length_squared() == 0:
            direcao = pygame.Vector2(0, 1)
        chave_direcao = (
            int(direcao.x > 0) - int(direcao.x < 0),
            int(direcao.y > 0) - int(direcao.y < 0)
        )
        if chave_direcao in arma_sprites_direcionais:
            arma_sprite_na_mao = arma_sprites_direcionais[chave_direcao]
        else:
            arma_sprite_na_mao = None

        offset_x, offset_y = ARMA_OFFSETS_MAO.get(chave_direcao, (0, 0))
        arma_rect.center = centro + pygame.Vector2(offset_x, offset_y)
        return

    tempo = pygame.time.get_ticks() / 1000
    arma_angulo = math.sin(tempo * 1.8) * 7
    arma_rect.centerx = LARGURA // 2 + math.sin(tempo * 1.3) * 8
    arma_rect.centery = ALTURA // 2 - 120 + math.sin(tempo * 1.9) * 6


# ==========================================
# GERENCIADOR DE BOSSES
# ==========================================

gerenciador_bosses = GerenciadorBosses(
    bosses,
    jogador
)


# ==========================================
# CRIAR EREN
# ==========================================

eren = Eren(
    *sprites_eren,
    jogador
)


# ==========================================
# CRIAR CORAÇÃO
# ==========================================

coracao = Coracao(
    sprites_coracao,
    LARGURA,
    ALTURA
)

jogador.definir_coracao(coracao)


# ==========================================
# CRIAR INTERFACE
# ==========================================

interface = Interface(
    VIDA_MAXIMA
)


# ==========================================
# CRIAR CAIXA DE DIÁLOGO
# ==========================================

caixa_dialogo = CaixaDialogo(
    LARGURA,
    ALTURA
)


# ==========================================
# SISTEMA DE SOMBRAS
# ==========================================

sistema_sombras = SistemaSombras(
    posicao_luz=(120, -180),
    cor=(10, 13, 24),
    intensidade=0.62
)


# ==========================================
# INICIAR PRIMEIRO DIÁLOGO
# ==========================================

caixa_dialogo.iniciar(
    0
)


def obter_alvo_interacao():
    if (
        interface.morta
        or not caixa_dialogo.pode_mover()
        or gerenciador_bosses.documento_ativo
        or botao_estado["animando"]
        or porta_estado["fase"] in ("fade_out", "fade_in", "done")
    ):
        return None

    centro_jogador = pygame.Vector2(jogador.obter_rect().center)
    alvos = []

    if mapa_ativo == 1 and jogador.tem_chave and porta_estado["fase"] == "idle":
        centro_porta = pygame.Vector2(obter_rect_porta().center)
        alvos.append(("porta", centro_porta))

    if not arma_coletada:
        alvos.append(("arma", pygame.Vector2(arma_rect.center)))

    if mapa_ativo == 2 and papel_final_coletado:
        alvos.append(("botao", pygame.Vector2(rect_botao_final.center)))

    alvos_proximos = [
        (centro_jogador.distance_to(centro), nome)
        for nome, centro in alvos
        if centro_jogador.distance_to(centro) <= 100
    ]
    if not alvos_proximos:
        return None

    return min(alvos_proximos)[1]


def interagir_com_alvo():
    global arma_coletada

    alvo = obter_alvo_interacao()
    if alvo == "porta":
        porta_estado["fase"] = "abrindo"
        porta_estado["inicio"] = pygame.time.get_ticks()
        porta_estado["indice"] = 0
    elif alvo == "arma":
        arma_coletada = True
        gerenciador_bosses.iniciar()
    elif alvo == "botao":
        botao_estado["animando"] = True
        botao_estado["inicio"] = pygame.time.get_ticks()


# ==========================================
# LOOP PRINCIPAL
# ==========================================

rodando = True


while rodando:
    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        # ----------------------------------
        # FECHAR JOGO
        # ----------------------------------

        if evento.type == pygame.QUIT:

            rodando = False

        # ----------------------------------
        # TECLAS
        # ----------------------------------

        if evento.type == pygame.KEYDOWN:

            if evento.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                interface.invencibilidade_secreta = not (
                    interface.invencibilidade_secreta
                )

            # ==================================
            # F11
            # ==================================

            if evento.key == pygame.K_F11:

                alternar_fullscreen()

            # ==================================
            # DIÁLOGO
            # ==================================

            caixa_dialogo.processar_evento(
                evento
            )

            if evento.key == pygame.K_e:
                interagir_com_alvo()

    if not rodando:
        break

    if (
        botao_estado["animando"]
        and pygame.time.get_ticks() - botao_estado["inicio"] >= 1200
    ):
        mostrar_final(tela)
        rodando = False
        break

    # ======================================
    # ATUALIZAR CAIXA DE DIÁLOGO
    # ======================================

    caixa_dialogo.atualizar()

    # ======================================
    # ATUALIZAR ARMA
    # ======================================

    atualizar_arma()
    if not interface.morta:
        atualizar_porta()

    # ======================================
    # ATUALIZAR JOGO
    # ======================================

    if (
        not interface.morta
        and caixa_dialogo.pode_mover()
        and porta_estado["fase"] not in ("fade_out", "fade_in")
        and not botao_estado["animando"]
    ):

        gerenciador_bosses.atualizar(interface)
        gerenciador_bosses.atualizar_documentos(jogador)

        if not gerenciador_bosses.documento_ativo:
            identificador_dialogo = (
                gerenciador_bosses.consumir_dialogo_pendente()
            )
            if identificador_dialogo is not None:
                caixa_dialogo.iniciar_boss(identificador_dialogo)
            elif (
                gerenciador_bosses.boss is not None
                and not caixa_dialogo.ativo
                and gerenciador_bosses.boss.animacao_entrada_ativa
                and not gerenciador_bosses.boss.entrada_iniciada
                and gerenciador_bosses.boss.y < 0
            ):
                gerenciador_bosses.iniciar_entrada_boss_ativo()

            # ==================================
            # ATUALIZAR JOGADOR
            # ==================================

            jogador.atualizar()

            if (
                mapa_ativo == 2
                and not papel_final_coletado
                and jogador.obter_rect().colliderect(rect_papel_final)
            ):
                papel_final_coletado = True
                gerenciador_bosses.iniciar_documento_final(
                    texto_papel_final
                )

            coracao.ativo = jogador.usando_coracao

            # ==================================
            # ATUALIZAR EREN
            # ==================================

            eren.atualizar()

            # ==================================
            # ATUALIZAR CORAÇÃO
            # ==================================

            coracao.atualizar()

            indicador_interacao.atualizar(obter_alvo_interacao())

    interface.atualizar_particulas()

    # ======================================
    # LIMPAR TELA
    # ======================================

    tela_jogo.fill(
        (
            0,
            0,
            0
        )
    )

    if interface.morta:
        interface.desenhar_gore(
            tela_jogo
        )
        jogador.desenhar(
            tela_jogo,
            interface.obter_alpha_game_over()
        )
    else:
        # ======================================
        # DESENHAR MAPA
        # ======================================

        desenhar_chao(
            tela_jogo,
            chao
        )
        desenhar_papel_final(tela_jogo)

        bosses_ativos = gerenciador_bosses.obter_bosses()
        personagens = [
            (eren.obter_rect().bottom, eren),
            (jogador.obter_rect().bottom, jogador)
        ]
        for boss in bosses_ativos:
            personagens.append((boss.obter_rect().bottom, boss))
        personagens.sort(key=lambda personagem: personagem[0])

        objetos_sombra = [personagem for _, personagem in personagens]

        sistema_sombras.desenhar(
            tela_jogo,
            objetos_sombra
        )

        desenhar_paredes(
            tela_jogo,
            parede
        )

        desenhar_porta(tela_jogo)

        for boss in bosses_ativos:
            boss.desenhar_ataques(tela_jogo)

        gerenciador_bosses.desenhar_balas(
            tela_jogo
        )

        indicador_interacao.desenhar(tela_jogo, jogador)

        arma_atras_personagem = (
            arma_coletada
            and arma_sprite_na_mao is not None
            and jogador.direcao_mira.x != 0
            and jogador.direcao_mira.y < 0
        )
        if arma_atras_personagem:
            rect_arma = arma_sprite_na_mao.get_rect(
                center=arma_rect.center
            )
            tela_jogo.blit(arma_sprite_na_mao, rect_arma)

        for _, personagem in personagens:
            if (
                personagem in bosses_ativos
                and gerenciador_bosses.efeito_derrota is not None
            ):
                deslocamento = gerenciador_bosses.efeito_derrota
                sprite = deslocamento.get(
                    "sprite_final") or personagem.pegar_sprite()
                sprite = sprite.copy()
                brilho = deslocamento.get("brilho", 1.0)
                if brilho > 1.0 and deslocamento.get("aplicar_brilho", False):
                    brilho_surface = sprite.copy()
                    for y in range(brilho_surface.get_height()):
                        for x in range(brilho_surface.get_width()):
                            r, g, b, a = brilho_surface.get_at((x, y))
                            if a <= 0:
                                continue
                            intensidade = min(255, int((r + g + b) / 3))
                            fator = min(1.0, (brilho - 1.0) * 0.85)
                            novo_r = int(r + (255 - r) * fator)
                            novo_g = int(g + (255 - g) * fator)
                            novo_b = int(b + (255 - b) * fator)
                            brilho_surface.set_at(
                                (x, y),
                                (novo_r, novo_g, novo_b, a)
                            )
                    sprite = brilho_surface
                tela_jogo.blit(
                    sprite,
                    (
                        personagem.x + deslocamento["offset_x"],
                        personagem.y + deslocamento["offset_y"]
                    )
                )
            else:
                personagem.desenhar(tela_jogo)

        if not arma_coletada:
            sprite_arma = pygame.transform.rotate(arma, arma_angulo - 90)
            rect_arma = sprite_arma.get_rect(center=arma_rect.center)
            tela_jogo.blit(sprite_arma, rect_arma)
        elif arma_sprite_na_mao is not None and not arma_atras_personagem:
            rect_arma = arma_sprite_na_mao.get_rect(center=arma_rect.center)
            tela_jogo.blit(arma_sprite_na_mao, rect_arma)

        interface.desenhar_gore(
            tela_jogo
        )

        # ======================================
        # DESENHAR CORAÇÃO
        # ======================================

        coracao.desenhar(
            tela_jogo,
            jogador
        )

        # ======================================
        # DESENHAR VIDA
        # ======================================

        interface.desenhar_vida(
            tela_jogo
        )

        interface.stamina = jogador.stamina
        interface.desenhar_stamina(
            tela_jogo
        )

        gerenciador_bosses.desenhar_interface(
            tela_jogo
        )

    if not interface.morta:
        # ======================================
        # DESENHAR CAIXA DE DIÁLOGO
        # ======================================

        caixa_dialogo.desenhar(
            tela_jogo
        )

    gerenciador_bosses.desenhar_documentos(tela_jogo)

    desenhar_transicao(tela_jogo)

    # ======================================
    # APRESENTAR TELA
    # ======================================

    apresentar_tela()

    # ======================================
    # ATUALIZAR DISPLAY
    # ======================================

    pygame.display.flip()

    # ======================================
    # FPS
    # ======================================

    clock.tick(FPS)


# ==========================================
# ENCERRAR PYGAME
# ==========================================

pygame.quit()

sys.exit()
