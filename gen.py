from jinja2 import Template
import yaml
import datetime
from dateutil.relativedelta import relativedelta
from weasyprint import HTML
import os

TEMPLATE = 'template.html'
LOGO = 'logo.png'
DATA = 'data.yml'

DATE_FORMAT = "%B %d, %Y"

def calc_totals(data):
    total = 0
    for item in data['items']:
        if 'hours' not in item:
            item['hours'] = 0
        if 'rate' not in item:
            item['rate'] = 0
        if item['hours'] != 0:
            item['total'] = item['rate'] * item['hours']
        else:
            item['total'] =  item['rate']
            item['hours'] = ""            
        total = total + item['total']
    data['total'] = total
    return data

def load_data(data_file):
    with open(data_file, 'r') as infile:
        data = yaml.safe_load(infile)
    data = calc_totals(data)
    data['logo'] = f'file://{os.path.abspath(data["logo"])}'
    return data

def load_template(template_file):
    with open(template_file, 'r') as infile:
        template = Template(infile.read())
    return template

def generate_invoice(template, data, due_months=None):
    generatedDate = datetime.datetime.now()
    data['createdDate'] = generatedDate.strftime(DATE_FORMAT)
    if due_months: 
        dueDate = generatedDate + relativedelta(months=+due_months)
        data['dueDate'] = dueDate.strftime(DATE_FORMAT)
    else:
        data['dueDate'] = ""
    invoice = template.render(data)
    return invoice

def generate_pdf(invoice):
    html = HTML(string=invoice)
    return html.write_pdf()

def main():
    data = load_data(DATA)
    template = load_template(TEMPLATE)
    invoice = generate_invoice(template, data)
    with open('out.html', 'w') as outfile:
        outfile.write(invoice)
    pdf = generate_pdf(invoice)
    with open('out.pdf', 'wb') as outfile:
        outfile.write(pdf)
        
if __name__ == "__main__":
    main()