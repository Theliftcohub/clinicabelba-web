#!/usr/bin/env python3
"""Traducciones de los textos de los 5 formularios rehechos desde Typeform (migracion/typeform_forms.json).
Los Typeform estaban SOLO en español también en las páginas traducidas del WordPress; en la web nueva se muestran
en el idioma de la página. Los VALORES que viajan a n8n (value de cada opción, nombres de campo) siguen siendo
los literales en español: aquí solo se traduce lo que ve el visitante. Traducciones hechas por Claude (30/09),
pendientes de revisión de la clínica (anotado en NO_LITERAL.md). El registro sigue el de la home: tú (es, ca, it, nl),
vous/Sie/вы (fr, de, ru, uk), you (en)."""

LANGS = ('ca', 'en', 'fr', 'de', 'it', 'nl', 'ru', 'uk')

X = {
    # ---- Belba Gral (iOSo1PBX) / Dr Dewever (BdYhxQFV) / Dr Chavarría (vwHofvjc) / Consulta online (tCXPyaGW)
    '*Da el primer paso para resolver tus dudas con un cirujano.*': (
        '*Fes el primer pas per resoldre els teus dubtes amb un cirurgià.*',
        '*Take the first step and clear up your doubts with a surgeon.*',
        '*Faites le premier pas pour résoudre vos doutes avec un chirurgien.*',
        '*Machen Sie den ersten Schritt und klären Sie Ihre Fragen mit einem Chirurgen.*',
        '*Fai il primo passo per risolvere i tuoi dubbi con un chirurgo.*',
        '*Zet de eerste stap en bespreek je twijfels met een chirurg.*',
        '*Сделайте первый шаг и обсудите свои сомнения с хирургом.*',
        '*Зробіть перший крок і обговоріть свої сумніви з хірургом.*'),
    'Primero, lo más importante: ¿Cómo te llamas?': (
        'Primer, el més important: com et dius?', 'First things first: what is your name?',
        "Tout d'abord, le plus important : comment vous appelez-vous ?", 'Zuerst das Wichtigste: Wie heißen Sie?',
        'Prima di tutto, la cosa più importante: come ti chiami?', 'Eerst het belangrijkste: hoe heet je?',
        'Прежде всего, самое важное: как вас зовут?', 'Насамперед найважливіше: як вас звати?'),
    'Primero, lo más importante. ¿Cómo te llamas?': (
        'Primer, el més important: com et dius?', 'First things first: what is your name?',
        "Tout d'abord, le plus important : comment vous appelez-vous ?", 'Zuerst das Wichtigste: Wie heißen Sie?',
        'Prima di tutto, la cosa più importante: come ti chiami?', 'Eerst het belangrijkste: hoe heet je?',
        'Прежде всего, самое важное: как вас зовут?', 'Насамперед найважливіше: як вас звати?'),
    'Lo más importante. ¿Cómo te llamas?': (
        'El més important: com et dius?', 'The most important thing: what is your name?',
        'Le plus important : comment vous appelez-vous ?', 'Das Wichtigste: Wie heißen Sie?',
        'La cosa più importante: come ti chiami?', 'Het belangrijkste: hoe heet je?',
        'Самое важное: как вас зовут?', 'Найважливіше: як вас звати?'),
    'Que Cirugía Necesitas:': (
        'Quina cirurgia necessites?', 'Which surgery do you need?', 'De quelle chirurgie avez-vous besoin ?',
        'Welche Operation benötigen Sie?', 'Di quale intervento hai bisogno?', 'Welke operatie heb je nodig?',
        'Какая операция вам нужна?', 'Яка операція вам потрібна?'),
    'Que Cirugía necesitas:': (
        'Quina cirurgia necessites?', 'Which surgery do you need?', 'De quelle chirurgie avez-vous besoin ?',
        'Welche Operation benötigen Sie?', 'Di quale intervento hai bisogno?', 'Welke operatie heb je nodig?',
        'Какая операция вам нужна?', 'Яка операція вам потрібна?'),
    'Cirugía de pecho': ('Cirurgia de pit', 'Breast surgery', 'Chirurgie mammaire', 'Brustoperation', 'Chirurgia del seno', 'Borstchirurgie', 'Хирургия груди', 'Хірургія грудей'),
    'Cirugía corporal': ('Cirurgia corporal', 'Body surgery', 'Chirurgie corporelle', 'Körperoperation', 'Chirurgia del corpo', 'Lichaamschirurgie', 'Хирургия тела', 'Хірургія тіла'),
    'Cirugía facial': ('Cirurgia facial', 'Facial surgery', 'Chirurgie du visage', 'Gesichtsoperation', 'Chirurgia del viso', 'Gezichtschirurgie', 'Хирургия лица', 'Хірургія обличчя'),
    'Cirugía genital': ('Cirurgia genital', 'Genital surgery', 'Chirurgie génitale', 'Genitaloperation', 'Chirurgia genitale', 'Genitale chirurgie', 'Интимная хирургия', 'Інтимна хірургія'),
    'Otra': ('Altra', 'Other', 'Autre', 'Andere', 'Altro', 'Anders', 'Другое', 'Інше'),
    '¿Cuándo tienes pensado operarte?': (
        'Quan tens pensat operar-te?', 'When are you planning to have surgery?', 'Quand envisagez-vous de vous faire opérer ?',
        'Wann möchten Sie sich operieren lassen?', 'Quando pensi di operarti?', 'Wanneer wil je je laten opereren?',
        'Когда вы планируете операцию?', 'Коли ви плануєте операцію?'),
    'Lo antes posible': ('Com més aviat millor', 'As soon as possible', 'Le plus tôt possible', 'So bald wie möglich', 'Il prima possibile', 'Zo snel mogelijk', 'Как можно скорее', 'Якомога швидше'),
    'En los próximos 1–3 meses': ('En els propers 1–3 mesos', 'In the next 1–3 months', 'Dans les 1 à 3 prochains mois', 'In den nächsten 1–3 Monaten', 'Nei prossimi 1–3 mesi', 'Binnen 1–3 maanden', 'В ближайшие 1–3 месяца', 'У найближчі 1–3 місяці'),
    'En 3–6 meses': ("D'aquí a 3–6 mesos", 'In 3–6 months', 'Dans 3 à 6 mois', 'In 3–6 Monaten', 'Tra 3–6 mesi', 'Over 3–6 maanden', 'Через 3–6 месяцев', 'Через 3–6 місяців'),
    'Aún estoy evaluando, no tengo fecha definida': (
        'Encara ho estic valorant, no tinc data', 'Still considering, no date yet', "J'y réfléchis encore, sans date définie",
        'Ich überlege noch, kein festes Datum', 'Ci sto ancora pensando, nessuna data', 'Ik overweeg het nog, geen datum',
        'Пока думаю, даты нет', 'Ще думаю, дати немає'),
    'Tu email': ('El teu email', 'Your email', 'Votre e-mail', 'Ihre E-Mail', 'La tua email', 'Je e-mail', 'Ваш email', 'Ваш email'),
    'Tu móvil': ('El teu mòbil', 'Your mobile number', 'Votre portable', 'Ihre Handynummer', 'Il tuo cellulare', 'Je mobiele nummer', 'Ваш мобильный телефон', 'Ваш мобільний телефон'),
    '¡Gracias por enviar la información!\nNos pondremos en contacto contigo muy pronto. \nMientras tanto, puedes visitar nuestra página web.': (
        'Gràcies per enviar la informació!\nEns posarem en contacte amb tu molt aviat.\nMentrestant, pots visitar la nostra pàgina web.',
        'Thank you for sending your information!\nWe will contact you very soon.\nIn the meantime, feel free to browse our website.',
        "Merci d'avoir envoyé vos informations !\nNous vous contacterons très prochainement.\nEn attendant, vous pouvez visiter notre site web.",
        'Vielen Dank für Ihre Angaben!\nWir melden uns sehr bald bei Ihnen.\nIn der Zwischenzeit können Sie sich gerne auf unserer Website umsehen.',
        'Grazie per averci inviato le informazioni!\nTi contatteremo molto presto.\nNel frattempo puoi visitare il nostro sito web.',
        'Bedankt voor het versturen van je gegevens!\nWe nemen zeer binnenkort contact met je op.\nIn de tussentijd kun je onze website bekijken.',
        'Спасибо за отправленную информацию!\nМы свяжемся с вами в ближайшее время.\nА пока вы можете посмотреть наш сайт.',
        "Дякуємо за надіслану інформацію!\nМи зв'яжемося з вами найближчим часом.\nА поки ви можете переглянути наш сайт."),
    'Selecciona que necesitas:': (
        'Selecciona què necessites:', 'Select what you need:', 'Sélectionnez ce dont vous avez besoin :', 'Wählen Sie, was Sie benötigen:',
        'Seleziona di cosa hai bisogno:', 'Selecteer wat je nodig hebt:', 'Выберите, что вам нужно:', 'Оберіть, що вам потрібно:'),
    'Consulta': ('Consulta', 'Consultation', 'Consultation', 'Beratung', 'Consulenza', 'Consult', 'Консультация', 'Консультація'),
    'Primera visita': ('Primera visita', 'First visit', 'Première visite', 'Erstbesuch', 'Prima visita', 'Eerste bezoek', 'Первый визит', 'Перший візит'),
    'Presupuesto Express': ('Pressupost exprés', 'Express quote', 'Devis express', 'Express-Kostenvoranschlag', 'Preventivo express', 'Express-offerte', 'Экспресс-расчёт стоимости', 'Експрес-розрахунок вартості'),
    'Promociones disponibles': ('Promocions disponibles', 'Current offers', 'Promotions disponibles', 'Aktuelle Angebote', 'Promozioni disponibili', 'Beschikbare aanbiedingen', 'Действующие акции', 'Актуальні акції'),
    '¡Gracias por tu consulta!\nEn breve nos pondremos en contacto contigo.': (
        'Gràcies per la teva consulta!\nEn breu ens posarem en contacte amb tu.', 'Thank you for your enquiry!\nWe will contact you shortly.',
        'Merci pour votre demande !\nNous vous contacterons très prochainement.', 'Vielen Dank für Ihre Anfrage!\nWir melden uns in Kürze bei Ihnen.',
        'Grazie per la tua richiesta!\nTi contatteremo a breve.', 'Bedankt voor je aanvraag!\nWe nemen binnenkort contact met je op.',
        'Спасибо за ваш запрос!\nМы свяжемся с вами в ближайшее время.', "Дякуємо за ваш запит!\nМи зв'яжемося з вами найближчим часом."),
    # ---- Paciente ideal (eQ3VBLE2)
    '¿Eres candidata/o ideal para una cirugía estética?': (
        'Ets candidata/o ideal per a una cirurgia estètica?', 'Are you an ideal candidate for cosmetic surgery?',
        'Êtes-vous un(e) candidat(e) idéal(e) pour une chirurgie esthétique ?', 'Sind Sie ein(e) ideale(r) Kandidat(in) für eine Schönheitsoperation?',
        'Sei la candidata/il candidato ideale per un intervento di chirurgia estetica?', 'Ben jij een ideale kandidaat voor esthetische chirurgie?',
        'Являетесь ли вы идеальным кандидатом для эстетической операции?', 'Чи є ви ідеальним кандидатом для естетичної операції?'),
    'El equipo médico te contactará': (
        "L'equip mèdic et contactarà", 'Our medical team will contact you', "L'équipe médicale vous contactera", 'Das Ärzteteam wird sich bei Ihnen melden',
        "L'équipe medica ti contatterà", 'Het medisch team neemt contact met je op', 'Медицинская команда свяжется с вами', "Медична команда зв'яжеться з вами"),
    '¿Qué intervención te estás planteando principalmente?': (
        "Quina intervenció t'estàs plantejant principalment?", 'Which procedure are you mainly considering?', 'Quelle intervention envisagez-vous principalement ?',
        'Welchen Eingriff ziehen Sie hauptsächlich in Betracht?', 'Quale intervento stai valutando principalmente?', 'Welke ingreep overweeg je voornamelijk?',
        'Какую операцию вы рассматриваете в первую очередь?', 'Яку операцію ви розглядаєте насамперед?'),
    'Abdominoplastia': ('Abdominoplàstia', 'Abdominoplasty', 'Abdominoplastie', 'Bauchdeckenstraffung', 'Addominoplastica', 'Buikwandcorrectie', 'Абдоминопластика', 'Абдомінопластика'),
    'Liposucción': ('Liposucció', 'Liposuction', 'Liposuccion', 'Fettabsaugung', 'Liposuzione', 'Liposuctie', 'Липосакция', 'Ліпосакція'),
    'Rinoplastia': ('Rinoplàstia', 'Rhinoplasty', 'Rhinoplastie', 'Nasenkorrektur', 'Rinoplastica', 'Neuscorrectie', 'Ринопластика', 'Ринопластика'),
    'Blefaroplastia (párpados)': ('Blefaroplàstia (parpelles)', 'Blepharoplasty (eyelids)', 'Blépharoplastie (paupières)', 'Lidstraffung (Augenlider)', 'Blefaroplastica (palpebre)', 'Ooglidcorrectie', 'Блефаропластика (веки)', 'Блефаропластика (повіки)'),
    '¿Cuál es el principal motivo por el que te planteas esta cirugía?': (
        'Quin és el principal motiu pel qual et planteges aquesta cirurgia?', 'What is the main reason you are considering this surgery?',
        'Quelle est la principale raison pour laquelle vous envisagez cette chirurgie ?', 'Was ist der Hauptgrund, warum Sie diese Operation in Betracht ziehen?',
        'Qual è il motivo principale per cui stai valutando questo intervento?', 'Wat is de belangrijkste reden waarom je deze operatie overweegt?',
        'Какова основная причина, по которой вы рассматриваете эту операцию?', 'Яка основна причина, з якої ви розглядаєте цю операцію?'),
    'Sentirme mejor conmigo misma/o': ('Sentir-me millor amb mi mateixa/mateix', 'To feel better about myself', 'Me sentir mieux dans ma peau', 'Mich in meiner Haut wohler fühlen', 'Sentirmi meglio con me stessa/o', 'Me beter voelen over mezelf', 'Чувствовать себя лучше', 'Почуватися краще'),
    'Corregir cambios tras embarazo o pérdida de peso': (
        "Corregir canvis després de l'embaràs o d'una pèrdua de pes", 'To correct changes after pregnancy or weight loss', 'Corriger des changements après une grossesse ou une perte de poids',
        'Veränderungen nach Schwangerschaft oder Gewichtsverlust korrigieren', 'Correggere i cambiamenti dopo una gravidanza o una perdita di peso', 'Veranderingen na zwangerschap of gewichtsverlies corrigeren',
        'Исправить изменения после беременности или потери веса', 'Виправити зміни після вагітності або втрати ваги'),
    'Estoy en un momento de cambio personal importante': (
        'Estic en un moment de canvi personal important', 'I am going through an important personal change', 'Je traverse un moment de changement personnel important',
        'Ich befinde mich in einer wichtigen Phase persönlicher Veränderung', 'Sto vivendo un momento di cambiamento personale importante', 'Ik zit in een belangrijke periode van persoonlijke verandering',
        'Я переживаю важный период личных перемен', 'Я переживаю важливий період особистих змін'),
    'Principalmente estético / por influencia externa': (
        'Principalment estètic / per influència externa', 'Mainly aesthetic / outside influence', 'Principalement esthétique / par influence extérieure',
        'Hauptsächlich ästhetisch / durch äußeren Einfluss', 'Principalmente estetico / per influenza esterna', 'Vooral esthetisch / door invloed van buitenaf',
        'В основном эстетическая / под влиянием окружающих', 'Переважно естетична / під впливом оточення'),
    'En cuanto al resultado, ¿con qué frase te identificas más?': (
        "Pel que fa al resultat, amb quina frase t'identifiques més?", 'Regarding the result, which statement do you identify with most?',
        'Concernant le résultat, à quelle phrase vous identifiez-vous le plus ?', 'Welche Aussage zum Ergebnis trifft am ehesten auf Sie zu?',
        'Per quanto riguarda il risultato, in quale frase ti riconosci di più?', 'Wat het resultaat betreft, in welke zin herken je je het meest?',
        'Что касается результата, какое утверждение вам ближе?', 'Щодо результату, яке твердження вам ближче?'),
    'Busco una mejora natural y proporcionada': (
        'Busco una millora natural i proporcionada', 'I want a natural, well-proportioned improvement', 'Je recherche une amélioration naturelle et proportionnée',
        'Ich suche eine natürliche, ausgewogene Verbesserung', 'Cerco un miglioramento naturale e proporzionato', 'Ik zoek een natuurlijke, evenwichtige verbetering',
        'Я хочу естественное и гармоничное улучшение', 'Я хочу природне та гармонійне покращення'),
    'Quiero un cambio visible pero acorde a mi cuerpo': (
        "Vull un canvi visible però d'acord amb el meu cos", 'I want a visible change that suits my body', 'Je veux un changement visible mais en accord avec mon corps',
        'Ich möchte eine sichtbare Veränderung, die zu meinem Körper passt', 'Voglio un cambiamento visibile ma in armonia con il mio corpo', 'Ik wil een zichtbare verandering die bij mijn lichaam past',
        'Я хочу заметное изменение, но соответствующее моему телу', 'Я хочу помітну зміну, але відповідну моєму тілу'),
    'Busco un resultado muy marcado o llamativo': (
        'Busco un resultat molt marcat o cridaner', 'I want a very pronounced or striking result', 'Je recherche un résultat très marqué ou spectaculaire',
        'Ich suche ein sehr ausgeprägtes oder auffälliges Ergebnis', 'Cerco un risultato molto marcato o appariscente', 'Ik zoek een heel uitgesproken of opvallend resultaat',
        'Я хочу очень выраженный или броский результат', 'Я хочу дуже виражений або помітний результат'),
    '¿En qué punto del proceso te encuentras ahora mismo?': (
        'En quin punt del procés et trobes ara mateix?', 'Where are you in the process right now?', 'Où en êtes-vous actuellement dans votre démarche ?',
        'An welchem Punkt des Prozesses stehen Sie gerade?', 'A che punto del percorso ti trovi in questo momento?', 'In welke fase van het proces zit je op dit moment?',
        'На каком этапе вы сейчас находитесь?', 'На якому етапі ви зараз перебуваєте?'),
    'Estoy informándome seriamente': ("M'estic informant seriosament", 'I am seriously looking into it', 'Je me renseigne sérieusement', 'Ich informiere mich ernsthaft', 'Mi sto informando seriamente', 'Ik ben me serieus aan het informeren', 'Я серьёзно изучаю вопрос', 'Я серйозно вивчаю питання'),
    'Quiero hacerlo en los próximos meses': ('Vull fer-ho en els propers mesos', 'I want to do it in the coming months', 'Je veux le faire dans les prochains mois', 'Ich möchte es in den nächsten Monaten machen', 'Voglio farlo nei prossimi mesi', 'Ik wil het in de komende maanden doen', 'Хочу сделать это в ближайшие месяцы', 'Хочу зробити це найближчими місяцями'),
    'Estoy comparando clínicas': ('Estic comparant clíniques', 'I am comparing clinics', 'Je compare des cliniques', 'Ich vergleiche Kliniken', 'Sto confrontando diverse cliniche', 'Ik vergelijk klinieken', 'Сравниваю клиники', 'Порівнюю клініки'),
    'Solo quiero información general por ahora': ('Només vull informació general de moment', 'I just want general information for now', 'Je veux seulement des informations générales pour le moment', 'Ich möchte vorerst nur allgemeine Informationen', 'Per ora voglio solo informazioni generali', 'Ik wil voorlopig alleen algemene informatie', 'Пока мне нужна только общая информация', 'Поки що мені потрібна лише загальна інформація'),
    'La consulta médica es un paso clave para valorar tu caso de forma personalizada.': (
        'La consulta mèdica és un pas clau per valorar el teu cas de manera personalitzada.', 'The medical consultation is a key step to assess your case individually.',
        'La consultation médicale est une étape clé pour évaluer votre cas de manière personnalisée.', 'Die ärztliche Beratung ist ein entscheidender Schritt, um Ihren Fall individuell zu beurteilen.',
        'La visita medica è un passaggio fondamentale per valutare il tuo caso in modo personalizzato.', 'Het medisch consult is een belangrijke stap om je situatie persoonlijk te beoordelen.',
        'Медицинская консультация — ключевой шаг для персональной оценки вашего случая.', 'Медична консультація — ключовий крок для персональної оцінки вашого випадку.'),
    'Lo considero imprescindible': ('Ho considero imprescindible', 'I consider it essential', 'Je la considère indispensable', 'Ich halte sie für unverzichtbar', 'La considero indispensabile', 'Ik vind het onmisbaar', 'Считаю её обязательной', "Вважаю її обов'язковою"),
    'Me interesa si es con un especialista de confianza': ("M'interessa si és amb un especialista de confiança", 'I am interested if it is with a trusted specialist', "Cela m'intéresse si c'est avec un spécialiste de confiance", 'Sie interessiert mich, wenn sie bei einem vertrauenswürdigen Spezialisten stattfindet', 'Mi interessa se è con uno specialista di fiducia', 'Ik heb interesse als het bij een betrouwbare specialist is', 'Мне интересно, если это надёжный специалист', 'Мені цікаво, якщо це надійний фахівець'),
    'Me genera algunas dudas': ('Em genera alguns dubtes', 'I have some doubts', "J'ai quelques doutes", 'Ich habe einige Zweifel', 'Ho qualche dubbio', 'Ik heb enkele twijfels', 'У меня есть некоторые сомнения', 'У мене є деякі сумніви'),
    'Aún no estoy segura/o': ("Encara no n'estic segura/segur", 'I am not sure yet', 'Je ne suis pas encore sûr(e)', 'Ich bin mir noch nicht sicher', 'Non sono ancora sicura/o', 'Ik weet het nog niet zeker', 'Пока не уверен(а)', 'Поки не впевнений(а)'),
    '¿Hay algún aspecto de tu salud o antecedentes que creas importante comentar?': (
        'Hi ha algun aspecte de la teva salut o antecedents que creguis important comentar?', 'Is there anything about your health or medical history you think is important to mention?',
        'Y a-t-il un aspect de votre santé ou de vos antécédents que vous jugez important de mentionner ?', 'Gibt es Aspekte Ihrer Gesundheit oder Vorgeschichte, die Sie für wichtig halten?',
        "C'è qualche aspetto della tua salute o della tua storia clinica che ritieni importante segnalare?", 'Is er iets over je gezondheid of medische voorgeschiedenis dat je belangrijk vindt om te vermelden?',
        'Есть ли что-то в вашем здоровье или анамнезе, о чём вы считаете важным сообщить?', "Чи є щось у вашому здоров'ї або анамнезі, про що ви вважаєте важливим повідомити?"),
    'No': ('No', 'No', 'Non', 'Nein', 'No', 'Nee', 'Нет', 'Ні'),
    'Sí (embarazos, cirugías previas, variaciones de peso, etc.)': (
        'Sí (embarassos, cirurgies prèvies, variacions de pes, etc.)', 'Yes (pregnancies, previous surgery, weight changes, etc.)', 'Oui (grossesses, chirurgies antérieures, variations de poids, etc.)',
        'Ja (Schwangerschaften, frühere Operationen, Gewichtsschwankungen usw.)', 'Sì (gravidanze, interventi precedenti, variazioni di peso, ecc.)', 'Ja (zwangerschappen, eerdere operaties, gewichtsschommelingen, enz.)',
        'Да (беременности, предыдущие операции, колебания веса и т. д.)', 'Так (вагітності, попередні операції, коливання ваги тощо)'),
    'Prefiero comentarlo directamente en consulta': ('Prefereixo comentar-ho directament a la consulta', 'I would rather discuss it at the consultation', "Je préfère en parler directement en consultation", 'Ich bespreche das lieber direkt in der Beratung', 'Preferisco parlarne direttamente in visita', 'Dat bespreek ik liever direct tijdens het consult', 'Предпочитаю обсудить это непосредственно на консультации', 'Волію обговорити це безпосередньо на консультації'),
    '¿Cuándo te gustaría, idealmente, realizar la consulta?': (
        "Quan t'agradaria, idealment, fer la consulta?", 'Ideally, when would you like to have the consultation?', 'Idéalement, quand souhaiteriez-vous réaliser la consultation ?',
        'Wann möchten Sie die Beratung idealerweise wahrnehmen?', 'Idealmente, quando vorresti fare la visita?', 'Wanneer zou je idealiter het consult willen doen?',
        'Когда бы вы хотели пройти консультацию в идеале?', 'Коли б ви хотіли пройти консультацію в ідеалі?'),
    'En las próximas semanas': ('En les properes setmanes', 'In the next few weeks', 'Dans les prochaines semaines', 'In den nächsten Wochen', 'Nelle prossime settimane', 'In de komende weken', 'В ближайшие недели', 'Найближчими тижнями'),
    'Más adelante, aún no lo tengo decidido': ('Més endavant, encara no ho tinc decidit', 'Later on, I have not decided yet', "Plus tard, je n'ai pas encore décidé", 'Später, ich habe mich noch nicht entschieden', 'Più avanti, non ho ancora deciso', 'Later, ik heb nog niets besloten', 'Позже, ещё не решил(а)', 'Пізніше, ще не вирішив(ла)'),
    'Gracias por tus respuestas.\n\nPor lo que nos indicas, una valoración médica personalizada puede ayudarte a resolver tus dudas y valorar tu caso con un especialista.\n\nEn Clínica Belba, nuestros doctores te acompañan desde la primera consulta hasta el postoperatorio, dentro del entorno del Grupo Teknon (clínica Premium)': (
        "Gràcies per les teves respostes.\n\nPel que ens indiques, una valoració mèdica personalitzada pot ajudar-te a resoldre els teus dubtes i valorar el teu cas amb un especialista.\n\nA Clínica Belba, els nostres doctors t'acompanyen des de la primera consulta fins al postoperatori, dins l'entorn del Grup Teknon (clínica Premium)",
        'Thank you for your answers.\n\nFrom what you tell us, a personalised medical assessment can help you resolve your doubts and evaluate your case with a specialist.\n\nAt Clínica Belba, our doctors are with you from the first consultation to the postoperative period, within the Teknon Group (premium clinic)',
        "Merci pour vos réponses.\n\nD'après ce que vous nous indiquez, une évaluation médicale personnalisée peut vous aider à résoudre vos doutes et à évaluer votre cas avec un spécialiste.\n\nÀ la Clínica Belba, nos médecins vous accompagnent de la première consultation jusqu'à la période postopératoire, au sein du Groupe Teknon (clinique Premium)",
        'Vielen Dank für Ihre Antworten.\n\nNach Ihren Angaben kann eine persönliche ärztliche Beurteilung Ihnen helfen, Ihre Fragen zu klären und Ihren Fall mit einem Spezialisten zu besprechen.\n\nIn der Clínica Belba begleiten Sie unsere Ärzte von der ersten Beratung bis zur Nachsorge, im Umfeld der Teknon-Gruppe (Premium-Klinik)',
        "Grazie per le tue risposte.\n\nDa quanto ci indichi, una valutazione medica personalizzata può aiutarti a risolvere i tuoi dubbi e a valutare il tuo caso con uno specialista.\n\nAlla Clínica Belba i nostri medici ti accompagnano dalla prima visita fino al post-operatorio, all'interno del Gruppo Teknon (clinica Premium)",
        'Bedankt voor je antwoorden.\n\nOp basis van wat je aangeeft, kan een persoonlijke medische beoordeling je helpen je twijfels weg te nemen en je situatie met een specialist te bespreken.\n\nBij Clínica Belba begeleiden onze artsen je van het eerste consult tot en met de nazorg, binnen de Teknon Groep (premium kliniek)',
        'Спасибо за ваши ответы.\n\nСудя по вашим ответам, персональная медицинская консультация поможет вам разрешить сомнения и оценить ваш случай со специалистом.\n\nВ клинике Belba наши врачи сопровождают вас от первой консультации до послеоперационного периода в рамках группы Teknon (премиум-клиника)',
        'Дякуємо за ваші відповіді.\n\nЗ огляду на ваші відповіді, персональна медична консультація допоможе вам розвіяти сумніви та оцінити ваш випадок із фахівцем.\n\nУ клініці Belba наші лікарі супроводжують вас від першої консультації до післяопераційного періоду в межах групи Teknon (преміум-клініка)'),
    'Solicta tu visita gratuita valorada en 150€': (
        'Sol·licita la teva visita gratuïta valorada en 150€', 'Request your free visit, worth €150', "Demandez votre visite gratuite d'une valeur de 150 €",
        'Fordern Sie Ihren kostenlosen Besuch im Wert von 150 € an', 'Richiedi la tua visita gratuita del valore di 150 €', 'Vraag je gratis bezoek ter waarde van € 150 aan',
        'Запросите бесплатный визит стоимостью 150 €', 'Запросіть безкоштовний візит вартістю 150 €'),
    'Nombre': ('Nom', 'First name', 'Prénom', 'Vorname', 'Nome', 'Voornaam', 'Имя', "Ім'я"),
    'Apellidos': ('Cognoms', 'Last name', 'Nom', 'Nachname', 'Cognome', 'Achternaam', 'Фамилия', 'Прізвище'),
    'Teléfono': ('Telèfon', 'Phone', 'Téléphone', 'Telefon', 'Telefono', 'Telefoon', 'Телефон', 'Телефон'),
    'Email': ('Email', 'Email', 'E-mail', 'E-Mail', 'Email', 'E-mail', 'Email', 'Email'),
}

_IDX = {l: i for i, l in enumerate(LANGS)}
_NORM = {k.strip(): v for k, v in X.items()}


def tr(lang, s):
    """Texto traducido para mostrar; si no hay traducción (o el idioma es es), el literal en español."""
    if not s or lang == 'es' or lang not in _IDX:
        return s
    row = X.get(s) or _NORM.get(s.strip())
    return row[_IDX[lang]] if row else s


def faltan():
    """Textos de typeform_forms.json sin traducción (para comprobar en el pipeline)."""
    import json, os
    B = os.environ.get('BELBA_ROOT', '/home/claude/belba')
    TF = json.load(open(B + '/migracion/typeform_forms.json', encoding='utf-8'))
    out = set()
    for f in TF.values():
        for x in f['fields']:
            if x['lvl'] == 0 and x['type'] != 'contact_info' and x['title'] and tr('en', x['title']) == x['title']:
                out.add(x['title'])
            if x['type'] == 'contact_info' and x['title'] and tr('en', x['title']) == x['title']:
                out.add(x['title'])
            for c in x['choices']:
                if tr('en', c) == c and c != 'No':
                    out.add(c)
        for w in (f.get('welcome') or []):
            if w and tr('en', w) == w:
                out.add(w)
        t = f.get('thanks_text') or ''
        if t and not t.startswith('http') and '{{' not in t and tr('en', t) == t:
            out.add(t)
    return sorted(out)


if __name__ == '__main__':
    print('sin traducción:', faltan())
