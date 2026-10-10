"""
content.py
==========
Everything the site says, in one place. Edit here, then run:

    python3 tools/build.py

Sections
  1. SITE       business facts (contact, hours, address)
  2. PASSEIOS   the nine day trips
  3. TRANSFERS  the three transfer services
  4. FAQ        questions and answers
  5. Filter and navigation labels
"""

# =============================================================================
# 1. SITE · business facts
# -----------------------------------------------------------------------------
# A value left as "" is simply not shown on the site. Nothing here is invented:
# fill in the real details and rebuild.
# =============================================================================
SITE = {
    "name": "Baía Azul",
    "tagline": "Passeios e transfers na Bahia",
    "description": "Agência de passeios e transfers com base no Pelourinho, em Salvador. "
                   "Morro de São Paulo, Boipeba, Ilha dos Frades, Itaparica e Praia do Forte, com saídas todos os dias.",
    "neighbourhood": "Pelourinho, Centro Histórico",
    "city": "Salvador, Bahia",
    "hours": "Todos os dias, das 7h às 22h",
    "map_url": "https://www.google.com/maps/search/?api=1&query=Pelourinho%2C+Salvador+-+BA",

    # WhatsApp number in international format, digits only, for example "5571999990000".
    # Every booking button uses it. While it is empty the buttons still open WhatsApp
    # with the message written, but the visitor has to pick the contact by hand.
    "whatsapp": "5571996798039",
    # The same number as it should be read by people, for example "+55 71 99999-0000".
    "whatsapp_display": "+55 71 99679-8039",
    "email": "",
    "instagram": "",            # handle without the @
    "street": "Shopping do Pelô",   # street and number inside the Pelourinho
    "cnpj": "",
    "cadastur": "",
    # Public address of the site, for example "https://www.baiaazul.com.br". Used for
    # the canonical link, the social preview image and the sitemap.
    "url": "https://mento-web.github.io/baia-azul",
    "year": 2026,
}


# =============================================================================
# 2. PASSEIOS
# -----------------------------------------------------------------------------
# Field guide
#   slug       file name of the page
#   eyebrow    small line above the title (what sets this trip apart)
#   title      big line (keep it under about 22 characters)
#   name       full name, used in the menu, the booking form and WhatsApp
#   tipo       filter: ilhas | praias | aventura | dayuse
#   saida      filter: salvador | morro | boipeba (space separated if more than one)
#   duration   short label at the top right of the card ("" hides it)
#   facts      the row between the two hairlines; the first item is emphasised
#   card       one or two sentences plus bullet facts for the list
#   lede       one sentence under the page title
#   body       paragraphs for the page
#   rows       label and value pairs for the page
#   steps      itinerary, only where the route is fixed
#   know       "bom saber" points
#   price      number for search engines, None when the price is on request
# =============================================================================
PASSEIOS = [
    {
        "slug": "volta-as-ilhas-tinhare",
        "eyebrow": "Volta às ilhas",
        "title": "Tinharé e Boipeba",
        "name": "Volta às Ilhas de Tinharé e Boipeba",
        "tipo": "ilhas", "saida": "morro",
        "img": "tinhare", "img2": "tinhare-agua",
        "duration": "7h30",
        "facts": ["A partir de R$ 350", "Tabela oficial de Cairu", "Cooler liberado"],
        "card": "O passeio de barco mais pedido de Morro de São Paulo: um dia inteiro entre piscinas naturais "
                "e as praias mais bonitas de Tinharé e Boipeba. • 9h30 às 17h • Saída de Morro de São Paulo",
        "lede": "Um dia de barco pelas piscinas naturais e praias do arquipélago.",
        "body": [
            "É o clássico de Morro de São Paulo, e não por acaso. Em um único dia você contorna o arquipélago de "
            "barco, para em piscinas naturais de água transparente e desembarca em praias de Tinharé e de Boipeba "
            "aonde não se chega caminhando.",
            "O valor segue a tabela definida pela Secretaria de Turismo de Cairu, o município ao qual as ilhas "
            "pertencem. Você reserva sabendo que paga o preço oficial, o mesmo praticado em toda a ilha.",
            "A ordem das paradas muda com a maré, que é quem decide a melhor hora de cada piscina natural.",
        ],
        "rows": [
            ("Saída", "Morro de São Paulo"),
            ("Horário", "9h30 às 17h"),
            ("Valor", "A partir de R$ 350"),
            ("Preço", "Tabelado pela Secretaria de Turismo de Cairu"),
            ("Cooler", "Liberado"),
        ],
        "steps": [],
        "know": [
            "Pode levar cooler com as suas bebidas e lanches.",
            "Leve roupa de banho, protetor solar, chapéu e toalha.",
            "O passeio começa em Morro de São Paulo. Se você está em Salvador, combine com o nosso transfer diário.",
            "O ponto de encontro e o horário de embarque são confirmados na reserva.",
        ],
        "price": 350,
    },
    {
        "slug": "day-use-morro-de-sao-paulo",
        "eyebrow": "Day use",
        "title": "Morro de São Paulo",
        "name": "Day Use Morro de São Paulo",
        "tipo": "dayuse", "saida": "salvador",
        "img": "day-use-morro", "img2": "morro-primeira",
        "duration": "Dia inteiro",
        "facts": ["A partir de R$ 290", "Taxa de embarque R$ 20"],
        "card": "Ida e volta no mesmo dia, saindo de Salvador, com tempo para conhecer os principais pontos da ilha. "
                "• Cerca de 3h de viagem desde o Terminal Marítimo • Trajeto semiterrestre",
        "lede": "Morro de São Paulo em um dia, com ida e volta de Salvador.",
        "body": [
            "Para quem tem pouco tempo e não quer ir embora da Bahia sem conhecer Morro de São Paulo. "
            "Você sai de Salvador pela manhã, passa o dia na ilha e volta no fim da tarde.",
            "A viagem é semiterrestre: combina trechos de barco e de estrada, com todas as conexões organizadas "
            "pela nossa equipe. São cerca de 3 horas, contadas a partir do Terminal Marítimo de Salvador.",
            "Em Morro não circulam carros. Tudo se faz a pé, entre as praias numeradas, a vila e o farol, "
            "e um dia é suficiente para ver o essencial.",
        ],
        "rows": [
            ("Saída", "Salvador"),
            ("Viagem", "Cerca de 3h desde o Terminal Marítimo"),
            ("Valor", "A partir de R$ 290"),
            ("Taxa de embarque", "R$ 20, obrigatória, paga à parte"),
        ],
        "steps": [],
        "know": [
            "A taxa de embarque de R$ 20 é obrigatória e não está incluída no valor do passeio.",
            "Vá de calçado confortável: a ilha se percorre a pé.",
            "Os horários de saída e de retorno são confirmados na reserva.",
            "Quer ficar mais dias? Veja o transfer diário para Morro de São Paulo.",
        ],
        "price": 290,
    },
    {
        "slug": "ilha-dos-frades-e-itaparica",
        "eyebrow": "Escuna",
        "title": "Frades e Itaparica",
        "name": "Ilha dos Frades e Itaparica",
        "tipo": "ilhas", "saida": "salvador",
        "img": "frades", "img2": "escuna",
        "duration": "Dia inteiro",
        "facts": ["A partir de R$ 140", "Entrada em Frades R$ 34,90"],
        "card": "Um dia de escuna pela Baía de Todos-os-Santos, com cerca de duas horas em cada ilha. "
                "• Saída às 9h do Terminal Marítimo de Salvador • Cooler liberado",
        "lede": "A Baía de Todos-os-Santos de escuna, com parada em duas ilhas.",
        "body": [
            "A baía vista de dentro. A escuna sai de Salvador com serviço de bar, samba e frutas frescas a bordo, "
            "e navega por cerca de 1h40 até a Ilha dos Frades.",
            "O desembarque é na Ponta de Nossa Senhora de Guadalupe. Frades foi a primeira ilha do Nordeste a "
            "receber o selo internacional Bandeira Azul, e ali o tempo é livre para nadar e explorar.",
            "Depois a escuna segue para Itaparica, a maior ilha da Baía de Todos-os-Santos. A chegada à praia é em "
            "pequenos botes, e a parada tem banho de mar e um restaurante típico com redes para descansar.",
        ],
        "rows": [
            ("Saída", "Terminal Marítimo de Salvador, 9h"),
            ("Busca no hotel", "Horário combinado na reserva"),
            ("Em cada ilha", "Cerca de 2h"),
            ("Valor", "A partir de R$ 140"),
            ("Entrada em Frades", "R$ 34,90, paga à parte"),
            ("Cooler", "Liberado"),
        ],
        "steps": [
            "Embarque no Terminal Marítimo de Salvador, às 9h.",
            "Cerca de 1h40 de navegação pela baía, com bar, samba e frutas a bordo.",
            "Ilha dos Frades: tempo livre na Ponta de Nossa Senhora de Guadalupe.",
            "Travessia até a Ilha de Itaparica.",
            "Desembarque em botes, banho de mar e parada em restaurante típico.",
            "Retorno a Salvador.",
        ],
        "know": [
            "A taxa de entrada na Ilha dos Frades, de R$ 34,90, é paga à parte.",
            "Pode levar cooler.",
            "Confirme na reserva o que está incluído no serviço de bordo e no restaurante.",
            "Leve roupa de banho, protetor solar e uma muda de roupa seca para a volta.",
        ],
        "price": 140,
    },
    {
        "slug": "praia-do-forte-e-guarajuba",
        "eyebrow": "Litoral Norte",
        "title": "Praia do Forte",
        "name": "Praia do Forte e Guarajuba",
        "tipo": "praias", "saida": "salvador",
        "img": "praia-do-forte", "img2": "",
        "duration": "8h",
        "facts": ["A partir de R$ 140", "9h às 17h", "Saída de Salvador"],
        "card": "Praia do Forte e Guarajuba, duas das praias mais queridas do Litoral Norte, em um só dia. "
                "• Cerca de 2h em cada praia",
        "lede": "Duas praias do Litoral Norte, com ida e volta no mesmo dia.",
        "body": [
            "O Litoral Norte começa logo depois de Salvador, e este passeio leva você a duas das suas praias "
            "mais conhecidas, com ida e volta no mesmo dia.",
            "Na Praia do Forte, a antiga vila de pescadores virou um calçadão de lojas e restaurantes que termina "
            "na igrejinha à beira-mar. Na maré baixa, os recifes formam piscinas naturais. É ali também que fica a "
            "base do Projeto Tamar, de proteção às tartarugas marinhas, que você pode visitar no seu tempo livre, "
            "com ingresso à parte.",
            "Guarajuba completa o dia com uma faixa larga de areia e coqueiros.",
        ],
        "rows": [
            ("Saída", "Salvador"),
            ("Horário", "9h às 17h"),
            ("Em cada praia", "Cerca de 2h"),
            ("Valor", "A partir de R$ 140"),
        ],
        "steps": [],
        "know": [
            "São cerca de duas horas em cada praia.",
            "A visita ao Projeto Tamar é opcional e tem ingresso próprio.",
            "O ponto de encontro e o horário de busca são confirmados na reserva.",
            "Leve roupa de banho, protetor solar e chapéu.",
        ],
        "price": 140,
    },
    {
        "slug": "day-use-village-itaparica",
        "eyebrow": "Day use",
        "title": "Village Itaparica",
        "name": "Day Use Village Itaparica",
        "tipo": "dayuse", "saida": "salvador morro",
        "img": "village-itaparica", "img2": "",
        "duration": "Dia inteiro",
        "facts": ["De Salvador R$ 140", "De Morro R$ 210"],
        "card": "Um dia de descanso na Ilha de Itaparica, com a travessia organizada por nós. "
                "• Saídas de Salvador e de Morro de São Paulo",
        "lede": "Um dia de descanso em Itaparica, saindo de Salvador ou de Morro.",
        "body": [
            "Itaparica é a maior ilha da Baía de Todos-os-Santos e fica bem em frente a Salvador. "
            "O day use é para quem quer um dia inteiro de praia e sossego, sem se preocupar com a logística.",
            "Você escolhe de onde sair. De Salvador, embarcando no Terminal Marítimo ou com busca no hotel, "
            "o valor é o mesmo. Quem está em Morro de São Paulo também pode fazer o passeio, com saída da ilha.",
        ],
        "rows": [
            ("Do Terminal Marítimo de Salvador", "R$ 140"),
            ("De hotel em Salvador", "R$ 140"),
            ("De Morro de São Paulo", "R$ 210"),
        ],
        "steps": [],
        "know": [
            "O valor muda conforme o ponto de partida.",
            "Confirme na reserva o que o day use inclui em lazer e alimentação.",
            "Os horários de saída e de retorno são combinados na reserva.",
        ],
        "price": 140,
    },
    {
        "slug": "garapua-de-4x4",
        "eyebrow": "Off-road 4x4",
        "title": "Garapuá",
        "name": "Garapuá de 4x4",
        "tipo": "aventura", "saida": "morro",
        "img": "garapua", "img2": "",
        "duration": "",
        "facts": ["Valor sob consulta", "Saída de Morro de São Paulo"],
        "card": "Trilhas de areia em veículo 4x4 até a Praia do Encanto e a enseada de Garapuá, "
                "com banho nas piscinas naturais.",
        "lede": "Por trilhas de areia até a enseada mais tranquila de Tinharé.",
        "body": [
            "O lado menos visitado da Ilha de Tinharé. A bordo de um 4x4, por caminhos de areia e com condução "
            "segura, você chega à Praia do Encanto e à enseada de Garapuá, uma vila de pescadores cercada de coqueiros.",
            "Na maré certa, as piscinas naturais de Garapuá ficam rasas, mornas e transparentes. "
            "É a parada mais esperada do dia.",
        ],
        "rows": [
            ("Saída", "Morro de São Paulo"),
            ("Veículo", "4x4, em trajeto off-road"),
            ("Valor", "Sob consulta"),
        ],
        "steps": [],
        "know": [
            "O trajeto é off-road e pode balançar bastante.",
            "Leve roupa de banho, protetor solar e toalha.",
            "Valor, horário e ponto de encontro são informados na reserva.",
        ],
        "price": None,
    },
    {
        "slug": "quadriciclo-garapua",
        "eyebrow": "Aventura",
        "title": "Quadriciclo",
        "name": "Passeio de quadriciclo",
        "tipo": "aventura", "saida": "morro",
        "img": "quadriciclo", "img2": "",
        "duration": "",
        "facts": ["Valor sob consulta", "Saída de Morro de São Paulo"],
        "card": "Você pilota. Um roteiro de quadriciclo por trilhas e praias até Garapuá, "
                "com as suas piscinas naturais, e a Ilha de Boipeba.",
        "lede": "Você no comando, por trilhas e praias de Tinharé e Boipeba.",
        "body": [
            "Para quem prefere dirigir a ser levado. Você pilota um quadriciclo potente por trilhas e trechos "
            "de praia, com paradas em Garapuá, nas suas piscinas naturais, e na Ilha de Boipeba.",
            "É o jeito mais direto de sentir a ilha: vento, areia e uma praia diferente a cada parada.",
        ],
        "rows": [
            ("Saída", "Morro de São Paulo"),
            ("Veículo", "Quadriciclo, pilotado por você"),
            ("Valor", "Sob consulta"),
        ],
        "steps": [],
        "know": [
            "Os requisitos para pilotar, como idade mínima e habilitação, são informados na reserva.",
            "Vá de calçado fechado e roupa que possa sujar.",
            "Valor, horário e ponto de encontro são informados na reserva.",
        ],
        "price": None,
    },
    {
        "slug": "ecoturismo-gamboa",
        "eyebrow": "Ecoturismo",
        "title": "Gamboa",
        "name": "Ecoturismo na Gamboa e Ilha da Coroa",
        "tipo": "praias", "saida": "morro",
        "img": "gamboa", "img2": "",
        "duration": "",
        "facts": ["Valor sob consulta", "Saída de Morro de São Paulo"],
        "card": "Falésias de argila na Praia da Gamboa, piscinas naturais para banho e mergulho, "
                "praias de areia branca quase desertas e a cozinha local.",
        "lede": "Falésias de argila, piscinas naturais e praias quase desertas.",
        "body": [
            "Um dia em ritmo lento, para quem viaja atrás de natureza. O roteiro passa pelas falésias de argila "
            "colorida da Praia da Gamboa, por piscinas naturais de água cristalina, boas para banho e mergulho, "
            "e por praias de areia branca onde quase não há ninguém.",
            "No caminho há tempo para provar a cozinha local, feita com o que o mar entrega no dia.",
        ],
        "rows": [
            ("Saída", "Morro de São Paulo"),
            ("Roteiro", "Praia da Gamboa e Ilha da Coroa"),
            ("Valor", "Sob consulta"),
        ],
        "steps": [],
        "know": [
            "Leve roupa de banho e uma muda de roupa.",
            "Se tiver máscara de mergulho, vale levar.",
            "Valor, horário e ponto de encontro são informados na reserva.",
        ],
        "price": None,
    },
    {
        "slug": "volta-a-ilha-de-boipeba",
        "eyebrow": "Volta à ilha",
        "title": "Boipeba",
        "name": "Volta à Ilha de Boipeba",
        "tipo": "ilhas", "saida": "boipeba",
        "img": "boipeba", "img2": "morere",
        "duration": "",
        "facts": ["Valor sob consulta", "Saída de Boipeba"],
        "card": "O passeio mais tradicional de Boipeba: uma volta completa pela ilha, "
                "com paradas nos seus pontos mais bonitos e reservados.",
        "lede": "A volta completa pela ilha mais preservada do arquipélago.",
        "body": [
            "Boipeba é vizinha de Morro de São Paulo e muito mais quieta. A volta à ilha é o seu passeio mais "
            "tradicional: um circuito completo que passa pelos principais pontos e também pelos mais reservados.",
            "Para aproveitar com calma, o ideal é dormir na ilha. O nosso transfer para Boipeba sai de Salvador "
            "todos os dias do ano.",
        ],
        "rows": [
            ("Saída", "Ilha de Boipeba"),
            ("Roteiro", "Volta completa pela ilha"),
            ("Valor", "Sob consulta"),
        ],
        "steps": [],
        "know": [
            "O passeio começa em Boipeba. Veja os horários do transfer saindo de Salvador.",
            "Leve roupa de banho, protetor solar e chapéu.",
            "Valor, horário e ponto de encontro são informados na reserva.",
        ],
        "price": None,
    },
]


# =============================================================================
# 3. TRANSFERS
# -----------------------------------------------------------------------------
# "times" feeds the timetable on transfers.html: (label, [times] or one text).
# =============================================================================
TRANSFERS = [
    {
        "id": "morro",
        "eyebrow": "Transfer diário",
        "title": "Morro de São Paulo",
        "name": "Transfer para Morro de São Paulo",
        "saida": "salvador morro",
        "img": "terminal",
        "duration": "3h",
        "facts": ["5 saídas por dia", "3h desde o terminal", "Todos os dias"],
        "card": "De Salvador a Morro de São Paulo todos os dias do ano, com busca no aeroporto, "
                "no hotel ou embarque direto no Terminal Marítimo.",
        "body": [
            "O caminho mais confortável entre Salvador e Morro de São Paulo. A viagem é semiterrestre: "
            "combina trechos de barco e de estrada, e a nossa equipe cuida de cada conexão.",
            "São 3 horas de viagem. Contamos o tempo a partir do Terminal Marítimo porque é de lá que partem "
            "também as outras opções, como o catamarã, e assim a comparação fica justa.",
        ],
        "go_title": "Salvador para Morro de São Paulo",
        "go": [
            ("Aeroporto", ["5h15", "8h15", "11h15", "14h15", "16h15"]),
            ("Terminal Marítimo", ["6h30", "9h30", "12h30", "15h30", "17h30"]),
            ("Hotel", "Horário combinado na reserva"),
        ],
        "back_title": "Morro de São Paulo para Salvador",
        "back": [("Retornos", ["6h20", "9h20", "12h20", "15h20"])],
    },
    {
        "id": "boipeba",
        "eyebrow": "Transfer diário",
        "title": "Ilha de Boipeba",
        "name": "Transfer para a Ilha de Boipeba",
        "saida": "salvador boipeba",
        "img": "morere",
        "duration": "",
        "facts": ["2 saídas por dia", "Todos os dias"],
        "card": "De Salvador à Ilha de Boipeba todos os dias do ano. Fique quantos dias quiser "
                "e volte quando for melhor para você.",
        "body": [
            "Boipeba pede mais de um dia, e o transfer foi pensado para isso. As saídas acontecem nos 365 dias "
            "do ano, então você escolhe quando ir e quando voltar.",
            "A busca no aeroporto e nos hotéis de Salvador acompanha os horários de embarque. "
            "Informe o seu voo ou o seu hotel na reserva e confirmamos a hora exata.",
        ],
        "go_title": "Salvador para a Ilha de Boipeba",
        "go": [
            ("Terminal Marítimo", ["6h30", "9h30"]),
            ("Aeroporto", "Horário combinado na reserva"),
            ("Hotel", "Horário combinado na reserva"),
        ],
        "back_title": "Ilha de Boipeba para Salvador",
        "back": [("Retornos", ["7h", "11h30"])],
    },
    {
        "id": "privativo",
        "eyebrow": "Sob medida",
        "title": "Transfer privativo",
        "name": "Transfer privativo",
        "saida": "salvador morro boipeba",
        "img": "lacerda",
        "duration": "",
        "facts": ["Carro, van ou ônibus", "No seu horário"],
        "card": "Um veículo só para você, a sua família ou o seu grupo, no horário que você escolher, "
                "com motoristas profissionais e experientes.",
        "body": [
            "Para famílias, grupos e para quem prefere não dividir o trajeto. Você define o horário e o ponto "
            "de partida, e nós escolhemos o veículo certo para o tamanho do grupo: carro, van ou ônibus.",
            "Os veículos são modernos e conduzidos por motoristas profissionais e experientes. "
            "Conte quantas pessoas são e para onde vão, e enviamos o orçamento.",
        ],
        "go_title": "", "go": [], "back_title": "", "back": [],
    },
]


# =============================================================================
# 4. FAQ · grouped. Answers are lists of paragraphs.
# =============================================================================
FAQ = [
    ("Transfers", [
        ("Que tipo de transfer vocês fazem?",
         ["O nosso transfer é semiterrestre. Escolhemos esse formato porque ele entrega mais conforto "
          "e mais segurança durante toda a viagem."]),
        ("O que quer dizer semiterrestre?",
         ["Quer dizer que a viagem combina trechos de barco e trechos de estrada. "
          "As conexões entre um e outro são organizadas pela nossa equipe, do começo ao fim."]),
        ("Quanto tempo dura a viagem até Morro de São Paulo?",
         ["São 3 horas. Contamos o tempo a partir do Terminal Marítimo de Salvador porque é de lá que saem "
          "também as outras opções, como o catamarã."]),
        ("Vocês me buscam no aeroporto ou no hotel?",
         ["Sim. Buscamos no Aeroporto de Salvador, no hotel em que você está hospedado ou recebemos você "
          "diretamente no Terminal Marítimo. Os horários do aeroporto e do terminal estão na página de transfers. "
          "A hora da busca no hotel é combinada na reserva."]),
        ("Vocês fazem transfer privativo?",
         ["Sim, com carros, vans e ônibus, conforme o tamanho do grupo."]),
        ("Quero passar vários dias em Boipeba. É possível?",
         ["É. O transfer funciona nos 365 dias do ano, justamente para você ir e voltar de Boipeba quando quiser."]),
    ]),
    ("Passeios", [
        ("De onde saem os passeios?",
         ["Depende do passeio. Morro de São Paulo em um dia, Ilha dos Frades e Itaparica, Praia do Forte e o day use "
          "em Itaparica saem de Salvador. A volta às ilhas, Garapuá, o quadriciclo e a Gamboa saem de "
          "Morro de São Paulo. A volta à ilha sai de Boipeba."]),
        ("As taxas estão incluídas no valor?",
         ["Não. Quando existem, são pagas à parte: a taxa de embarque do day use em Morro de São Paulo é de R$ 20, "
          "e a entrada na Ilha dos Frades custa R$ 34,90."]),
        ("Posso levar cooler?",
         ["Na volta às ilhas de Tinharé e no passeio de escuna a Frades e Itaparica, pode. "
          "Para os outros passeios, pergunte na reserva."]),
        ("O que devo levar?",
         ["Roupa de banho, protetor solar, chapéu, toalha e um documento com foto. "
          "Para os passeios de barco, uma muda de roupa seca ajuda na volta."]),
        ("Por que alguns passeios não têm preço no site?",
         ["Esses valores são informados diretamente pela nossa equipe. "
          "Chame no WhatsApp e respondemos com o valor para a sua data e o seu grupo."]),
    ]),
    ("Reserva e pagamento", [
        ("Como faço a reserva?",
         ["Pelo WhatsApp. Toque em Reservar, escolha o passeio, a data e o número de pessoas, e a mensagem já "
          "chega pronta para a nossa equipe. Confirmamos a disponibilidade, o horário e o ponto de encontro."]),
        ("Quais são as formas de pagamento?",
         ["Cartão de crédito e de débito, de todas as bandeiras, PIX e transferência bancária."]),
        ("Qual é o horário de atendimento?",
         ["Todos os dias, inclusive domingos e feriados, das 7h às 22h."]),
    ]),
]

# Cancellation rules, shown on the FAQ page and on the policy page.
CANCELAMENTO = [
    ("Compra pelo site, WhatsApp ou telefone",
     "Reembolso integral se você pedir em até 7 dias corridos depois da contratação, "
     "como prevê o artigo 49 do Código de Defesa do Consumidor."),
    ("Se o passeio acontecer antes desses 7 dias",
     "Vale a regra das 24 horas, descrita abaixo."),
    ("Compra feita na nossa loja",
     "Reembolso de 50% do valor do serviço não realizado, se o pedido for feito até 24 horas antes do horário marcado."),
    ("Pedido com menos de 24 horas ou depois do passeio",
     "É considerado não comparecimento (no show) e não há reembolso."),
    ("Prazo e forma da devolução",
     "Em até 30 dias, pelo mesmo meio usado no pagamento."),
]


# =============================================================================
# 5. Filter and navigation labels
# =============================================================================
TIPOS = [("ilhas", "Ilhas e barco"), ("praias", "Praias e natureza"), ("dayuse", "Day use"),
         ("aventura", "Aventura"), ("transfer", "Transfers")]
SAIDAS = [("salvador", "Saída: Salvador"), ("morro", "Saída: Morro de São Paulo"), ("boipeba", "Saída: Boipeba")]
