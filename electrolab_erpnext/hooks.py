# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "electrolab_erpnext"
app_title = "Electrolab Erpnext"
app_publisher = "Frappe"
app_description = "Electrolab erpnext app"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/electrolab_erpnext/css/electrolab_erpnext.css"
# app_include_js = "/assets/electrolab_erpnext/js/electrolab_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/electrolab_erpnext/css/electrolab_erpnext.css"
# web_include_js = "/assets/electrolab_erpnext/js/electrolab_erpnext.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Payment Order" : "public/js/Payment Order.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "electrolab_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "electrolab_erpnext.install.before_install"
# after_install = "electrolab_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "electrolab_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"electrolab_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"electrolab_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"electrolab_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"electrolab_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"electrolab_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "electrolab_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "electrolab_erpnext.event.get_events"
# }

