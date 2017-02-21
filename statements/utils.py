from functools import reduce
from main import constants
from retiresmartz.models import RetirementPlan
from django.core.exceptions import ObjectDoesNotExist
import math

def get_lifestyle_box(client):
    return [
        {
            'target': True,
            'title': 'No.1: Doing OK',
            'stars': range(3),
            'subtitle': 'Lifestyle 1',
            'description': 'Largely Social Security',
            'income': round(client.income * constants.LIFESTYLE_DOING_OK_MULTIPLIER),
            'image': 'statements/retirement/lifestyle_01.png'
        },
        {
            'target': True,
            'title': 'No.2: Comfortable',
            'stars': range(4),
            'subtitle': 'Lifestyle 2',
            'description': 'Social Security + supplement',
            'income': round(client.income * constants.LIFESTYLE_COMFORTABLE_MULTIPLIER),
            'image': 'statements/retirement/lifestyle_02.png'
        },
        {
            'target': True,
            'title': 'No.3: Doing Well',
            'stars': range(5),
            'subtitle': 'Lifestyle 3',
            'description': 'Self-funded + some social security',
            'income': round(client.income * constants.LIFESTYLE_DOING_WELL_MULTIPLIER),
            'image': 'statements/retirement/lifestyle_03.png'
        },
        {
            'target': True,
            'title': 'No.4: Luxury',
            'stars': range(6),
            'subtitle': 'Lifestyle 4',
            'description': 'Self funded',
            'income': round(client.income * constants.LIFESTYLE_LUXURY_MULTIPLIER),
            'image': 'statements/retirement/lifestyle_04.png'
        }
    ]

expenseGroups = [
    {
      'label': 'Expenditures',
      'color': '#d47877'
    },
    {
      'label': 'Retirement contributions',
      'color': '#add5ff'
    },
    {
      'label': 'Savings & Investments',
      'color': '#83ad5d'
    },
    {
      'label': 'Social security & Medicare (FCIA)',
      'color': '#8a6d3b'
    },
    {
      'label': 'Tax',
      'color': '#5f9ea0'
    }
]

def get_waterfall_chart(plan, has_partner):
    expenses = plan.expenses if plan.expenses else []
    ExpenseCategory = RetirementPlan.ExpenseCategory
    sum_expenses = reduce(lambda acc, item: acc + item['amt'], expenses, 0)

    expensesGroupsMapping = {
        ExpenseCategory.ALCOHOLIC_BEVERAGE.value: 0,
        ExpenseCategory.APPAREL_SERVICES.value: 0,
        ExpenseCategory.EDUCATION.value: 0,
        ExpenseCategory.ENTERTAINMENT.value: 0,
        ExpenseCategory.FOOD.value: 0,
        ExpenseCategory.HEALTHCARE.value: 0,
        ExpenseCategory.HOUSING.value: 0,
        ExpenseCategory.INSURANCE_PENSIONS_SOCIAL_SECURITY.value: 3,
        ExpenseCategory.PERSONAL_CARE.value: 0,
        ExpenseCategory.READING.value: 0,
        ExpenseCategory.SAVINGS.value: 2,
        ExpenseCategory.TAXES.value: 4,
        ExpenseCategory.TOBACCO.value: 0,
        ExpenseCategory.TRANSPORTATION.value: 0,
        ExpenseCategory.MISCELLANEOUS.value: 0
    }

    btc = (plan.btc + (plan.partner_data['btc'] if has_partner else 0)) / 12
    sum_expenses += btc

    btc_bar = {
        'color': expenseGroups[1]['color'],
        'amt': round(btc),
        'height': btc / max(1, sum_expenses) * 100,
        'left': 0
    }

    x_axis = [expenseGroups[1]['label']] + list(map(lambda item: RetirementPlan.get_expense_category_text(item['cat']), expenses))
    y_axis = range(int(math.ceil(sum_expenses / 1000.0)) * 1000, 0, -1000)

    # TODO: Group by categories and sort by alphabetical order of x_axis
    bars = [btc_bar] + [{
        'color': expenseGroups[expensesGroupsMapping[item['cat']]]['color'],
        'amt': round(item['amt']),
        'height': item['amt'] / sum_expenses * 100,
        'left': (i + 1) * 100 / max(1, len(x_axis))
    } for i, item in enumerate(expenses)]

    return {
        'x_axis': x_axis,
        'x_unit_width': int(100 / max(1, len(x_axis)) * 100) / 100,
        'y_axis': y_axis,
        'y_unit_width': 100 / max(1, len(y_axis)),
        'legends': expenseGroups,
        'bars': bars
    }

def get_tax_situation(plan):
    try:
        p = plan.projection
        client = {
            'state_income_tax': round(p.current_percent_state_tax * 100, 2),
            'federal_income_tax': round(p.current_percent_fed_tax * 100, 2),
            'medicare': round(p.current_percent_medicare * 100, 2),
            'social_security': round(p.current_percent_soc_sec * 100, 2)
        }
        client['yours_to_keep'] = 100 - (client['state_income_tax'] + client['federal_income_tax'] + client['medicare'] + client['social_security'])

        partner = {
            'state_income_tax': round(p.part_current_percent_state_tax * 100, 2),
            'federal_income_tax': round(p.part_current_percent_fed_tax * 100, 2),
            'medicare': round(p.part_current_percent_medicare * 100, 2),
            'social_security': round(p.part_current_percent_soc_sec * 100, 2)
        }
        partner['yours_to_keep'] = 100 - (partner['state_income_tax'] + partner['federal_income_tax'] + partner['medicare'] + partner['social_security'])
        return {
            'client': client,
            'partner': partner
        }
    except ObjectDoesNotExist:
        return {
            'client': {
                'yours_to_keep': 58.05,
                'state_income_tax': 9.3,
                'federal_income_tax': 25,
                'medicare': 1.45,
                'social_security': 6.2
            },
            'partner': {
                'yours_to_keep': 58.05,
                'state_income_tax': 9.3,
                'federal_income_tax': 25,
                'medicare': 1.45,
                'social_security': 6.2
            }
        }

def get_pensions_annuities(plan):
    pa = plan.external_income.all()
    # TODO: return all the external incomes added or restrict to have only one external income
    if pa.count():
        return pa[0]
    else:
        return {
            'name': 'N/A',
            'begin_date': None,
            'amount': None
        }
