"""Taller evaluable presencial"""

import pandas as pd


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""
    df = pd.read_csv(input_file,sep="\t")
    return df


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la columna 'text'"""

    df = df.copy()

    # Copie la columna 'text' a la columna 'key'

    # 1. Copie la columna 'text' a la columna 'key'
    df["key"] = df["text"]

    # 2. Remueva los espacios en blanco al principio y al final de la cadena
    df["key"] = df["key"].str.strip()

    # 3. Convierta el texto a minúsculas
    #podría usar df["key"] = df["key"].str.strap().str.lower()
    df["key"] = df["key"].str.lower()

    # 4. Transforme palabras que pueden (o no) contener guiones por su version sin guion.
    #df["key"] = df["key"].str.strap().str.lower().str.replace("-","")
    df["key"] = df["key"].str.replace("-","")

    # 5. Remueva puntuación y caracteres de control
    #df["key"] = df["key"].str.strap().str.lower().str.replace("-","").str.replace(".","")
    df["key"] = df["key"].str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))

    # 6. Convierta el texto a una lista de tokens
    #df["key"] = df["key"].str.strap().str.lower().str.replace("-","").str.replace(".","").str.split()
    df["key"] = df["key"].str.split()

    df["key"] = df["key"].str.join("")

     # Convierta el texto a una lista de n-gramas
    df["key"] = df["key"].map(lambda x: [x[t:t+n-1] for t in range(len(x))])

    #ordena la lista de n-gramas y remueve duplicados
    df["key"] = df["key"].apply(lambda x: sorted(set(x))) 

    # 9. Convierta la lista de tokens a una cadena de texto separada por espacios
    df["key"] = df["key"].str.join("")

    # Remueva los espacios en blanco al principio y al final de la cadena
    # Convierta el texto a minúsculas
    # Transforme palabras que pueden (o no) contener guiones por su version sin guion.
    # Remueva puntuación y caracteres de control
    # Convierta el texto a una lista de tokens
    # Una el texto sin espacios en blanco


    # Convierta el texto a una lista de n-gramas
    # Ordene la lista de n-gramas y remueve duplicados
    # Convierta la lista de ngramas a una cadena
    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()

    # Ordene el dataframe por 'key' y 'text'
    df = df.sort_values(by=["key", "text"], ascending=[True, True])

    # Seleccione la primera fila de cada grupo de 'key'
    keys = df.drop_duplicates(subset="key", keep="first")

    # Cree un diccionario con 'key' como clave y 'text' como valor
    key_dict = dict(zip(keys["key"], keys["text"]))

    # Cree la columna 'cleaned' usando el diccionario
    df["cleaned"] = df["key"].map(key_dict)

    return df



def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""

    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, index=False)


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
