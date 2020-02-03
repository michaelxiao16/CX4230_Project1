import csv


def get_salary_prob():
    with open("salary_prob.csv", 'r') as csv_file:
        rows = []
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            val = row[0]
            try:
                val1 = float(val)
                val2 = float(row[1])
                row = [val1, val2]
            except ValueError as e:
                continue
            rows.append(row)
    return rows


def get_move_out_prob():
    with open("move_out_prob.csv", 'r') as csv_file:
        rows = []
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            val = row[0]
            try:
                val = float(val)
            except ValueError as e:
                continue
            rows.append(val)
    return rows


def get_monthly_total_costs_prob():
    with open("monthly_total_costs.csv", 'r') as csv_file:
        rows = []
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            val = row[0]
            try:
                val1 = float(val)
                val2 = float(row[1])
                row = [val1, val2]
            except ValueError as e:
                continue
            rows.append(row)
    return rows


def get_percent_monthly_income():
    with open("percent_monthly_income.csv", 'r') as csv_file:
        rows = []
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            val = row[0]
            try:
                val1 = float(val)
                val2 = float(row[1])
                row = [val1, val2]
            except ValueError as e:
                continue
            rows.append(row)
    return rows
