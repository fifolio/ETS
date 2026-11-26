import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from appwrite.exception import AppwriteException

ROWS = [
    ("usd", "US Dollar", "$", 1.0),
    ("eur", "Euro", "€", 0.908584),
    ("gbp", "British Pound", "£", 0.758255),
    ("cad", "Canadian Dollar", "CA$", 1.40),
    ("aud", "Australian Dollar", "A$", 1.54),
    ("inr", "Indian Rupee", "₹", 93.959855),
    ("tnd", "Tunisian Dinar", "DT", 3.033810),
    ("egp", "Egyptian Pound", "E£", 53.681178),
    ("sar", "Saudi Riyal", "SR", 3.750000),
    ("aed", "UAE Dirham", "د.إ", 3.672500),
    ("mad", "Moroccan Dirham", "DH", 9.972541),
    ("dzd", "Algerian Dinar", "DA", 136.975866),
    ("brl", "Brazilian Real", "R$", 5.32),
    ("mxn", "Mexican Peso", "MX$", 18.30),
    ("jpy", "Japanese Yen", "¥", 159.580113),
    ("cny", "Chinese Yuan", "¥", 7.10),
    ("krw", "South Korean Won", "₩", 1460.0),
    ("idr", "Indonesian Rupiah", "Rp", 16600.0),
    ("bdt", "Bangladeshi Taka", "৳", 122.0),
    ("pkr", "Pakistani Rupee", "Rs", 280.0),
    ("ngn", "Nigerian Naira", "₦", 1450.0),
    ("zar", "South African Rand", "R", 17.0),
    ("try", "Turkish Lira", "₺", 42.0),
    ("pln", "Polish Zloty", "zł", 3.65),
    ("sek", "Swedish Krona", "kr", 9.45),
    ("chf", "Swiss Franc", "Fr", 0.80),
    ("nok", "Norwegian Krone", "kr", 9.80),
    ("dkk", "Danish Krone", "kr", 6.78),
    ("sgd", "Singapore Dollar", "S$", 1.29),
    ("hkd", "Hong Kong Dollar", "HK$", 7.80),
    # North America and Caribbean
    ("gtq", "Guatemalan Quetzal", "Q", 7.65),
    ("hnl", "Honduran Lempira", "L", 26.50),
    ("nio", "Nicaraguan Córdoba", "C$", 36.80),
    ("crc", "Costa Rican Colón", "₡", 510.0),
    ("pab", "Panamanian Balboa", "B/.", 1.0),
    ("bzd", "Belize Dollar", "BZ$", 2.0),
    ("bsd", "Bahamian Dollar", "B$", 1.0),
    ("jmd", "Jamaican Dollar", "J$", 160.0),
    ("dop", "Dominican Peso", "RD$", 63.0),
    ("htg", "Haitian Gourde", "G", 130.0),
    ("ttd", "Trinidad and Tobago Dollar", "TT$", 6.78),
    ("xcd", "East Caribbean Dollar", "EC$", 2.70),
    ("bbd", "Barbadian Dollar", "Bds$", 2.0),
    ("awg", "Aruban Florin", "ƒ", 1.79),
    ("ang", "Netherlands Antillean Guilder", "ƒ", 1.79),
    ("cup", "Cuban Peso", "$", 24.0),
    # South America
    ("ars", "Argentine Peso", "$", 1450.0),
    ("clp", "Chilean Peso", "$", 930.0),
    ("cop", "Colombian Peso", "$", 3800.0),
    ("pen", "Peruvian Sol", "S/", 3.40),
    ("uyu", "Uruguayan Peso", "$U", 40.0),
    ("pyg", "Paraguayan Guaraní", "₲", 7300.0),
    ("bob", "Bolivian Boliviano", "Bs", 6.96),
    ("ves", "Venezuelan Bolívar", "Bs.", 200.0),
    ("gyd", "Guyanese Dollar", "G$", 209.0),
    ("srd", "Surinamese Dollar", "$", 38.0),
    # Europe
    ("czk", "Czech Koruna", "Kč", 21.0),
    ("huf", "Hungarian Forint", "Ft", 335.0),
    ("ron", "Romanian Leu", "lei", 4.50),
    ("bgn", "Bulgarian Lev", "лв", 1.78),
    ("isk", "Icelandic Krona", "kr", 124.0),
    ("all", "Albanian Lek", "L", 82.0),
    ("rsd", "Serbian Dinar", "дин.", 106.0),
    ("bam", "Bosnia Convertible Mark", "KM", 1.78),
    ("mkd", "Macedonian Denar", "ден", 56.0),
    ("mdl", "Moldovan Leu", "L", 17.0),
    ("uah", "Ukrainian Hryvnia", "₴", 42.0),
    ("byn", "Belarusian Ruble", "Br", 3.0),
    ("rub", "Russian Ruble", "₽", 80.0),
    ("gel", "Georgian Lari", "₾", 2.70),
    ("amd", "Armenian Dram", "֏", 385.0),
    ("azn", "Azerbaijani Manat", "₼", 1.70),
    # Middle East and Africa
    ("lyd", "Libyan Dinar", "LD", 5.40),
    ("sdg", "Sudanese Pound", "ج.س", 600.0),
    ("ssp", "South Sudanese Pound", "£", 4500.0),
    ("mru", "Mauritanian Ouguiya", "UM", 40.0),
    ("djf", "Djiboutian Franc", "Fdj", 178.0),
    ("sos", "Somali Shilling", "Sh", 570.0),
    ("kmf", "Comorian Franc", "CF", 447.0),
    ("ern", "Eritrean Nakfa", "Nfk", 15.0),
    ("etb", "Ethiopian Birr", "Br", 155.0),
    ("qar", "Qatari Riyal", "QR", 3.64),
    ("kwd", "Kuwaiti Dinar", "KD", 0.31),
    ("bhd", "Bahraini Dinar", "BD", 0.38),
    ("omr", "Omani Rial", "OMR", 0.385),
    ("yer", "Yemeni Rial", "﷼", 250.0),
    ("iqd", "Iraqi Dinar", "IQD", 1310.0),
    ("jod", "Jordanian Dinar", "JD", 0.709),
    ("lbp", "Lebanese Pound", "L£", 89500.0),
    ("ils", "Israeli New Shekel", "₪", 3.25),
    ("irr", "Iranian Rial", "﷼", 42000.0),
    ("ghs", "Ghanaian Cedi", "₵", 11.0),
    ("kes", "Kenyan Shilling", "KSh", 129.0),
    ("tzs", "Tanzanian Shilling", "TSh", 2450.0),
    ("ugx", "Ugandan Shilling", "USh", 3600.0),
    ("rwf", "Rwandan Franc", "RF", 1450.0),
    ("bif", "Burundian Franc", "FBu", 3000.0),
    ("cdf", "Congolese Franc", "FC", 2300.0),
    ("xof", "West African CFA Franc", "CFA", 596.0),
    ("xaf", "Central African CFA Franc", "FCFA", 596.0),
    ("mga", "Malagasy Ariary", "Ar", 4500.0),
    ("mur", "Mauritian Rupee", "₨", 46.0),
    ("scr", "Seychellois Rupee", "₨", 14.0),
    ("zmw", "Zambian Kwacha", "ZK", 24.0),
    ("mwk", "Malawian Kwacha", "MK", 1750.0),
    ("bwp", "Botswana Pula", "P", 13.5),
    ("nad", "Namibian Dollar", "N$", 17.0),
    ("szl", "Swazi Lilangeni", "E", 17.0),
    ("lsl", "Lesotho Loti", "L", 17.0),
    ("mzn", "Mozambican Metical", "MT", 64.0),
    ("aoa", "Angolan Kwanza", "Kz", 920.0),
    ("cve", "Cape Verdean Escudo", "$", 101.0),
    ("stn", "São Tomé and Príncipe Dobra", "Db", 22.0),
    ("gnf", "Guinean Franc", "FG", 8600.0),
    ("gmd", "Gambian Dalasi", "D", 72.0),
    ("sll", "Sierra Leonean Leone", "Le", 23000.0),
    ("lrd", "Liberian Dollar", "L$", 180.0),
    # Asia
    ("npr", "Nepalese Rupee", "रू", 150.0),
    ("lkr", "Sri Lankan Rupee", "Rs", 300.0),
    ("afn", "Afghan Afghani", "؋", 68.0),
    ("kpw", "North Korean Won", "₩", 900.0),
    ("twd", "New Taiwan Dollar", "NT$", 31.5),
    ("mop", "Macanese Pataca", "MOP$", 8.0),
    ("myr", "Malaysian Ringgit", "RM", 4.20),
    ("thb", "Thai Baht", "฿", 32.0),
    ("vnd", "Vietnamese Dong", "₫", 26000.0),
    ("php", "Philippine Peso", "₱", 58.0),
    ("khr", "Cambodian Riel", "៛", 4000.0),
    ("lak", "Lao Kip", "₭", 22000.0),
    ("mmk", "Myanmar Kyat", "K", 2100.0),
    ("bnd", "Brunei Dollar", "B$", 1.29),
    ("mvr", "Maldivian Rufiyaa", "Rf", 15.4),
    ("mnt", "Mongolian Tugrik", "₮", 3500.0),
    ("uzs", "Uzbekistani Som", "so'm", 12000.0),
    ("kzt", "Kazakhstani Tenge", "₸", 520.0),
    ("kgs", "Kyrgyzstani Som", "сом", 87.0),
    ("tjs", "Tajikistani Somoni", "SM", 10.0),
    ("tmt", "Turkmenistani Manat", "m", 3.5),
    # Oceania
    ("nzd", "New Zealand Dollar", "NZ$", 1.75),
    ("fjd", "Fijian Dollar", "FJ$", 2.25),
    ("pgk", "Papua New Guinean Kina", "K", 4.25),
    ("wst", "Samoan Tala", "WS$", 2.70),
    ("top", "Tongan Paʻanga", "T$", 2.40),
    ("vuv", "Vanuatu Vatu", "VT", 120.0),
    ("sbd", "Solomon Islands Dollar", "SI$", 8.5),
    ("xpf", "CFP Franc", "₣", 109.0),
    # Additional currencies
    ("bmd", "Bermudian Dollar", "BD$", 1.0),
    ("kyd", "Cayman Islands Dollar", "CI$", 1.20),
    ("gip", "Gibraltar Pound", "£", 0.758255),
    ("fkp", "Falkland Islands Pound", "£", 0.758255),
    ("shp", "Saint Helena Pound", "£", 0.758255),
    ("jep", "Jersey Pound", "£", 0.758255),
    ("ggp", "Guernsey Pound", "£", 0.758255),
    ("imp", "Manx Pound", "£", 0.758255),
]


def main() -> None:
    tables = get_tables_db()
    created = updated = 0
    for code, name, symbol, rate in ROWS:
        data = {"code": code, "name": name, "symbol": symbol, "rateFromUsd": rate}
        try:
            tables.create_row(
                database_id=settings.appwrite_database_id,
                table_id=settings.appwrite_currencies_table_id,
                row_id=code,
                data=data,
            )
            created += 1
        except AppwriteException as exc:
            if exc.code != 409:
                raise
            tables.update_row(
                database_id=settings.appwrite_database_id,
                table_id=settings.appwrite_currencies_table_id,
                row_id=code,
                data=data,
            )
            updated += 1
    print(f"Done: {created} created, {updated} updated.")


if __name__ == "__main__":
    main()
