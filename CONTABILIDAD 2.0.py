import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO, StringIO
import OTMrunReport as rr
import requests
st.set_page_config(layout="wide")
logo_base64 = """
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
"""
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo de la Empresa" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)
# Acceder a las credenciales desde los secretos
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]

# Función para verificar las credenciales
def authenticate(username, password):
    if username in usernames:
        index = usernames.index(username)
        if passwords[index] == password:
            return True
    return False

# Inicializar el estado de sesión si no existe
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Si el usuario no está autenticado, mostrar el formulario de inicio de sesión
if not st.session_state.authenticated:
    st.title("Iniciar sesión")
    username_input = st.text_input("Usuario")
    password_input = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if authenticate(username_input, password_input):
            st.session_state.authenticated = True
            st.success(f"Bienvenid@, {username_input}!")
            st.rerun()  # Recarga la página para reflejar el cambio
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # Contenido de la aplicación para usuarios autenticados
    provisiones = st.secrets["google_drive"]["provisiones"]
    mapeo = st.secrets["google_drive"]["mapeo"]
    base = st.secrets["google_drive"]["base"]

    @st.cache_data
    def cargar_datos_pro(url, sheet_name=None):
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la descarga
        archivo_excel = BytesIO(response.content)
        return pd.read_excel(archivo_excel, sheet_name=sheet_name, engine="openpyxl")

    @st.cache_data
    def cargar_datos(url):
            response = requests.get(url)
            response.raise_for_status()  # Verifica si hubo algún error en la descarga
            archivo_excel = BytesIO(response.content)
            return pd.read_excel(archivo_excel, engine="openpyxl")

    # Especifica la hoja que deseas cargar
    hoja_deseada = "Base provisiones"

    df_provisiones = cargar_datos_pro(provisiones, sheet_name=hoja_deseada)
    df_mapeo = cargar_datos(mapeo)
    df_base = cargar_datos(base)
    @st.cache_data
    def get_xtr_as_dataframe():
        # 1. Obtener el reporte (contenido del archivo XTR)
        headers = rr.headers(st.secrets["RR"]["usuario_otm"], st.secrets["RR"]["contrasena_otm"])
        algo = rr.runReport(st.secrets["RR"]["path"], 'ekck.fa.us6', headers)

        # 2. Verificar el tipo de "algo"
        if isinstance(algo, bytes):
            algo = algo.decode('utf-8')  # Convertir bytes a string

        # 3. Convertir el contenido XTR a DataFrame
        try:
            xtr_io = StringIO(algo)  # Crear un buffer en memoria
            df = pd.read_csv(xtr_io, sep=",", low_memory=False)  # Ajusta el delimitador aquí
        except Exception as e:
            st.error(f"Error al procesar el archivo XTR: {e}")
            return None

        return df, algo

    df, algo = get_xtr_as_dataframe()
    df_original = df.copy()

        # Selección y renombrado de columnas
    columnas_d = ['DEFAULT_EFFECTIVE_DATE', 'DEFAULT_EFFECTIVE_DATE', 'SEGMENT1', 'SEGMENT2', 'SEGMENT3', 'SEGMENT5', 'CREDIT', 'DEBIT']
    nuevo_nombre = ['Año_A','Mes_A', 'Empresa_A', 'CeCo_A', 'Proyecto_A', 'Cuenta_A', 'Credit_A', 'Debit_A']
        # Validar que las columnas existen en el DataFrame
    columnas_disponibles = [col for col in columnas_d if col in df.columns]
        # Seleccionar y renombrar las columnas
    df = df[columnas_disponibles]
    df.columns = nuevo_nombre[:len(columnas_disponibles)]
    df['Cuenta_A'] = pd.to_numeric(df['Cuenta_A'], errors='coerce')
    df['Debit_A'] = pd.to_numeric(df['Debit_A'], errors='coerce')
    df['Credit_A'] = pd.to_numeric(df['Credit_A'], errors='coerce')

        # Rellenar valores NaN con 0 (opcional, dependiendo de tus datos)
    df[['Debit_A', 'Credit_A']] = df[['Debit_A', 'Credit_A']].fillna(0)
        # Calcular la columna Neto_A
    df['Neto_A'] = df.apply(
            lambda row: row['Debit_A'] - row['Credit_A'] ,
            axis=1
        )
    df['Año_A'] = pd.to_datetime(df['Año_A'], errors='coerce')
    df['Año_A'] = df['Año_A'].dt.year

        # Convertir la columna 'Mes_A' al tipo datetime
    df['Mes_A'] = pd.to_datetime(df['Mes_A'], errors='coerce')
    df = df.merge(df_mapeo, on='Cuenta_A', how='left')
        # Crear una nueva columna con el mes (en formato numérico o nombre, según prefieras)
    df['Mes_A'] = df['Mes_A'].dt.month 
    df = df.groupby(['Año_A', 'Mes_A', 'Proyecto_A', 'CeCo_A', 'Empresa_A', 'Cuenta_A'])['Debit_A','Credit_A','Neto_A'].sum().reset_index()
    df = df.merge(df_mapeo, on='Cuenta_A', how='left')

    meses = df['Mes_A'].unique().tolist()
    años = df['Año_A'].unique().tolist()
    empresas = df['Empresa_A'].unique().tolist()
    st.write('')
    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        return output.getvalue()

    # Botón de descarga
    excel_data = to_excel(df)
    col1, col2 = st.columns(2)
    col1.download_button(
        label="Descargar Movimientos de sistema",
        data=excel_data,
        file_name="datos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    def limpiar_cache():
        st.cache_data.clear()  # Limpia el caché de los datos
        
    if col2.button("Volver a recargar datos del sistema"):
        limpiar_cache()
        st.warning("recargar la pagina")
    col1, col2 = st.columns(2)
    año = col1.selectbox('SELECCIONAR AÑO', años)
    mes = col2.selectbox('SELECCIONAR MES', meses)

    df = df[(df['Año_A'] == año) & (df['Mes_A'] == mes)]
    col1, col2 = st.columns(2)
    ingreso_50 = df[(df['CeCo_A'] == 50) & (df['Cuenta_A'] >399999999) & (df['Cuenta_A'] <500000000)]['Neto_A'].sum()
    egreso_50 = df[(df['CeCo_A'] == 50) & (df['Cuenta_A'] >500000000)]['Neto_A'].sum()
    col1.write(f'INGRESO INTEREMPRESAS: {ingreso_50:,.2f}')
    col2.write(f'EGRESO INTEREMPRESAS: {egreso_50:,.2f}')
    dfsb = df[~(df['CeCo_A'] == 50) & (df['Cuenta_A']>399999999)]
    orden_meses = {
        1: 'ene.', 2: 'feb.', 3: 'mar.', 4: 'abr.',
        5: 'may.', 6: 'jun.', 7: 'jul.', 8: 'ago.',
        9: 'sep.', 10: 'oct.', 11: 'nov.', 12: 'dic.'
    }
    mes_a_numero = {v: k for k, v in orden_meses.items()}

    # Cambiar la columna 'mes' de abreviaturas a números usando map
    df_base['Mes_A'] = df_base['Mes_A'].map(mes_a_numero)

    proyectos = dfsb['Proyecto_A'].unique().tolist()
    historicos = ['CASETAS', 'RENTA', 'SOFTWARE', 'NOMINA ADMINISTRATIVOS','NOMINA OPERADORES']
    def df_cuentas (df, y, cat, col, mes, df_base):
        df_list = []
        for x in proyectos:
            df_pro = df[df['Proyecto_A'] == x]
            df_cat = df_pro[df_pro[y] == cat]['Neto_A'].sum(skipna=True)
            if cat in historicos:
                df_base = df_base[df_base['Mes_A'] == (mes -1)]
                df_pro_provisiones = df_base[df_base['Proyecto_A'] == x]
                df_cat_provisiones = df_pro_provisiones[df_pro_provisiones[y] == cat]['Neto_A'].sum(skipna=True)
            else:
                df_pro_provisiones = df_provisiones[df_provisiones['Proyecto_A'] == x]
                df_cat_provisiones = df_pro_provisiones[df_pro_provisiones[y] == cat]['Neto_A'].sum(skipna=True)
            data = {
                'PROYECTO' : [x],
                f'{cat} SISTEMA' : [df_cat],
                f'{cat} PROVISION' : [df_cat_provisiones] 
            }
            x = pd.DataFrame(data)
            df_list.append(x)

        df_final = pd.concat(df_list, ignore_index=True)
        nueva_fila = {
        df_final.columns[0] : 'ESGARI',
        df_final.columns[1] : df_final[df_final.columns[1]].sum(skipna=True),
        df_final.columns[2] : df_final[df_final.columns[2]].sum(skipna=True)
            }
        nueva_fila = pd.DataFrame([nueva_fila])
        df_final = pd.concat([df_final, nueva_fila], ignore_index=True)
        df_final = df_final.set_index('PROYECTO')
        col.subheader(f'COMPARACIÓN {cat}')
        col.write(df_final)

    categorias = ['INGRESO','NOMINA OPERADORES', 'NOMINA ADMINISTRATIVOS', 'FLETES', 'RENTA DE REMOLQUES', 'COMBUSTIBLE', 'CASETAS', 'RENTA', 'SOFTWARE']
    i = 0
    col1, col2, col3 = st.columns(3)

    # Alternar entre tres columnas
    i = 0
    for x in categorias:
        if i % 3 == 0:
            # Columna 1
            current_col = col1
        elif i % 3 == 1:
            # Columna 2
            current_col = col2
        else:
            # Columna 3
            current_col = col3
        df_cuentas(dfsb, 'Categoria_A', x, current_col, mes, df_base)
        i = i+1

    cuentas = ['DAÑOS', 'DIF DE KILOMETRAJE', 'MANTENIMIENTO EQ TRANSPORTE', 'SEGUROS Y FIANZAS']
    i = 0
    col1, col2, col3 = st.columns(3)

    # Alternar entre tres columnas
    i = 0
    for x in cuentas:
        if i % 3 == 0:
            # Columna 1
            current_col = col1
        elif i % 3 == 1:
            # Columna 2
            current_col = col2
        else:
            # Columna 3
            current_col = col3
        df_cuentas(dfsb, 'Cuenta_Nombre_A', x, current_col, mes, df_base)
        i = i+1
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.rerun()
