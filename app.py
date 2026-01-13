import streamlit as st
import database as db

db.create_tables()

st.title("📦 Zarządzanie Produktami i Kategoriami")

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
        liczba = st.number_input("Liczba", min_value=0, step=1)
        cena = st.number_input("Cena", min_value=0.0, format="%.2f")
        kategoria = st.selectbox("Kategoria", category_dict.keys())
        submitted = st.form_submit_button("Dodaj")

        if submitted:
            db.add_product(nazwa, liczba, cena, category_dict[kategoria])
            st.success("Produkt dodany")

    st.header("📋 Lista produktów")
    products = db.get_products()

    for prod in products:
        col1, col2 = st.columns([4, 1])
        col1.write(
            f"**{prod[1]}** | Ilość: {prod[2]} | Cena: {prod[3]} zł | Kategoria: {prod[4]}"
        )
        if col2.button("Usuń", key=f"prod_{prod[0]}"):
            db.delete_product(prod[0])
            st.experimental_rerun()
