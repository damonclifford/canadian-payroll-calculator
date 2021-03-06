from django.db import models


class Payroll(models.Model):
    '''
    Represents a single payroll entry.
    
    '''
    employee = models.ForeignKey('employee.Employee')
    salary = models.FloatField(default='0.00', 
        help_text='Salary or wages for the pay period')
    ei_insurable_earnings = models.FloatField(default='0.00', 
        help_text='Total EI insurable earnings for the pay period')
    taxable_income = models.FloatField(default='0.00', 
        help_text='Taxable income')
    cash_income = models.FloatField(default='0.00', 
        help_text='Cash income for the pay period')
    federal_tax_deductions = models.FloatField('Federal', default='0.00', 
        help_text='Federal tax deductions')
    provincial_tax_deductions = models.FloatField('Provincial', default='0.00', 
        help_text='Provincial tax deductions')
    additional_tax_deductions = models.FloatField(default='0.00', 
        help_text='Requested additional tax deduction')
    total_tax_on_income = models.FloatField(default='0.00', 
        help_text='Total tax on income')
    cpp_deductions = models.FloatField('CPP', default=0.00, 
        help_text='CPP deductions')
    ei_deductions = models.FloatField('EI', default=0.00, 
        help_text='EI deductions') 
    amounts_deducted_at_source = models.FloatField(default='0.00', 
        help_text='Amounts deducted at source')
    total_deductions_on_income = models.FloatField(default='0.00', 
        help_text='Total deductions on income')
    net_amount = models.FloatField(default='0.00', 
        help_text='Net amount')
    paid = models.BooleanField(default=False, 
        help_text='Whether this has been paid or not.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField()
        
    def __unicode__(self):
        return '%s (%s)' % (self.employee, self.created_at)

    def corporate_payable_tax(self):
        '''
        Total Corporate Tax = Fed + Provincial + CPP * 2 + EI * 2.4
                
        CPP: http://www.cra-arc.gc.ca/tx/bsnss/tpcs/pyrll/clcltng/cpp-rpc/menu-eng.html
        EI: http://www.cra-arc.gc.ca/tx/bsnss/tpcs/pyrll/clcltng/ei/menu-eng.html
        
        '''
        # TODO: This old calculation is wrong. Use corporate_payable_tax2.
        # return self.total_deductions_on_income + \
        #        self.cpp_deductions * 2 + \
        #        self.ei_deductions * 2.4        
        return self.total_deductions_on_income + self.cpp_deductions + self.ei_deductions * 0.4
    
    def total_ei_deductions(self):
        # Corporate EI owing
        return self.ei_deductions * 2.4
        
    def total_cpp_deductions(self):
        # Corporate CPP owing
        return self.cpp_deductions * 2
        
    def total_tax_deductions(self):
        # Federal + Provincal Tax
        return self.federal_tax_deductions + self.provincial_tax_deductions
    
    def corporate_payable_tax2(self):
        # import pdb;pdb.set_trace()
        # return self.total_deductions_on_income + \
        #        self.ei_deductions * 1.4 + \
        #        self.cpp_deductions
        return self.total_tax_deductions() + \
               self.total_cpp_deductions() + \
               self.total_ei_deductions()
    
    def total_liability(self):
        return self.corporate_payable_tax2() + self.net_amount