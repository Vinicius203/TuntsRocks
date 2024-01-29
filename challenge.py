import pandas as pd
import math
from googleapiclient.discovery import build
from google.oauth2 import service_account


def authenticate_spreadsheet():
    SERVICE_ACCOUNT_FILE = "keys.json"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    return creds


def get_spreadsheet_data(creds, spreadsheet_id, spreadsheet_range):
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=spreadsheet_range)
        .execute()
    )

    values = result.get("values", [])
    return values


def calculate_situation_and_update_sheet(df):
    for index, row in df.iterrows():
        # Average of P1, P2 and P3
        average = (float(row["P1"]) + float(row["P2"]) + float(row["P3"])) / 3

        situation = ""
        # Naf stands for "Nota para Aprovação Final = Grade to Final Approval"
        naf = 0

        # Check absences percentage (> 25% = Reproved)
        if (
            int(row["Faltas"]) > 0.25 * 60
        ):  # The number of total classes is assumed as 60 (value in the sheet)
            situation = "Reprovado por Falta"
        elif average < 50:
            situation = "Reprovado por Nota"
        elif 50 <= average < 70:
            situation = "Exame Final"
            naf = max(0, 100 - average)
            naf = math.ceil(naf)
        else:
            situation = "Aprovado"

        df.at[index, "Situação"] = situation
        df.at[index, "Nota para Aprovação Final"] = naf

        print(
            f"Student {row['Aluno']}: Situation - {situation}, Nota para Aprovação Final - {naf}"
        )

    return df


def update_spreadsheet(creds, spreadsheet_id, spreadsheet_range, updated_values):
    service = build("sheets", "v4", credentials=creds)

    updated_body = {"values": updated_values}
    update_result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=spreadsheet_range,
            body=updated_body,
            valueInputOption="RAW",
        )
        .execute()
    )

    print("Data has beed updated in Google Spreadsheets.")


def main():
    creds = authenticate_spreadsheet()

    if creds:
        # Spreadsheet ID
        SAMPLE_SPREADSHEET_ID = "1tSh199BesukXZ8cbrwsFFsRCiAX77g8RGTtUqd-wcJE"
        SPREADSHEET_RANGE = "engenharia_de_software!A4:H27"

        values = get_spreadsheet_data(creds, SAMPLE_SPREADSHEET_ID, SPREADSHEET_RANGE)

        if values:
            df = pd.DataFrame(
                values,
                columns=[
                    "Matricula",
                    "Aluno",
                    "Faltas",
                    "P1",
                    "P2",
                    "P3",
                    "Situação",
                    "Nota para Aprovação Final",
                ],
            )

            df = calculate_situation_and_update_sheet(df)

            # Include the header when creating the updated_values list
            updated_values = [df.columns.tolist()] + df.values.tolist()

            # Adjust the SPREADSHEET_RANGE to include the header
            SPREADSHEET_RANGE = f"engenharia_de_software!A3:H27"

            update_spreadsheet(
                creds, SAMPLE_SPREADSHEET_ID, SPREADSHEET_RANGE, updated_values
            )


if __name__ == "__main__":
    main()
