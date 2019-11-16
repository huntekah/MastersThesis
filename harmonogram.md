Co mamy:
2,
prawie 4
prawie 5 - Vue
7 token może wyglądać jako <|endoftext|>, ale w sumie powinno działać

przyrost 0 - pokazać to, co mam
przyrost 1  - działający backend do zwracania jsona z podpowiedziami 10-ciu tokenów
            - ui w swaggerze
            o


Roman - zbiór do korekty gramatycznej. Zrobić z tego wyzwanie na gonito i zrobić z tego 2 rodzaje wyzwań - korekta gramatyczna oraz model detekcji błędu.


metryka f1, f0.5, f2? poczytać

dodać Bert oraz Gpt2, mozna tez sprobowac je polaczyc

paper dt. korekcji nienadzorowanej. (Konferencja ACL)

narzędzie do testowania - odballnes mozna podnosic do kwadratu


współczynik do oddballnes można dobrać testowo (kwadrat czy coś) przed sumą
        oddballness = torch.sum( KWADRAT(   F.relu(tokens_proba - chosen_token_proba)  ) )

