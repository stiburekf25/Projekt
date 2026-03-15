import json
import os

def uloz_hru():
    pozadi_na_jmeno_save = {
        id(rozcestnik): "rozcestnik",
        id(venek): "venek",
        id(jezero): "jezero",
        id(dum): "dum",
        id(krb): "krb",
        id(garaz): "garaz",
        id(les): "les",
        id(cesta_pred_lesem): "cesta_pred_lesem",
        id(bar): "bar",
    }
    
    data = {
        "coins": coins,
        "hlad": hlad,
        "zizen": zizen,
        "deprese": deprese,
        "hrac_pozice_x": hrac_pozice_x,
        "hrac_pozice_y": hrac_pozice_y,
        "kamera_x": kamera_x,
        "pozadi": pozadi_na_jmeno_save.get(id(pozadi), "rozcestnik"),
        
        # inventar
        "obsah_inventare": obsah_inventare,
        "obsah_inventare_max": obsah_inventare_max,
        "inventar_order": [p["jmeno"] for p in inventar_order],
        
        # upgrady rybareni
        "kyblik_lvl": kyblik_lvl,
        "zmacknuti_lvl": zmacknuti_lvl,
        "cekani_lvl": cekani_lvl,
        "momentalni_cekani": momentalni_cekani,
        
        # baits
        "baits": {k: v["pocet"] for k, v in baits.items()},
        "baits_lvl": baits_lvl,
        "obsah_baits_max": obsah_baits_max,
        
        # mazlicek
        "mazlicek_odemceny": mazlicek_odemceny,
        "mazlicek_equipped": mazlicek_equipped,
        
        # boruvky
        "boruvky_pocet_v_inv": boruvky_pocet_v_inv,
        "boruvky_respawn_delay": boruvky_respawn_delay,
        "boruvky_visible": [b[2] for b in boruvky],
        "kosik_upgrade_level": kosik_upgrade_level,
        "sber_vice_boruvek_upgrade_level": sber_vice_boruvek_upgrade_level,
        "cekani_boruvky_upgrade_level": cekani_boruvky_upgrade_level,
        "pocet_boruvek_pri_sebrani": pocet_boruvek_pri_sebrani,
        "max_kosik_na_boruvky": max_kosik_na_boruvky,
        "cena_kosik_na_boruvky": cena_kosik_na_boruvky,
        "cena_sber_vice_boruvek": cena_sber_vice_boruvek,
        "cena_cekani_na_boruvky": cena_cekani_na_boruvky,
        
        # quest kytky
        "start_questu": start_questu,
        "levandule": levandule,
        "ruze": ruze,
        "tulipan": tulipan,
        "pocet_levanduli": pocet_levanduli,
        "pocet_ruzi": pocet_ruzi,
        "pocet_tulipanu": pocet_tulipanu,
        "levandule_pozice_visible": [l[2] for l in levandule_pozice],
        "ruze_pozice_visible": [r[2] for r in ruze_pozice],
        "tulipan_pozice_visible": [t[2] for t in tulipan_pozice],
        
        # auto
        "pneumatiky_inv_pocet": pneumatiky_inv_pocet,
        "benzin_inv_pocet": benzin_inv_pocet,
        "motor_inv_pocet": motor_inv_pocet,
        "brzdy_inv_pocet": brzdy_inv_pocet,
        "fixed_pneumatiky_pocet": fixed_pneumatiky_pocet,
        "fixed_benzin_pocet": fixed_benzin_pocet,
        "fixed_brzdy_pocet": fixed_brzdy_pocet,
        "fixed_motor_pocet": fixed_motor_pocet,
        "maxed_out_pneumatiky": maxed_out_pneumatiky,
        "maxed_out_benzin": maxed_out_benzin,
        "maxed_out_brzdy": maxed_out_brzdy,
        "maxed_out_motor": maxed_out_motor,
        "pneumatiky_pocet": pneumatiky_pocet,
        "benzin_pocet": benzin_pocet,
        "motor_pocet": motor_pocet,
        "brzdy_pocet": brzdy_pocet,
    }
    
    with open("save.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
def nacti_hru():
    global coins, hlad, zizen, deprese
    global hrac_pozice_x, hrac_pozice_y, kamera_x, pozadi
    global obsah_inventare, obsah_inventare_max, inventar_order
    global kyblik_lvl, zmacknuti_lvl, cekani_lvl, momentalni_cekani
    global baits, baits_lvl, obsah_baits_max
    global mazlicek_odemceny, mazlicek_equipped
    global boruvky_pocet_v_inv, boruvky_respawn_delay, boruvky
    global kosik_upgrade_level, sber_vice_boruvek_upgrade_level, cekani_boruvky_upgrade_level
    global pocet_boruvek_pri_sebrani, max_kosik_na_boruvky
    global cena_kosik_na_boruvky, cena_sber_vice_boruvek, cena_cekani_na_boruvky
    global start_questu, levandule, ruze, tulipan
    global pocet_levanduli, pocet_ruzi, pocet_tulipanu
    global levandule_pozice, ruze_pozice, tulipan_pozice
    global pneumatiky_inv_pocet, benzin_inv_pocet, motor_inv_pocet, brzdy_inv_pocet
    global fixed_pneumatiky_pocet, fixed_benzin_pocet, fixed_brzdy_pocet, fixed_motor_pocet
    global maxed_out_pneumatiky, maxed_out_benzin, maxed_out_brzdy, maxed_out_motor
    global pneumatiky_pocet, benzin_pocet, motor_pocet, brzdy_pocet
    global pozadi_sirka, pozadi_vyska
    

    if not os.path.exists("save.json"):
        return False
    
    with open("save.json", "r", encoding="utf-8") as f:
        d = json.load(f)
        
    jmeno_na_pozadi = {
        "rozcestnik": rozcestnik, "venek": venek, "jezero": jezero,
        "dum": dum, "krb": krb, "garaz": garaz,
        "les": les, "cesta_pred_lesem": cesta_pred_lesem, "bar": bar,
    }
    
    coins = d["coins"]
    hlad = d["hlad"]
    zizen = d["zizen"]
    deprese = d["deprese"]
    hrac_pozice_x = d["hrac_pozice_x"]
    hrac_pozice_y = d["hrac_pozice_y"]
    kamera_x = d["kamera_x"]
    pozadi = jmeno_na_pozadi.get(d["pozadi"], rozcestnik)
    pozadi_sirka = pozadi.get_width()
    pozadi_vyska = pozadi.get_height()
    
    obsah_inventare = d["obsah_inventare"]
    obsah_inventare_max = d["obsah_inventare_max"]
    inventar_order = []
    for jmeno in d["inventar_order"]:
        predmet = najdi_predmet_podle_jmena(predmety, jmeno)
        if predmet:
            inventar_order.append(predmet)
    
    kyblik_lvl = d["kyblik_lvl"]
    zmacknuti_lvl = d["zmacknuti_lvl"]
    cekani_lvl = d["cekani_lvl"]
    momentalni_cekani = d["momentalni_cekani"]
    
    for k in baits:
        baits[k]["pocet"] = d["baits"][k]
    baits_lvl = d["baits_lvl"]
    obsah_baits_max = d["obsah_baits_max"]
    
    mazlicek_odemceny = d["mazlicek_odemceny"]
    mazlicek_equipped = d["mazlicek_equipped"]
    
    boruvky_pocet_v_inv = d["boruvky_pocet_v_inv"]
    boruvky_respawn_delay = d["boruvky_respawn_delay"]
    for i, vis in enumerate(d["boruvky_visible"]):
        boruvky[i][2] = vis
    kosik_upgrade_level = d["kosik_upgrade_level"]
    sber_vice_boruvek_upgrade_level = d["sber_vice_boruvek_upgrade_level"]
    cekani_boruvky_upgrade_level = d["cekani_boruvky_upgrade_level"]
    pocet_boruvek_pri_sebrani = d["pocet_boruvek_pri_sebrani"]
    max_kosik_na_boruvky = d["max_kosik_na_boruvky"]
    cena_kosik_na_boruvky = d["cena_kosik_na_boruvky"]
    cena_sber_vice_boruvek = d["cena_sber_vice_boruvek"]
    cena_cekani_na_boruvky = d["cena_cekani_na_boruvky"]
    
    start_questu = d["start_questu"]
    levandule = d["levandule"]
    ruze = d["ruze"]
    tulipan = d["tulipan"]
    pocet_levanduli = d["pocet_levanduli"]
    pocet_ruzi = d["pocet_ruzi"]
    pocet_tulipanu = d["pocet_tulipanu"]
    for i, vis in enumerate(d["levandule_pozice_visible"]):
        levandule_pozice[i][2] = vis
    for i, vis in enumerate(d["ruze_pozice_visible"]):
        ruze_pozice[i][2] = vis
    for i, vis in enumerate(d["tulipan_pozice_visible"]):
        tulipan_pozice[i][2] = vis
    
    pneumatiky_inv_pocet = d["pneumatiky_inv_pocet"]
    benzin_inv_pocet = d["benzin_inv_pocet"]
    motor_inv_pocet = d["motor_inv_pocet"]
    brzdy_inv_pocet = d["brzdy_inv_pocet"]
    fixed_pneumatiky_pocet = d["fixed_pneumatiky_pocet"]
    fixed_benzin_pocet = d["fixed_benzin_pocet"]
    fixed_brzdy_pocet = d["fixed_brzdy_pocet"]
    fixed_motor_pocet = d["fixed_motor_pocet"]
    maxed_out_pneumatiky = d["maxed_out_pneumatiky"]
    maxed_out_benzin = d["maxed_out_benzin"]
    maxed_out_brzdy = d["maxed_out_brzdy"]
    maxed_out_motor = d["maxed_out_motor"]
    pneumatiky_pocet = d["pneumatiky_pocet"]
    benzin_pocet = d["benzin_pocet"]
    motor_pocet = d["motor_pocet"]
    brzdy_pocet = d["brzdy_pocet"]
    
    return True