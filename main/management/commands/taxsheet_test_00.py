from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        from main import taxsheet as tax
        from main import testtaxsheet as tst_tx
        
        tst_cls = tax.TaxUser(tst_tx.name,
                          tst_tx.ssn,
                          tst_tx.dob,
                          tst_tx.desired_retirement_age,
                          tst_tx.life_exp,
                          tst_tx.retirement_lifestyle,
                          tst_tx.reverse_mort,
                          tst_tx.house_value,
                          tst_tx.filing_status,
                          tst_tx.retire_earn_at_fra,
                          tst_tx.retire_earn_under_fra,
                          tst_tx.total_income,
                          tst_tx.adj_gross,
                          tst_tx.federal_taxable_income,
                          tst_tx.federal_regular_tax,
                          tst_tx.state_tax_after_credits,
                          tst_tx.state_effective_rate_to_agi,
                          tst_tx.after_tax_income,
                          tst_tx.fica,
                          tst_tx.other_income,
                          tst_tx.ss_fra_retirement,
                          tst_tx.paid_days,
                          tst_tx.ira_rmd_factor,
                          tst_tx.initial_401k_balance,
                          tst_tx.inflation_level,
                          tst_tx.risk_profile_over_cpi,
                          tst_tx.projected_income_growth,
                          tst_tx.contrib_rate_employee_401k,
                          tst_tx.contrib_rate_employer_401k)
    
        tst_cls.create_maindf()
        
