"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import pandas as pd
    from pathlib import Path
    import os

    # Ruta del directorio donde están los archivos ZIP
    input_dir = Path("files/input")
    output_dir =Path("files/output")

    # Definir las columnas correctamente
    columns = [ "client_id", "age", "job", "marital", "education", "credit_default", 
            "mortgage", "month", "day", "contact_duration", "number_contacts", 
            "previous_campaign_contacts", "previous_outcome", "cons_price_idx", 
            "euribor_three_months", "campaign_outcome"]

    # Crear un DataFrame vacío con las columnas correctas
    data = pd.DataFrame(columns=columns)

    # Leer y concatenar los archivos ZIP
    for archive in input_dir.iterdir():
        df = pd.read_csv(
            archive,
            index_col=False,
            compression="zip",
        )
        # Concatenar con el DataFrame principal
        data = pd.concat([data, df], ignore_index=True)

    # Mostrar las primeras filas del DataFrame final
   
    data["job"] = data["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    data["education"] = data["education"].str.replace(".","_", regex=False).replace("unknown",pd.NA)
    data["credit_default"] = data["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    data["mortgage"] = data["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    client_df = data[["client_id","age","job","marital","education","credit_default","mortgage"]]


    data["previous_outcome"] = data["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    data["campaign_outcome"] = data["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    data["last_contact_date"] = pd.to_datetime(data["day"].astype(str) + "-" + data["month"] + "-2022", format="%d-%b-%Y")

    campaing_df = data[["client_id","number_contacts","contact_duration","previous_campaign_contacts","previous_outcome","campaign_outcome","last_contact_date"]]


    economics_df =data[["client_id","cons_price_idx","euribor_three_months"]]


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    campaing_df.set_index("client_id", drop=True, inplace=True)
    economics_df.set_index("client_id", drop=True, inplace=True)
    client_df.set_index("client_id", drop=True, inplace=True)
  

    client_df.to_csv(os.path.join(output_dir, "client.csv",))
    campaing_df.to_csv(os.path.join(output_dir, "campaign.csv"))
    economics_df.to_csv(os.path.join(output_dir, "economics.csv"))


    return



if __name__ == "__main__":
    clean_campaign_data()
