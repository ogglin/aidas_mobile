from google_translate_new import google_translator

from db import _query


def set_classy_view(id):
    _query(f"""UPDATE advertise SET views = 
                (SELECT * FROM (SELECT views + 1 FROM advertise WHERE id = {id}) as adv) WHERE id = {id};""")


def update_translate(cid, text):
    _query(f"""UPDATE advertise SET newspaper_content_en = '{text}' WHERE id = {cid}""")


def get_categories(site_id):
    q = _query(f"""SELECT categories.*, categories_translate.title FROM categories 
                        LEFT JOIN categories_translate ON categories.id = categories_translate.categories_id 
                        and categories_translate.language_id = {site_id};""")
    return q


def get_all_classy(site_id):
    issue = int(_query(f"""SELECT svalue FROM core.settings WHERE id = {site_id};""")[0]['svalue'])
    if int(site_id) == 1:
        template_ids = '(1, 2, 7)'
    elif int(site_id) == 2:
        template_ids = '(3, 4)'
    else:
        template_ids = '(1, 2, 7)'

    tClassies = _query(f"""SELECT * FROM advertise WHERE advertise_template_id in {template_ids} 
                AND newspaper_content_en is null and active = 1 and is_paid = 1 and end_issue >= {issue};""")
    translator = google_translator()
    for tClassy in tClassies:
        print(tClassy['newspaper_content'])
        translate_text = translator.translate(tClassy['newspaper_content'], lang_tgt='en')
        print(translate_text)
        update_translate(int(tClassy['id']), translate_text.replace("'", '"'))
    q = f"""SELECT advertise.id, advertise.categories_id, advertise.newspaper_content, 
        advertise.newspaper_content_en, advertise.views, advertise.created, 
        GROUP_CONCAT('serv', services.id  SEPARATOR ' ') as services FROM advertise
        LEFT JOIN services_has_advertise sha ON sha.advertise_id = advertise.id
        LEFT JOIN services ON services.id = sha.services_id
        WHERE advertise.active = 1 and advertise.advertise_template_id in {template_ids} 
        and advertise.end_issue >= {issue} 
        GROUP BY advertise.id
        ORDER BY case when services.id = 4 then 0 when services.id = 6 then 1 else 3 end, advertise.id DESC;"""
    res = _query(q)
    print(res)
    return res
