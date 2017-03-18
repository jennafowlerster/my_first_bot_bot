import xlrd
from sys import argv
YEARS = [2014, 2016]
MONEY_KEY = 'Tran_Amt1'
ZIP_CODE_NUM = 22

def get_year_records(year):

    datafilename = 'data/efile_CPA_{}.xlsx'.format(year)
    book = xlrd.open_workbook(datafilename)
    sheet = book.sheets()[0]

    data = []
    for n in range(sheet.nrows):
        data.append(sheet.row_values(n))

    return data

def get_year_zipcode_records(year, zipcode):
    zipcodestr = str(zipcode)
    data = get_year_records(year)
    headers = data[0]

    newdata = []
    for row in data:
        if row[ZIP_CODE_NUM] == zipcodestr:
            d = dict(zip(headers, row))
            newdata.append(d)

    return newdata

def get_zipcode_records(zipcode):
    records = {}
    for year in YEARS:
        records[year] = get_year_zipcode_records(year, zipcode)
    return records

def make_story(zipcode, year_records):
    thestory = "The zip code of: " + str(zipcode) + "\n"
    for year, rows in year_records.items():
        year_total = 0
        for row in rows:
            year_total += row[MONEY_KEY]

        thestory += "In {year}, {amount} was raised.\n".format(year=year, amount=year_total)

    return thestory

def bot(zipcode):
    records = get_zipcode_records(zipcode)
    story = make_story(zipcode, records)
    return story


if __name__ == '__main__':

    if len(argv) < 2:
        print("You must enter a zip code as an argument!")
    else:
        zipcode = argv[1]
        txt = bot(zipcode)
        print(txt)
