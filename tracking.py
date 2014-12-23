from openerp.osv import fields,osv
from openerp import tools
from tools.translate import _
from datetime import datetime

class tracking(osv.Model):
    
	_name = 'tracking.tracking'

	_columns = {                                                                                                                                                                                                                                                                                             
		'tier' : fields.selection([('Production Reference','Production Reference'),('Golden Reference','Golden Reference'),('Engineeering Sample','Engineering Sample'),('Mechanical Sample','Mechanical Sample'),('Failure Model Sample','Failure Model Sample'),('SW Test Sample','SW Test Sample')],'Tier'),
		'project_id' : fields.many2one('project.project','Project'),
		'version': fields.many2one('res.states', string="Version"),
		'condition' : fields.selection([('Active','Active'),('Defective-Unrepairable','Defective-Unrepairable'),('Defective-Needs Repair','Defective-Needs Repair'),('Destroy/Discard/EOL','Destroy/Discard/EOL')],'Condition'),
		'sample_data1' : fields.binary('Sample Data 1'),
		'sample_data2' : fields.binary('Sample Data 2'),
		'sample_data3' : fields.binary('Sample Data 3'),
		'type' : fields.selection([('Electronics','Electronics'),('Driver','Driver'),('System','System')],'Type',required=True),
		'electronics_type' : fields.selection([('Audio','Audio'),('Functional','Functional'),('Wireless','Wireless'),('All','All')],'Sub-Type'),
		'driver_type' : fields.selection([('Frequency Response','Frequency Response'),('Impedance','Impedance'),('Distortion','Distortion'),('Rub & Buzz','Rub & Buzz'),('All','All')],'Sub-Type'),
		'system_type' : fields.selection([('Frequency Response','Frequency Response'),('Impedance','Impedance'),('Distortion','Distortion'),('Rub & Buzz','Rub & Buzz'),('Airleak','Airleak'),('Cosmetic','Cosmetic'),('Wireless','Wireless'),('Functional','Functional'),('All','All')],'Sub-Type'),
        'verification_interval' : fields.char(string="Verification Interval",size=256),
        'name' : fields.char('Serial Number',required=True),
        'production_serial_number' : fields.char(string="Production Serial Number",size=256),
        'sample_ids' : fields.one2many('tracking.sample','tracking_id','Sample Data'),
        'date_ids' : fields.one2many('tracking.verification','tracking_id','Verification History For * Tier'),
        'check_in_ids' : fields.one2many('tracking.check_in','serial_number',string='Check In'),
        'check_out_ids' : fields.one2many('tracking.check_out','serial_number',string='Check Out'),
    }

class sample(osv.Model):
	
	_name = 'tracking.sample'

	_columns = {
        'tracking_id' : fields.many2one('tracking.tracking',ondelete='cascade',string="Tracking"),
        'sample_data_x' : fields.char(string="Sample Data X",size=10),
        'sample_data_y' : fields.char(string="Sample Data Y",size=10),
	}
	
class verification(osv.Model):
	
	_name = 'tracking.verification'

	_columns = {
	    'tracking_id' : fields.many2one('tracking.tracking',ondelete='cascade',string="Tracking"),
	    'partner_id' : fields.many2one('res.partner','Who'),
	    'date' : fields.date('Date'),
	    'verification_ids' : fields.many2many('tracking.tracking','tracking_verification_rel','verification_id','tracking_id',string='Related Sample'),
	}

class location(osv.Model):
	
	_name = 'tracking.location'

	_columns = {
	    'scan_location_x' : fields.char('Scan Location X'),
	    'scan_location_y' : fields.char('Scan Location Y'),
	    'on_line' : fields.char('On Line'),
	    'lent_out' : fields.many2one('res.partner','Lent Out'),
	    'with_department_member' : fields.many2one('res.partner','With Department Member'),
	}

class check_in(osv.Model):

	_name = 'tracking.check_in'

	_columns = {
	    'serial_number': fields.many2one('tracking.tracking',  string="Serial Number",required=True),   
        'time_now' : fields.datetime('Time',readonly=True),
        'create_uid': fields.many2one('res.users', 'Created by', readonly=True),
	}
    
	_defaults = {
		'time_now': lambda self, cr, uid, context={}: context.get('time_now', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		}

class check_out(osv.Model):

	_name = 'tracking.check_out'

	_columns = {
	    'tracking_id' : fields.many2one('tracking.tracking','Tracking'),
	    'serial_number': fields.many2one('tracking.tracking',  string="Serial Number",required=True),
	    'create_uid': fields.many2one('res.users', 'Created by', readonly=True),
	    'time_now' : fields.datetime('Time',readonly=True),
	    'use' : fields.selection([('On Production Line','On Production Line'),('With Department Member','With Department Member'),('Lent Out','Lent Out')],'Use'),
	    'who' : fields.char('Who'),
	    #'state': field.selection([('Checked In','Checked in'),('Checked out','Checked out')],'State'),
	}

	_defaults = {
		'time_now' : lambda self, cr, uid, context={}: context.get('time_now', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		}

class check(osv.Model):

	_name = 'tracking.check'

	def _check_in_out(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for i in self.browse(cr, uid, ids,context=context):
			if i.serial_number.id and i.state == "checked-in":
				res[i.id]= str(i.state)
			else:
				res[i.id]= "check-in" 
		return res

	def _check_io_(self, cr, uid, ids, field_name, arg, context=None):
		checkin = "checked_in"
		checkout = "checked_out" 

		if self.browse(cr, uid, ids,context=context).serial_number and self.browse(cr, uid, ids,context=context).state == "checked-in":
			return  str(checkout)
		else: #serial_number.id and state == "checked_out":
			return str(checkin)
	_columns = {
		'serial_number': fields.many2one('tracking.tracking',string="Serial Number",required=True),
		'state' : fields.function(_check_io_,type='char',string="State"),
	}

	_defaults = {
		'state' : "checked-in"
	}