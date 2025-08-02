"""Entry point for scraping app statistics from Google Play and the App Store."""

import datetime
import pandas as pd

import selenium_scraper as google_scraper
import appstore_scraper

APP_IDS = {
    "TBC UZ": {
        "google": "ge.space.app.uzbekistan",
        "google_tablet": True,
        "appstore": "tbc-uz-online-mobile-banking/id1450503714",
    },
    "Kapitalbank": {
        "google": "uz.kapitalbank.kbonline",
        "google_tablet": True,
        "appstore": "kapitalbank-online/id1546213356",
    },
    "Hamkorbank": {
        "google": "com.hamkorbank.mobile",
        "google_tablet": False,
        "appstore": "hamkor/id1602323485",
    },
    "Ipak Yuli Bank": {
        "google": "com.ipakyulibank.mobile",
        "google_tablet": True,
        "appstore": "ipak-yoli-mobile/id1436677359",
    },
    "ANOR BANK": {
        "google": "uz.anormobile.retail",
        "google_tablet": True,
        "appstore": "anorbank/id1579623268",
    },
    "DAVR BANK": {
        "google": "uz.davrbank.mobile",
        "google_tablet": False,
        "appstore": "davr-mobile-2-0/id6483247810",
    },
    "MKBANK": {
        "google": "uz.tune.mkbdbo",
        "google_tablet": False,
        "appstore": "mavrid/id6445884560",
    },
    "Tenge Bank": {
        "google": "uz.tune.tenge",
        "google_tablet": True,
        "appstore": "tenge24/id1586139053",
    },
    "AVO Bank": {
        "google": "uz.avo.app",
        "google_tablet": True,
        "appstore": "avo-onlayn-bank-ozbekiston/id6463799850",
    },
    "Turon Bank": {
        "google": "com.colvir.turon.mobile",
        "google_tablet": False,
        "appstore": "my-turon/id1639122039",
    },
    "Trustbank": {
        "google": "trastpay.uz",
        "google_tablet": True,
        "appstore": "trastpay/id6443658536",
    },
    "Ipoteka Bank": {
        "google": "com.bss.ipotekabank.retail.lite",
        "google_tablet": True,
        "appstore": "ipoteka-retail/id1637057203",
    },
    "Asakabank": {
        "google": "uz.asakabank.myasaka",
        "google_tablet": True,
        "appstore": "asakabank/id1574165416",
    },
    "OFB": {
        "google": "uz.ofbmobile.android",
        "google_tablet": False,
        "appstore": "ofb/id6443708765",
    },
    "InfinBANK": {
        "google": "uz.xsoft.myinfin",
        "google_tablet": True,
        "appstore": "infinbank/id1454367354",
    },
    "Payme": {
        "google": "uz.dida.payme",
        "google_tablet": True,
        "appstore": "payme-переводы-и-платежи/id1093525667",
    },
    "Click": {
        "google": "air.com.ssdsoftwaresolutions.clickuz",
        "google_tablet": True,
        "appstore": "click-superapp/id768132591",
    },
    "Paynet": {
        "google": "uz.paynet.app",
        "google_tablet": True,
        "appstore": "paynet-переводы-платежи/id1307888692",
    },
    "Alif Mobi": {
        "google": "tj.alif.mobi",
        "google_tablet": True,
        "appstore": "alif-mobi-платежи-и-переводы/id1331374853",
    },
    "Oson": {
        "google": "com.oson",
        "google_tablet": True,
        "appstore": "oson-платежи-и-переводы/id1207834182",
    },
    "Uzum Bank": {
        "google": "uz.kapitalbank.android",
        "google_tablet": True,
        "appstore": "uzum-bank-onlayn-ozbekiston/id1492307726",
    },
    "Beepul": {
        "google": "com.olsoft.mats.prod",
        "google_tablet": True,
        "appstore": "beepul/id1168589903",
    },
    "Xazna": {
        "google": "uz.tune.xazna",
        "google_tablet": True,
        "appstore": "xazna/id1642489915",
    },
    "Aloqabank": {
        "google": "uz.aloqabank.zoomrad",
        "google_tablet": True,
        "appstore": "zoomrad/id1522419775",
    },
    # НОВОЕ ПРИЛОЖЕНИЕ С 15.05
    "AAB": {
        "google": "uz.tune.juicer",
        "google_tablet": False,
        "appstore": "alliance-pay/id6469618319",
    },
    "Agrobank": {
        "google": "uz.agrobank.mobile",
        "google_tablet": True,
        "appstore": "agrobank-mobile/id1638716474",
    },
    #  для AppStore - левый адрес, у банка судя по всему нет AppStore (данные не выгружаются)
    "Apex Bank": {
        "google": "com.fincube.apexbank",
        "google_tablet": False,
        "appstore": "apex-bank/id1128362996",
    },
    "BDB": {
        "google": "com.qqb.quant",
        "google_tablet": True,
        "appstore": "brb/id1524422825",
    },
    "Garant Bank": {
        "google": "uz.comsa.garant.mobile",
        "google_tablet": False,
        "appstore": "garant-bank-узбекистан/id6476410628",
    },
    "Hayot Bank": {
        "google": "uz.cbssolutions.mobile",
        "google_tablet": False,
        "appstore": "hayot-bank/id6468219656",
    },
    "KDB Bank": {
        "google": "app.mobile.kdb",
        "google_tablet": False,
        "appstore": "kdbuz-mobile/id6448983924",
    },
    "NBU": {
        "google": "com.tune.milliy",
        "google_tablet": True,
        "appstore": "milliy/id1297283006",
    },
    "SQB": {
        "google": "com.uzpsb.olam",
        "google_tablet": True,
        "appstore": "sqb-mobile/id1499606946",
    },
    "Octobank": {
        "google": "com.ravnaqbank.rbkmobile",
        "google_tablet": True,
        "appstore": "octo-mobile/id1460141475",
    },
    "Smart Bank": {
        "google": "uz.smartbank",
        "google_tablet": True,
        "appstore": "smartbank-uz-onlayn-bank/id6446754221",
    },
    "Universal Bank": {
        "google": "uz.fido.universaldigital",
        "google_tablet": False,
        "appstore": "universalbank/id6453759395",
    },
    "Yangi Bank": {
        "google": "uz.yangi.finance",
        "google_tablet": True,
        "appstore": "yangi-online-banking-loans/id1644376437",
    },
    # 'Ziraat Bank': {
    # 'google': 'uz.ziraat.mobile',
    # 'google_tablet': False,
    # 'appstore': 'ziraat-mobile-uzbekistan/id1540767956'
    # }
    # ,
    "ATTO": {
        "google": "uz.genesis.asop",
        "google_tablet": True,
        "appstore": "atto/id1492486731",
    },
    "Uzum Nasiya": {
        "google": "uz.paymart.paymart_mobile",
        "google_tablet": True,
        "appstore": "uzum-nasiya-muddatli-tolov/id1579281935",
    },
    "hambi": {
        "google": "uz.beeline.odp",
        "google_tablet": True,
        "appstore": "hambi-beeline-uzbekistan/id722072887",
    },
    "Humans": {
        "google": "net.humans.fintech_uz",
        "google_tablet": True,
        "appstore": "humans-uz/id1508198703",
    },
    "Kaspi.kz": {
        "google": "kz.kaspi.mobile",
        "google_tablet": True,
        "appstore": "kaspi-kz-суперприложение/id1195076505",
    },
    "Nu Bank": {
        "google": "com.nu.production",
        "google_tablet": True,
        "appstore": "nu-financial-services/id814456780",
    },
    "Monzo": {
        "google": "co.uk.getmondo",
        "google_tablet": True,
        "appstore": "monzo-mobile-banking/id1052238659",
    },
    "bunq": {
        "google": "com.bunq.android",
        "google_tablet": True,
        "appstore": "bunq/id1021178150",
    },
    "N26": {
        "google": "de.number26.android",
        "google_tablet": True,
        "appstore": "n26-love-your-bank/id956857223",
    },
    "Revolut": {
        "google": "com.revolut.revolut",
        "google_tablet": True,
        "appstore": "revolut-send-spend-and-save/id932493382",
    },
    "Wise": {
        "google": "com.transferwise.android",
        "google_tablet": True,
        "appstore": "wise/id612261027",
    },
    "Kakao Bank": {
        "google": "com.kakaobank.channel",
        "google_tablet": False,
        "appstore": "카카오뱅크/id1258016944",
    },
    # 'Affirm': {
    # 'google': 'com.affirm.central',
    # 'google_tablet': True,
    # 'appstore': 'affirm-buy-now-pay-over-time/id967040652'
    # },
    # 'Block': {
    # 'google': 'com.squareup',
    # 'google_tablet': True,
    # 'appstore': 'square-point-of-sale-pos/id335393788'
    # }
}


def main() -> None:
    """Collect statistics for all banks and export them to an Excel file."""
    driver = google_scraper.Main_driver(headless=True)

    google_result = pd.DataFrame()
    google_updates_result = pd.DataFrame()
    appstore_result = pd.DataFrame()
    appstore_updates_result = pd.DataFrame()

    for bank, ids in APP_IDS.items():
        print()
        print("Bank: ", bank)
        google_data, google_updates = driver.get_data_by_id(
            name=bank, app_id=ids["google"], tablet=ids["google_tablet"]
        )
        appstore_data, appstore_updates = appstore_scraper.get_app_data(
            bank, ids["appstore"]
        )
        google_result = pd.concat([google_result, google_data])
        google_updates_result = pd.concat([google_updates_result, google_updates])
        appstore_result = pd.concat([appstore_result, appstore_data])
        appstore_updates_result = pd.concat([appstore_updates_result, appstore_updates])

    driver.driver_quit()

    result = pd.concat([google_result, appstore_result])
    result = result.pivot_table(
        index=["bank", "device"], columns="rating", aggfunc=lambda x: x
    )
    result = result.reset_index()
    cols_to_move = result.columns[2:8]
    remaining_cols = result.columns.difference(cols_to_move)
    new_order = list(remaining_cols) + list(cols_to_move)
    result = result[new_order[:-1]]
    result.columns = [
        "bank",
        "device",
        1,
        2,
        3,
        4,
        5,
        "google_total_installs",
        "apple_total_review_count",
        1,
        2,
        3,
        4,
        5,
    ]
    updates_result = pd.concat([google_updates_result, appstore_updates_result])
    result = result.merge(updates_result, how="left", on=["bank", "device"])

    result.to_excel(
        rf"./app_data {datetime.date.today().isoformat()}.xlsx", index=False
    )


if __name__ == "__main__":
    main()
