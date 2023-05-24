# from datetime import datetime, timedelta

# weekDaysDates = datetime.today().weekday()
# print(weekDaysDates)



# def create_dict(dict_name, value_input):
#     # create small dict
#     dict_name = {}
#     key = 'UpdateDate'
#     value = value_input
#     dict_name[key] = value

import deepl

auth_key = "ad34c11c-d02c-6496-4ee5-7c52693f6a31:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

a = ['Porkkana-rakuunakeitto', '12,90 €', '', 'Napolilainen kasvisragu', '14,90 €', 'sekä cavatappi pastaa, saa pyydettäessä gluteenittomana', 'Härkäragu', '14,90 €', 'sekä cavatappi pastaa, saa pyydettäessä gluteenittomana']

result = translator.translate_text(f"{a}", target_lang="RU")
print(result.text)  # "Bonjour, le monde !"