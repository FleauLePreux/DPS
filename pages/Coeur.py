from dash import register_page, callback, Input, Output, State, html, ALL
import generique_page_maladie
import pandas as pd

# Enregistrement de la page
register_page(__name__)

df_relative_path = r"\dataframes\chd_clean.csv"

page_name = "Maladies Cardiaques"

image_page =  r"\assets\images\maladies-cardiovasculaires.png"

col_name = {"Maladies Cardiaques": {"age": "Age",
                                    "sex": "Genre",
                                    "cp": "Type de douleur thoracique",
                                    "trestbps": "Pression artérielle au repos",
                                    "chol": "Cholestérol sérique",
                                    "restecg": "Résultats électrocardiographiques au repos",
                                    "thalach": "Fréquence cardiaque maximale atteinte",
                                    "exang": "Angine induite par l'exercice",
                                    "oldpeak": "Dépression du segment ST induite par l'exercice",
                                    "slope": "Pente du segment ST à l'effort maximal",
                                    "ca": "Nombre de vaisseaux majeurs colorés par fluoroscopie",
                                    "thal": "Thalassémie",
                                    "target": {0: "Sain", 1: "Maladie Chronique du coeur"}}
    }
    
# Créez la mise en page
df, model, score, precision, falseNeg, layout= generique_page_maladie.create_layout(df_relative_path, page_name, col_name,image_page)

@callback(
    Output(page_name+'_resultat','children'),
    Input(page_name+'_submit_button','n_clicks'),
    State({"type": page_name+"_form_input", "index": ALL}, "value"),
    prevent_initial_call = True
)
def get_results(input,states):
    df_test = pd.DataFrame([states], columns=df.iloc[:,:-1].columns)
        
    result = col_name[page_name]["target"][model.predict(df_test)[0]]
    
    return html.H2(f'{result} (probabilité de {model.predict_proba(df_test)[0][0 if result == "Sain" else 1] * 100 :.2f}%)', className='text-white card-title text-center p-4')