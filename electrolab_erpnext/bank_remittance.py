# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint,cstr, today
from frappe import _
from frappe.utils import get_link_to_form
import re
import datetime
from collections import OrderedDict

def create_bank_remittance_txt(name):
	payment_order = frappe.get_cached_doc("Payment Order", name)

	no_of_records = len(payment_order.get("references"))
	total_amount = sum(entry.get("amount") for entry in payment_order.get("references"))

	company_email = frappe.db.get_value("Company",
		filters={'name' : payment_order.company},
		fieldname=['email'])


	product_code, client_code = frappe.db.get_value("Bank Account",
		filters={'name' : payment_order.company_bank_account},
		fieldname=['product_code', 'client_code'])

	header, file_name = get_header_row(payment_order, client_code)
	batch = get_batch_row(payment_order, no_of_records, total_amount, product_code)

	detail = []
	for ref_doc in payment_order.get("references"):
		detail += get_detail_row(ref_doc, payment_order, company_email)

	trailer = get_trailer_row(no_of_records, total_amount)
	detail_records = "\n".join(detail)

	return "\n".join([header, batch, detail_records, trailer]), file_name

@frappe.whitelist()
def generate_report(name):
	data, file_name = create_bank_remittance_txt(name)

	f = frappe.get_doc({
		'doctype': 'File',
		'file_name': file_name,
		'content': data,
		"attached_to_doctype": 'Payment Order',
		"attached_to_name": name,
		'is_private': True
	})
	f.save()
	return {
		'file_url': f.file_url,
		'file_name': file_name
	}

def generate_file_name(name, company_account, date):
	''' generate file name with format (account_code)_mmdd_(payment_order_no) '''
	bank, acc_no = frappe.db.get_value("Bank Account", {"name": company_account}, ['bank', 'bank_account_no'])
	return bank[:1]+str(acc_no)[-4:]+'_'+date.strftime("%m%d")+sanitize_data(name, '')[4:]+'.txt'

def get_header_row(doc, client_code):
	''' Returns header row and generated file name '''
	file_name = generate_file_name(doc.name, doc.company_bank_account, doc.posting_date)
	header = ["H"]
	header.append(validate_field_size(client_code, "Client Code", 20))
	header += [''] * 3
	header.append(validate_field_size(file_name, "File Name", 20))
	return "~".join(header), file_name

def get_batch_row(doc, no_of_records, total_amount, product_code):
	batch = ["B"]
	batch.append(validate_field_size(no_of_records, "No Of Records", 5))
	batch.append(validate_amount(format(total_amount, '0.2f'), 17))
	batch.append(sanitize_data(doc.name, '_')[:20])
	batch.append(format_date(doc.posting_date))
	batch.append(validate_field_size(product_code,"Product Code", 20))
	return "~".join(batch)

def get_detail_row(ref_doc, payment_entry, company_email):

	payment_date = format_date(payment_entry.posting_date)
	payment_entry = frappe.get_cached_doc('Payment Entry', ref_doc.payment_entry)
	supplier_bank_acc = frappe.get_cached_doc('Bank Account', ref_doc.bank_account)
	company_bank_acc_no = frappe.db.get_value("Bank Account", {'name': payment_entry.bank_account}, ['bank_account_no'])

	addr = get_primary_address(ref_doc.supplier)

	email = ','.join(filter(None, [addr.email_id, company_email]))

	detail = OrderedDict(
		record_identifier='D',
		payment_ref_no=sanitize_data(ref_doc.payment_entry),
		payment_type=cstr(payment_entry.mode_of_payment)[:10],
		amount=str(validate_amount(format(ref_doc.amount, '.2f'),13)),
		payment_date=payment_date,
		instrument_date=payment_date,
		instrument_number='',
		dr_account_no_client=str(validate_field_size(company_bank_acc_no, "Company Bank Account", 20)),
		dr_description='',
		dr_ref_no='',
		cr_ref_no='',
		bank_code_indicator='M',
		beneficiary_code='',
		beneficiary_name=sanitize_data(validate_information(payment_entry, "party", 160), ' '),
		beneficiary_bank='',
		beneficiary_branch_code=cstr(validate_information(supplier_bank_acc, "branch_code", 11)),
		beneficiary_acc_no=validate_information(supplier_bank_acc, "bank_account_no", 20),
		location='',
		print_location='',
		beneficiary_address_1=validate_field_size(sanitize_data(cstr(addr.address_line1), ' '), " Beneficiary Address 1", 50),
		beneficiary_address_2=validate_field_size(sanitize_data(cstr(addr.address_line2), ' '), " Beneficiary Address 2", 50),
		beneficiary_address_3='',
		beneficiary_address_4='',
		beneficiary_address_5='',
		beneficiary_city=validate_field_size(cstr(addr.city), "Beneficiary City", 20),
		beneficiary_zipcode=validate_field_size(cstr(addr.pincode), "Pin Code", 6),
		beneficiary_state=validate_field_size(cstr(addr.state), "Beneficiary State", 20),
		beneficiary_email=cstr(email)[:255],
		beneficiary_mobile=validate_field_size(cstr(addr.phone), "Beneficiary Mobile", 10),
		payment_details_1='',
		payment_details_2='',
		payment_details_3='',
		payment_details_4='',
		delivery_mode=''
	)
	detail_record = ["~".join(list(detail.values()))]

	detail_record += get_advice_rows(payment_entry)
	return detail_record

def get_advice_rows(payment_entry):
	''' Returns multiple advice rows for a single detail entry '''
	payment_entry_date = payment_entry.posting_date.strftime("%b%y%d%m").upper()
	mode_of_payment = payment_entry.mode_of_payment
	advice_rows = []
	for record in payment_entry.references:
		advice = ['E']
		advice.append(cstr(mode_of_payment))
		advice.append(cstr(record.total_amount))
		advice.append('')
		advice.append(cstr(record.outstanding_amount))
		advice.append(record.reference_name)
		advice.append(format_date(record.due_date))
		advice.append(payment_entry_date)
		advice_rows.append("~".join(advice))
	return advice_rows

def get_trailer_row(no_of_records, total_amount):
	''' Returns trailer row '''
	trailer = ["T"]
	trailer.append(validate_field_size(no_of_records, "No of Records", 5))
	trailer.append(validate_amount(format(total_amount, "0.2f"), 17))
	return "~".join(trailer)

def sanitize_data(val, replace_str=''):
	''' Remove all the non-alphanumeric characters from string '''
	pattern = re.compile('[\W_]+')
	return pattern.sub(replace_str, val)

def format_date(val):
	''' Convert a datetime object to DD/MM/YYYY format '''
	if not val: return ''

	return val.strftime("%d/%m/%Y")

def validate_amount(val, max_int_size):
	''' Validate amount to be within the allowed limits  '''
	int_size = len(str(val).split('.')[0])

	if int_size > max_int_size:
		frappe.throw(_("Amount for a single transaction exceeds maximum allowed amount, create a separate payment order by splitting the transactions"))

	return val

def validate_information(obj, attr, max_size):
	''' Checks if the information is not set in the system and is within the size '''
	if getattr(obj, attr, None):
		form_link = get_link_to_form(obj.doctype, obj.name)
		return validate_field_size(getattr(obj, attr), frappe.unscrub(attr), max_size, form_link)

	else:
		frappe.throw(_("{0} is mandatory for generating remittance payments, set the field and try again".format(frappe.unscrub(attr))))

def validate_field_size(val, label, max_size, form_link=''):
	''' check the size of the val '''
	message = ''
	if form_link:
		message = ', Please change the details in the '+form_link
	if len(cstr(val)) > max_size:
		frappe.throw(_("{0} field is limited to size {1} {2}".format(label, max_size, message)))
	return cstr(val)

def get_primary_address(supplier):

	address_list = frappe._dict(frappe.db.sql('''
		Select
			addr.name, addr.is_primary_address 
		FROM `tabDynamic Link` dl, `tabAddress` addr 
		WHERE
			dl.link_name=%s
			and dl.parent = addr.name
			and (addr.address_type='Billing' or addr.is_primary_address = 1)''', (supplier)))

	if not address_list:
		frappe.throw(_('Please assign a billing address for the supplier {0} and try again').format(supplier))

	for address, primary_addr in address_list.items():
		if primary_addr:
			addr = address
			break
		else:
			addr = address

	return frappe.get_cached_doc('Address', addr)