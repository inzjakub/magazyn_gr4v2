import streamlit as st
import database as db

db.create_tables()

st.title("📦 Magazyn budowlany – produkty i kategorie")

menu = st.sidebar.selectbox(
    "Menu",
    ["Kategorie", "Produkty"]
)

# ---------------- KATEGORIE ----------------
if menu == "Kategorie":
    st.header("➕ Dodaj kategorię")

    with st.form("add_category"):
        nazwa = st.text_input("Nazwa kategorii")
        opis = st.text_area("Opis")
        submitted = st.form_submit_button("Dodaj")

        if submitted:
            db.add_category(nazwa, opis)
            st.success("Kategoria dodana")

    st.header("📋 Lista kategorii")
    categories = db.get_categories()

    for cat in categories:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{cat[1]}** – {cat[2]}")
        if col2.button("Usuń", key=f"cat_{cat[0]}"):
            db.delete_category(cat[0])
            st.experimental_rerun()


# ---------------- PRODUKTY ----------------
if menu == "Produkty":
    st.header("➕ Dodaj produkt")

    categories = db.get_categories()
    category_dict = {cat[1]: cat[0] for cat in categories}

    with st.form("add_product"):
        nazwa = st.text_input("Nazwa produktu")
        liczba = st.number_input("Ilość", min_value=0, step=1)
        cena = st.number_input("Cena", min_value=0.0, format="%.2f")
        stan_min = st.number_input(
            "Minimalny stan magazynowy",
            min_value=0,
            step=1
        )
        kategoria = st.selectbox("Kategoria", category_dict.keys())
        submitted = st.form_submit_button("Dodaj")

        if submitted:
            db.add_product(
                nazwa,
                liczba,
                cena,
                category_dict[kategoria],
                stan_min
            )
            st.success("Produkt dodany")

    st.header("📋 Lista produktów")

    products = db.get_products()

    for prod in products:
        id_, nazwa, ilosc, cena, kategoria, stan_min = prod

        col1, col2 = st.columns([4, 1])

        # 🚨 ALERT NISKIEGO STANU
        if ilosc <= stan_min:
            col1.error(
                f"⚠️ NISKI STAN | {nazwa} ({kategoria}) "
                f"– {ilosc} szt. | min: {stan_min}"
            )
        else:
            col1.write(
                f"**{nazwa}** | Ilość: {ilosc} | Cena: {cena} zł | Kategoria: {kategoria}"
            )

        if col2.button("Usuń", key=f"prod_{id_}"):
            db.delete_product(id_)
            st.experimental_rerun()
