from openerp.osv import fields,osv
from openerp import tools
from tools.translate import _
from datetime import datetime

class tracking(osv.Model):
    
	_name = 'tracking.tracking'

	_sql_constraints = [('name_unique','unique(name)','You can not create a duplicate serial number')]


	_columns = {                                                                                                                                                                                                                                                                                             
		'tier' : fields.selection([
			('Production Reference','Production Reference'),
			('Golden Reference','Golden Reference'),
			('Engineeering Sample','Engineering Sample'),
			('Mechanical Sample','Mechanical Sample'),
			('Failure Model Sample','Failure Model Sample'),
			('SW Test Sample','SW Test Sample')],'Tier'),
		'project_id' : fields.char('Project/Part Number'),
		'version': fields.char('Version/NPI Stage'),
		'condition' : fields.selection([
			('Active','Active'),
			('Defective-Unrepairable','Defective-Unrepairable'),
			('Defective-Needs Repair','Defective-Needs Repair'),
			('Destroy/Discard/EOL','Destroy/Discard/EOL')],'Condition'),
		'sample_data1' : fields.binary('Sample Data 1'),
		'sample_data2' : fields.binary('Sample Data 2'),
		'sample_data3' : fields.binary('Sample Data 3'),
		'type' : fields.selection([
			('Electronics','Electronics'),
			('Driver','Driver'),
			('System','System')],'Type',required=True),
		'electronics_type' : fields.selection([
			('Audio','Audio'),
			('Functional','Functional'),
			('Wireless','Wireless'),
			('All','All')],'Sub-Type'),
		'driver_type' : fields.selection([
			('Frequency Response','Frequency Response'),
			('Impedance','Impedance'),
			('Distortion','Distortion'),
			('Rub & Buzz','Rub & Buzz'),
			('All','All')],'Sub-Type'),
		'system_type' : fields.selection([
			('Frequency Response','Frequency Response'),
			('Impedance','Impedance'),
			('Distortion','Distortion'),
			('Rub & Buzz','Rub & Buzz'),
			('Airleak','Airleak'),
			('Cosmetic','Cosmetic'),
			('Wireless','Wireless'),
			('Functional','Functional'),
			('All','All')],'Sub-Type'),
        'verification_interval' : fields.integer(string="Verification Interval"),
        'name' : fields.char('Serial Number',required=True,store=True),
        'production_serial_number' : fields.char(string="Production Serial Number",size=256),
        'sample_ids' : fields.one2many('tracking.sample','tracking_id','Sample Data'),
        'date_ids' : fields.one2many('tracking.verification','tracking_id','Verification History For * Tier'),
        'check_ids' : fields.one2many('tracking.check','name',string='Check In'),
        'location' : fields.char(string="Location",size=256),
        'partner_id': fields.char('Customer'),
        'release_date' : fields.date('Release Date'),
        'user_id' : fields.char('Approver'),
        'unit' : fields.selection([('days','days'),('weeks','weeks'),('months','months'),('years','years'),('pieces','pieces')],'Interval Unit'),
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
	    'user_id' : fields.many2one('res.users','Who'),
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



class _check_in_out(osv.Model):

	_name = 'tracking.check'

	_sql_constraints = [('name_unique','unique(name)','You can not create a duplicate serial number')]

	_columns = {
		'name': fields.many2one('tracking.tracking',string="Serial Number",required=True, store=True),
		'state' : fields.selection([('Checked-in','Checked-in'),('Checked-out','Checked-out')],"State"),
		'create_uid': fields.many2one('res.users', 'Created by', readonly=True),
		'time_now' : fields.datetime('Time',readonly=True),
		'location' : fields.char('Location'),
		'who' : fields.char('Who'),
		'project_id' : fields.related('name','project_id', readonly=True, type='char', string="Project/Part Number"),
			
	}

	_defaults = {
		'time_now' : lambda self, cr, uid, context={}: context.get('time_now', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		'state' : 'Checked-in',
	}