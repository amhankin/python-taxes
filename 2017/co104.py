from form import Form, FilingStatus
from f1040 import F1040
from co104us import CO104us
import math

class CO104(Form):
    EXEMPTION = 114
    DEPENDENT_EXEMPTION = 353
    BRACKET_RATES = [0, .0463]
    BRACKET_LIMITS = [
        [0, 551473],    # SINGLE
        [0, 551473],    # JOINT
        [0, 551473],    # SEPARATE
        [0, 551473],    # HEAD
        [0, 551473],    # WIDOW
    ]
    SDI_MAX = 998.12
    MENTAL_HEALTH_LIMIT = 1000000
    MENTAL_HEALTH_RATE = .01

    def __init__(f, inputs, f1040):
        f1040sa = None
        super(CO104, f).__init__(inputs)
        f.must_file = True
        f.addForm(f)

        for i in f1040.forms:
            if i.__class__.__name__ == 'F1040sa':
                f1040sa = i
        if f1040sa is not None:
            raise RuntimeError('Make code work for case of itemized deductions')
            return None

        # Calculate income tax from taxable income
        f.comment['1'] = 'Taxable income'
        f['1'] = f1040['43']
        f['4'] = f.rowsum(['1', '2', '3'])
        # TODO: subtractions from income schedule
        f.comment['6'] = "Colorado Taxable Income"
        f['6'] = f['4'] - f['5']
        f.comment['7'] = 'Colorado tax'
        f['7'] = f.tax_rate_schedule(inputs['status'], f['6'])
        f['10'] = f.rowsum(['7', '8', '9'])
        #f['10'] = f.rowsum(['7', '8', '9'])
        credits = f.rowsum(['11', '12'])
        f.comment['13'] = 'Net Income Tax'
        if credits is None:
            f['13'] = f['10']
        else:
            f['13'] = f['10'] - credits

        # Add use tax if sales tax not included for internet purchases
        if inputs.get('use_tax_co') is not None:
            f.comment['14'] = 'Use Tax (must submit DR 0104US)'
            co104us = CO104us(inputs)
            f.addForm(co104us)
            f['14'] = co104us['7']

        # Net tax
        f.comment['15'] = 'Net Colorado tax'
        f['15'] = f.rowsum(['13', '14'])
        
        # Figure out if you own taxes
        f.comment['16'] = 'State withholding'
        f['16'] = inputs['state_withholding']
        f['24'] = f.rowsum(['16', '17', '18', '19', '20', '21', '22', '23'])
        f['25'] = f1040['37']
        if f['24'] > f['15']:
            f['26'] = f['24'] - f['15']
        f['29'] = f.rowsum(['27', '28'])

        if f['29'] != 0:
            f.comment['30'] = 'Refund'
            f['30'] = f['26'] - f['29'] 
        else:
            f['31'] = f['15'] - f['24']
            f.comment['35'] = 'Tax Due'
            f['35'] = f.rowsum(['31', '32', '33', '34'])

    def tax_rate_schedule(f, status, val):
        # TODO: rounding of amounts less than 100000 to match tax table
        tax = 0
        prev = 0
        i = 0
        for lim in f.BRACKET_LIMITS[status]:
            if val <= lim:
                break
            tax += f.BRACKET_RATES[i] * (lim - prev)
            prev = lim
            i += 1
        tax += f.BRACKET_RATES[i] * (val - prev)
        return tax

    def title(f):
        return 'CO Form 104'
