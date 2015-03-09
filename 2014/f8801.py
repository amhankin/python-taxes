from form import Form, FilingStatus

class F8801(Form):
    """Form 8801, Credit for Prior Year Minimum Tax"""
    def __init__(f, inputs, f1040, f6251):
        super(F8801, f).__init__(inputs)
        f['21'] = inputs.get('prior_amt_credit')
        if not f['21']:
            return

        f.must_file = True
        f['22'] = max(0, f1040['44'] + f1040['46'] - \
            (f1040.rowsum(['48', '49', '50', '51', '52', '53', '54']) or 0))
        f['23'] = f6251.get('33')
        f['24'] = max(0, f['22'] - f['23'])
        f.comment['25'] = 'Minimum tax credit'
        f['25'] = min(f['21'], f['24'])
        if f['25']:
            f6251.must_file = True
        f.comment['26'] = 'Credit carryforward to 2015'
        f['26'] = f['21'] - f['25']

    def title(self):
        return 'Form 8801 (for 2014 filing)'
