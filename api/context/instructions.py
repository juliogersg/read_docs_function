# SALARY SLIPS
TEMPLATE_SS = """
## Task Goal
The task goal is to identify specific financial details from the extracted OCR text of a payroll slip.

## Task Instructions
You will be given a text extracted with OCR from a payroll slip in Spanish. The text contains plain text, key-value pairs, and tables. Please identify and extract the following elements:

1. **Company**: Identify the employer or entity that issued the payroll slip.
2. **Net Salary**: Find the net salary that the employee receives. It may appear as "sueldo neto", "salario neto", "remuneración neta", "saldo neto", etc.
3. **Variable Amounts**: Identify all variable amounts listed in the payroll slip, such as "bonos" (bonuses), "renta de quinta categoría" (fifth category income), "utilidades" (profits), "vacaciones" (vacation), "seguro" (insurance), "aporte" (contribution), "comisión" (commission), "gratificación" (gratuity), "alimentos" (food), "asignación familiar" (family allowance), "Essalud" (social health insurance), "EPS" (private health insurance), "incentivo" (incentive), "retención" (retention), etc. Return this as a dictionary, indicating the concept and the amount.

If you cannot find a specific value, return an empty string ("").

## Task Output:
Provide the extracted information as follows:
- Company: [Company Name]
- Net Salary: [Net Salary Amount]
- Variable Amounts: [
                      "concept": "amount",
                      ...
                    ]

## Task Input:
{ocr_content}
"""

TEMPLATE_SS_VISION = """
## Task Goal
The task goal is to identify specific financial details from the image of a payroll slip.

## Task Instructions
You will be given an image of a payroll slip in Spanish. The image contains plain text, key-value pairs, and tables. Please identify and extract the following elements:

1. **Company**: Identify the employer or entity that issued the payroll slip.
2. **Net Salary**: Find the net salary that the employee receives. It may appear as "sueldo neto", "salario neto", "remuneración neta", "saldo neto", etc.
3. **Variable Amounts**: Identify all variable amounts listed in the payroll slip, such as "bonos" (bonuses), "renta de quinta categoría" (fifth category income), "utilidades" (profits), "vacaciones" (vacation), "seguro" (insurance), "aporte" (contribution), "comisión" (commission), "gratificación" (gratuity), "alimentos" (food), "asignación familiar" (family allowance), "Essalud" (social health insurance), "EPS" (private health insurance), "incentivo" (incentive), "retención" (retention), etc. Return this as a dictionary, indicating the concept and the amount.

If you cannot find a specific value, return an empty string ("").

## Task Output:
Provide the extracted information as follows:
- Company: [Company Name]
- Net Salary: [Net Salary Amount]
- Variable Amounts: [
                      "concept": "amount",
                      ...
                    ]

## Task Input:
"""

# PAYMENT SCHEDULES
TEMPLATE_PS = """
## Task Goal
The task goal is to identify specific financial details from the extracted OCR text of a payment schedule.

## Task Instructions
You will be given a text extracted with OCR from a payment schedule in Spanish. The text contains plain text, key-value pairs and tables. Please identify and extract the following elements:

1. **Bank**: Identify the bank that issued the loan. Some known banks include: "BCP" or "Banco de crédito del Perú", "BBVA", "Scotiabank", "Interbank", "Banco Pichincha", "Mi Banco", "BanBif", "Banco Falabella", "Banco Ripley", "Banco Santander", "Alfin Banco", "BCI", etc.
2. **Monthly Payment**: Find the monthly payment amount the user pays for their loan. It may appear as "cuota", "monto", "cuota mensual", "próximo pago", etc.
3. **Total Loan Amount**: Identify the total amount loaned by the bank. It may appear as "importe de préstamo", "monto original", "crédito hipotecario", etc.
4. **Interest Rate**: Find the interest rate at which the loan was issued. It may appear as "tasa de costo efectivo", "tasa anual", "TEA", "TCEA", etc.

If you cannot find a specific value, return an empty string ("").

## Task Output:
Provide the extracted information as follows:
- Bank: [Bank Name]
- Monthly Payment: [Monthly Payment Amount]
- Total Loan Amount: [Total Loan Amount]
- Interest Rate: [Interest Rate]

## Task Input:
{ocr_content}
"""