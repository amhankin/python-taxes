from form import Form, FilingStatus

class CO104us(Form):
    USE_TAX_STATE = 0.029
    USE_TAX_SPECIAL = {
            'Jefferson/Arvada': 0.011
            }
    USE_TAX_SPECIAL_CODE = {
            'Jefferson/Arvada': 12
            }

    def __init__(f, inputs):
        super(CO104us, f).__init__(inputs)
        f.disable_rounding = True
        f.comment['1'] = 'Sales tax for items not taxed online (or otherwise)'
        f['1'] = inputs['use_tax_co']
        f['2'] = f.USE_TAX_STATE * f['1']
        if inputs['use_tax_co'] > 0 or inputs['use_tax_co'] is not None:
            f.must_file = True
        f['3'] = f['1']
        district = inputs['use_tax_district']
        f.comment['4'] = '{:s} special district code'.format(district)
        f['4'] = f.USE_TAX_SPECIAL_CODE[district]
        f.comment['5'] = '{:s} special district tax rate'.format(district)
        f['5'] = f.USE_TAX_SPECIAL[district]
        f.comment['6'] = '{:s} special district tax'.format(district)
        f['6'] = f['3'] * f['5']
        f.comment['7'] = 'Total use tax'
        f['7'] = f['2'] + f['6']


    def title(self):
        return 'CA 540 Schedule CA'
