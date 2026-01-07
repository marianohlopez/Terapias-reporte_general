from db import connect_db
from extract import extract_docs_2026, extract_prest
from transform import export_excel, enviar_correo

def main():

  conn = connect_db()
  cursor = conn.cursor()
  data_docs_2026 = extract_docs_2026(cursor)
  data_prest = extract_prest(cursor)
  archivo = export_excel(data_docs_2026, data_prest)
  enviar_correo(archivo)

if __name__ == "__main__":
  main()