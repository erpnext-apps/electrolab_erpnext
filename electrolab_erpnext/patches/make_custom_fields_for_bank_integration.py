from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	frappe.reload_doc("accounts", "doctype", "tax_category")
	frappe.reload_doc("stock", "doctype", "item_manufacturer")
	company = frappe.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	bank_remittance_fields = {
		'Bank Account': [
			{
				'fieldname': 'bank_remittance_section',
				'label': 'Bank Remittance Settings',
				'fieldtype': 'Section Break',
				'collapsible': 1,
				'insert_after': 'mask'
			},
			{
				'fieldname': 'client_code',
				'label': 'Client Code',
				'fieldtype': 'Data',
				'insert_after': 'bank_remittance_section'
			},
			{
				'fieldname': 'remittance_column_break',
				'fieldtype': 'Column Break',
				'insert_after': 'client_code'
			},
			{
				'fieldname': 'product_code',
				'label': 'Product Code',
				'fieldtype': 'Data',
				'insert_after': 'remittance_column_break'
			}
		]
	}

	create_custom_fields(bank_remittance_fields, update=True)
