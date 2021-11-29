from simple_term_menu import TerminalMenu
from lib import db
import rich
from rich.console import Console
from rich.table import Table
import csv
from fpdf import FPDF

class Menu():
    def __init__(self):
        self.db = db.dbClass()
        self.lang_menu()
    
    def lang_menu(self):
        options = ["English", "فارسی"]
        terminal_menu = TerminalMenu(options, title='Select your language')
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == 0:
            self.lang = 'en'
        if menu_entry_index == 1:
            self.lang = 'fa'
        self.home()
    
    def home(self):
        lang_dict = {
            'en': {
                'title': 'Welcome',
                'status': 'Please choose your project here',
                'op1': 'Choose exiting project',
                'op2': 'Create new project',
                'op3': 'Back',
                'op4': 'Exit'
            },
            'fa': {
                'title': 'خوش آمدید',
                'status': 'لطفا پروژه خود را مشخص کنید',
                'op1': 'انتخاب پروژه موجود',
                'op2': 'ایجاد پروژه جدید',
                'op3': 'برگشت',
                'op4': 'خروج'
            }
        }
        options = [lang_dict['en']['op1'], lang_dict['en']['op2'], lang_dict['en']['op3'], lang_dict['en']['op4']] if self.lang == 'en' else [lang_dict['fa']['op1'], lang_dict['fa']['op2'], lang_dict['fa']['op3'], lang_dict['fa']['op4']]
        terminal_menu = TerminalMenu(options, title=lang_dict['en']['title'], status_bar=lang_dict['en']['status']) if self.lang == 'en' else TerminalMenu(options, title=lang_dict['fa']['title'], status_bar=lang_dict['fa']['status'])
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == 0:
            self.select_project()
        if menu_entry_index == 1:
            self.create_project()
        if menu_entry_index == 2:
            self.lang_menu()
            
    def project_home(self):
        lang_dict = {
            'en': {
                'status': 'You are in {pro}'.format(pro=self.project_name),
                'op1': 'Edit Project',
                'op2': 'Add Product',
                'op3': 'Edit Product',
                'op4': 'Delete Product',
                'op5': 'Show Table',
                'op6': 'Print',
                'op7': 'Back'
            },
            'fa': {
                'status': 'شما در پروژه {pro} هستید'.format(pro=self.project_name),
                'op1': 'ویرایش پروژه',
                'op2': 'اضافه کردن',
                'op3': 'ویرایش کردن',
                'op4': 'حذف کردن',
                'op5': 'نمایش خروجی',
                'op6': 'پرینت',
                'op7': 'برگشت'
            }
        }
        options = [lang_dict['en']['op1'], lang_dict['en']['op2'], lang_dict['en']['op3'], lang_dict['en']['op4'], lang_dict['en']['op5'], lang_dict['en']['op6'], lang_dict['en']['op7']] if self.lang == 'en' else [lang_dict['fa']['op1'], lang_dict['fa']['op2'], lang_dict['fa']['op3'], lang_dict['fa']['op4'], lang_dict['fa']['op5'], lang_dict['fa']['op6'], lang_dict['fa']['op7']]
        terminal_menu = TerminalMenu(options, status_bar=lang_dict['en']['status']) if self.lang == 'en' else TerminalMenu(options, status_bar=lang_dict['fa']['status'])
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == 0:
            self.edit_project()
        if menu_entry_index == 1:
            self.add_product()
        if menu_entry_index == 2:
            self.edit_product()
        if menu_entry_index == 3:
            self.delete_product()
        if menu_entry_index == 4:
            self.show()
        if menu_entry_index == 5:
            self.print()
        if menu_entry_index == 6:
            self.home()
    
    def select_project(self):
        lang_dict = {
            'en': {
                'title': 'Exiting project',
            },
            'fa': {
                'title': 'پروژه های موجود',
            }
        }
        products = self.db.select_pro()
        lenght = products[0]
        pro = products[1]
        if lenght != 0:
            options = []
            for project in pro:
                options.append(project[1])
            terminal_menu = TerminalMenu(options, title=lang_dict['en']['title']) if self.lang == 'en' else TerminalMenu(options, title=lang_dict['fa']['title'])
            menu_entry_index = terminal_menu.show()
            selected = options[menu_entry_index]
            for project in pro:
                if project[1] == selected:
                    self.project_id = project[0]
                    self.project_name = project[1]
        self.project_home()
    
    def create_project(self):
        lang_dict = {
            'en': {
                'title': 'Please enter new project name : ',
                'budge': 'Please enter project budge : '
            },
            'fa': {
                'title': 'لطفا نام پروژه جدید را وارد کنید : ',
                'budge': 'لطفا بودجه پروژه را وارد کنید : '
            }
        }
        name = ''
        while name == '':
            name = input(lang_dict['en']['title']) if self.lang == 'en' else input(lang_dict['fa']['title'])
        budge = 0
        while budge == 0:
            budge = input(lang_dict['en']['budge']) if self.lang == 'en' else input(lang_dict['fa']['budge'])
        self.db.create_project(name, budge)
        self.home()
        
    def add_product(self):
        lang_dict = {
            'en': {
                'name': 'Please enter new product name : ',
                'unit': 'Please enter unit : ',
                'price': 'Please enter price per unit : ',
                'value': 'Please enter value : '
            },
            'fa': {
                'name': 'لطفا نام کالای جدید را وارد کنید : ',
                'unit': 'لطفا واحد کالا را وار کنید : ',
                'price': 'لطفا بهای کالا را وارد کنید : ',
                'value': 'لطفا مقدار را وارد کنید : '
            }
        }
        name = ''
        while name == '':
            name = input(lang_dict['en']['name']) if self.lang == 'en' else input(lang_dict['fa']['name'])
        unit = ''
        while unit == '':
            unit = input(lang_dict['en']['unit']) if self.lang == 'en' else input(lang_dict['fa']['unit'])
        price = ''
        while price == '':
            price = input(lang_dict['en']['price']) if self.lang == 'en' else input(lang_dict['fa']['price'])
        value = ''
        while value == '':
            value = input(lang_dict['en']['value']) if self.lang == 'en' else input(lang_dict['fa']['value'])
        self.db.add_product(self.project_id, name, unit, price, value)
        self.project_home()
    
    def edit_product(self):
        lang_dict = {
            'en': {
                'title': 'Please enter for edit',
                'name': 'Please enter new product name : ',
                'unit': 'Please enter unit : ',
                'price': 'Please enter price per unit : ',
                'value': 'Please enter value : '
            },
            'fa': {
                'title': 'برای ویرایش انتخاب کنید',
                'name': 'لطفا نام کالای جدید را وارد کنید : ',
                'unit': 'لطفا واحد کالا را وار کنید : ',
                'price': 'لطفا بهای کالا را وارد کنید : ',
                'value': 'لطفا مقدار را وارد کنید : '
            }
        }
        products = self.db.get_product(self.project_id)
        lenght = products[0]
        products = products[1]
        if lenght != 0:
            options = []
            for pro in products:
                options.append(pro[1])
            terminal_menu = TerminalMenu(options, status_bar=lang_dict['en']['title'] if self.lang == 'en' else lang_dict['fa']['title'])
            menu_entry_index = terminal_menu.show()
            for pro in products:
                if options[menu_entry_index] == pro[1]:
                    pro_id_edit = pro[0]
                    pro_name = pro[1]
                    pro_unit = pro[2]
                    pro_price = pro[3]
                    pro_value = pro[4]
            rich.print('[bold red]Leave Empty if you do not wnat to change.')
            print('Name is : {text}'.format(text=pro_name))
            name = input(lang_dict['en']['name']) if self.lang == 'en' else input(lang_dict['fa']['name'])
            if name == '':
                name = pro_name
            print('Unit is : {text}'.format(text=pro_unit))
            unit = input(lang_dict['en']['unit']) if self.lang == 'en' else input(lang_dict['fa']['unit'])
            if unit == '':
                unit = pro_unit
            print('Price is : {text}'.format(text=pro_price))
            price = input(lang_dict['en']['price']) if self.lang == 'en' else input(lang_dict['fa']['price'])
            if price == '':
                price = pro_price
            print('Value is : {text}'.format(text=pro_value))
            value = input(lang_dict['en']['value']) if self.lang == 'en' else input(lang_dict['fa']['value'])
            if value == '':
                value = pro_value
            self.db.edit_product(pro_id_edit, self.project_id, name, unit, price, value)
        self.project_home()
    
    def delete_product(self):
        lang_dict = {
            'en': {
                'title': 'Please enter for delete',
            },
            'fa': {
                'title': 'برای حذف انتخاب کنید',
            }
        }
        products = self.db.get_product(self.project_id)
        lenght = products[0]
        products = products[1]
        if lenght != 0:
            options = []
            for pro in products:
                options.append(pro[1])
            terminal_menu = TerminalMenu(options, status_bar=lang_dict['en']['title'] if self.lang == 'en' else lang_dict['fa']['title'])
            menu_entry_index = terminal_menu.show()
            for pro in products:
                if options[menu_entry_index] == pro[1]:
                    pro_id_edit = pro[0]
            self.db.delete_product(pro_id_edit, self.project_id)
        self.project_home()
        
    def show(self):
        table = Table(title=self.project_name)
        if self.lang == 'en':
            table.add_column("Name", justify="right", style="cyan")
            table.add_column("Unit", style="magenta", justify="right")
            table.add_column("Price Per Unit", justify="right", style="green")
            table.add_column("Value", justify="right", style="green")
            table.add_column("Total Price", justify="right", style="green")
        if self.lang == 'fa':
            table.add_column("نام", justify="right", style="cyan")
            table.add_column("واحد", style="magenta", justify="right")
            table.add_column("قیمت بر هر واحد", justify="right", style="green")
            table.add_column("مقدار", justify="right", style="green")
            table.add_column("قیمت کل", justify="right", style="green")

        products = self.db.get_product(self.project_id)[1]
        sum = 0
        for pro in products:
            pro_name = pro[1]
            pro_unit = pro[2]
            pro_price = pro[3]
            pro_value = pro[4]
            sum += pro_price * pro_value
            table.add_row(pro_name, pro_unit, str(pro_price), str(pro_value), str(pro_price*pro_value))
        console = Console()
        console.print(table)
        budge = self.db.get_budge(self.project_id)
        if self.lang == 'en':
            rich.print('[bold red]Total budget : {sum}'.format(sum=str(budge)))
            rich.print('[bold red]Collect deductions : {sum}'.format(sum=str(sum)))
            rich.print('[bold red]Remaining budget : {i}'.format(i=str(budge - sum)))
        if self.lang == 'fa':
            rich.print('[bold red]کل بودجه : {sum}'.format(sum=str(budge)))
            rich.print('[bold red]جمع کسورات : {sum}'.format(sum=str(sum)))
            rich.print('[bold red]بودجه باقی مانده : {i}'.format(i=str(budge - sum)))
        self.project_home()
        
    def edit_project(self):
        lang_dict = {
            'en': {
                'name': 'Please enter new product name : ',
                'budge': 'Please enter budget : ',
            },
            'fa': {
                'name': 'لطفا نام کالای جدید را وارد کنید : ',
                'budge': 'لطفا بودجه را وارد کنید : ',
            }
        }
        project = self.db.get_edit_project(self.project_id)
        rich.print('[bold red]Leave Empty if you do not wnat to change.')
        print('Name is : {text}'.format(text=project[0]))
        name = input(lang_dict['en']['name']) if self.lang == 'en' else input(lang_dict['fa']['name'])
        if name == '':
            name = project[0]
        print('Unit is : {text}'.format(text=project[1]))
        budge = input(lang_dict['en']['budge']) if self.lang == 'en' else input(lang_dict['fa']['budge'])
        if budge == '':
            budge = project[1]
        self.db.edit_project(self.project_id, name, budge)
        self.project_home()
    
    def print(self):
        open('log.csv', 'w').close()
        def save_csv(row):
            with open('log.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
        products = self.db.get_product(self.project_id)[1]
        if self.lang == 'en':
            save_csv(['Name', 'Unit', 'Price Per Unit', 'Value', 'Total Price'])
        if self.lang == 'fa':
            save_csv(['نام', 'واحد', 'قیمت هر واحد', 'مقدار', 'قیمت کل'])
        sum = 0
        for product in products:
            row = []
            row.append(product[1])
            row.append(product[2])
            row.append(str(product[3]))
            row.append(str(product[4]))
            row.append(str(product[3]*product[4]))
            sum += product[3]*product[4]
            save_csv(row)
        budge = self.db.get_budge(self.project_id)
        total = budge - sum
        with open('log.csv', newline='') as f:
            reader = csv.reader(f)
            
            pdf = FPDF()
            #pdf.add_font('B Nazanin', '', 'B-NAZANIN.TTF', uni=True)
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
                
            pdf.set_font('Times','',14.0) 
            pdf.cell(page_width, 0.0, self.project_name, align='C')
            pdf.ln(10)

            pdf.set_font('Times', '', 10)
            
            col_width = page_width/5
            
            pdf.ln(1)
            
            th = pdf.font_size
            i = 0
            for row in reader:
                pdf.cell(col_width, th, row[0], border=1, align='C')
                pdf.cell(col_width, th, row[1], border=1, align='C')
                pdf.cell(col_width, th, row[2], border=1, align='C')
                pdf.cell(col_width, th, row[3], border=1, align='C')
                pdf.cell(col_width, th, row[4], border=1, align='C')
                pdf.ln(th)
                i += 1
                if i > 10:
                    pdf.add_page()
                    i = 0
                
            pdf.add_page()
            pdf.set_font('Times','',14.0) 
            pdf.cell(page_width, 0.0, 'Results', align='C')
            pdf.ln(20)
            pdf.set_font('Times','',10)
            pdf.cell(page_width, 0.0, 'Total budget : {sum}'.format(sum=str(budge)), align='L')
            pdf.ln(10)
            pdf.cell(page_width, 0.0, 'Collect deductions : {sum}'.format(sum=str(sum)), align='L')
            pdf.ln(10)
            pdf.cell(page_width, 0.0, 'Remaining budget : {i}'.format(i=str(total)), align='L')
            
            pdf.ln(10)
            pdf.set_font('Times','',7.0)
            pdf.cell(page_width, 0.0, '<<< Developed by http://qtle.ir >>>', align='C')
            
            pdf.output('result.pdf', 'F')
        self.project_home()