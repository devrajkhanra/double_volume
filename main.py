# main.py

import os
import pandas as pd


def homeEnv():

    # Get and print the home directory
    home_directory = f'{os.path.expanduser("~")}\Desktop'
    print("\nHome Directory:", home_directory)
    return home_directory


def userInput():

    # Take two user input
    print('')
    date1 = input("Enter today's date (ddmmyyyy): ")
    date2 = input("Enter yesterday's date (ddmmyyyy): ")
    print('Today', date1, ' | ', 'Yesterday', date2)
    return [date1, date2]

dates = userInput()


def fetchStockFile():

    homeDir = homeEnv()

    stockDir = f"{homeDir}/data/subfolders/stock"
    indiceDir = f"{homeDir}/data/subfolders/indice"
    niftyDir = f"{homeDir}/data/subfolders/nifty"

    # Check if both the csv files are present
    if (os.path.isfile(f"{stockDir}/sec_bhavdata_full_{dates[0]}.csv") and os.path.isfile(f"{stockDir}/sec_bhavdata_full_{dates[1]}.csv")):

        # Read csv files
        stockFile1 = pd.read_csv(
            f"{stockDir}/sec_bhavdata_full_{dates[0]}.csv")
        stockFile2 = pd.read_csv(
            f"{stockDir}/sec_bhavdata_full_{dates[1]}.csv")

        # Filter csv files according to SERIES column
        stockFile1 = stockFile1[stockFile1[' SERIES'] == ' EQ']
        stockFile2 = stockFile2[stockFile2[' SERIES'] == ' EQ']

        # Merge csv files according to their names
        stockFileMerged = pd.merge(stockFile1, stockFile2, on='SYMBOL')

        print(stockFileMerged.columns)
        # Delete unnecessary columns
        stockFileMerged = stockFileMerged.drop(columns=[' SERIES_x', ' PREV_CLOSE_x', ' OPEN_PRICE_x', ' LOW_PRICE_x', ' LAST_PRICE_x', ' AVG_PRICE_x', ' TURNOVER_LACS_x',
                                               ' NO_OF_TRADES_x', ' SERIES_y', ' PREV_CLOSE_y', ' OPEN_PRICE_y', ' LOW_PRICE_y', ' LAST_PRICE_y', ' AVG_PRICE_y', ' TURNOVER_LACS_y', ' NO_OF_TRADES_y'])

        # Convert columns to int
        stockFileMerged[' TTL_TRD_QNTY_x'] = stockFileMerged[' TTL_TRD_QNTY_x'].astype(
            int)
        stockFileMerged[' TTL_TRD_QNTY_y'] = stockFileMerged[' TTL_TRD_QNTY_y'].astype(
            int)
        stockFileMerged[' DELIV_QTY_x'] = stockFileMerged[' DELIV_QTY_x'].astype(
            int)
        stockFileMerged[' DELIV_QTY_y'] = stockFileMerged[' DELIV_QTY_y'].astype(
            int)
        stockFileMerged[' HIGH_PRICE_x'] = stockFileMerged[' HIGH_PRICE_x'].astype(
            float)
        stockFileMerged[' HIGH_PRICE_y'] = stockFileMerged[' HIGH_PRICE_y'].astype(
            float)

        # Calculate Volume break and Delivery volume break
        stockFileMerged['V Break Times'] = stockFileMerged[' TTL_TRD_QNTY_y'] > stockFileMerged[' TTL_TRD_QNTY_x']

        stockFileMerged['DV Break Times'] = stockFileMerged[' DELIV_QTY_y'] > stockFileMerged[' DELIV_QTY_x']

        # Calculate Higher High of price
        stockFileMerged['HH'] = stockFileMerged[' HIGH_PRICE_y'] < stockFileMerged[' HIGH_PRICE_x']
        stockFileMerged['HHCL'] = stockFileMerged[' CLOSE_PRICE_y'] < stockFileMerged[' HIGH_PRICE_x']
        # Return only the ones that broke atleast twice times
        # stockFileMerged = stockFileMerged[stockFileMerged['DV Break Times'] >= 2.0]

        return stockFileMerged


def fetchNiftyFiles(dataframe):
    homeDir = homeEnv()

    niftyDir = f"{homeDir}/data/subfolders/nifty"

    # Check if both the csv files are present
    if (os.path.isfile(f"{niftyDir}/ind_nifty50list.csv") and os.path.isfile(f"{niftyDir}/ind_niftynext50list.csv") and os.path.isfile(f"{niftyDir}/ind_niftymidcap50list.csv") and os.path.isfile(f"{niftyDir}/ind_niftysmallcap50list.csv")):

        # Read csv files
        niftyFile1 = pd.read_csv(
            f"{niftyDir}/ind_nifty50list.csv")
        niftyFile2 = pd.read_csv(
            f"{niftyDir}/ind_niftynext50list.csv")
        niftyFile3 = pd.read_csv(
            f"{niftyDir}/ind_niftymidcap50list.csv")
        niftyFile4 = pd.read_csv(
            f"{niftyDir}/ind_niftysmallcap50list.csv")

        # Filter stockFileMerged csv files according to SYMBOL column
        stockFile1filtered = dataframe[dataframe['SYMBOL'].isin(
            niftyFile1['Symbol'])]
        stockFile2filtered = dataframe[dataframe['SYMBOL'].isin(
            niftyFile2['Symbol'])]
        stockFile3filtered = dataframe[dataframe['SYMBOL'].isin(
            niftyFile3['Symbol'])]
        stockFile4filtered = dataframe[dataframe['SYMBOL'].isin(
            niftyFile4['Symbol'])]

        return stockFile1filtered, stockFile2filtered, stockFile3filtered, stockFile4filtered


if __name__ == "__main__":
    stockFiles = fetchStockFile()
    niftyFiles = fetchNiftyFiles(stockFiles)
    # print(niftyFiles)
    df1, df2, df3, df4 = niftyFiles

    # Specify the Excel file path
    excel_file_path = f'{homeEnv()}/data/output_file{dates[1]}.xlsx'

    # Create an ExcelWriter object
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        # Write each DataFrame to a different sheet
        df1.to_excel(writer, sheet_name='Nifty50', index=False)
        df2.to_excel(writer, sheet_name='Next50', index=False)
        df3.to_excel(writer, sheet_name='Midcap50', index=False)
        df4.to_excel(writer, sheet_name='Smallcap50', index=False)
