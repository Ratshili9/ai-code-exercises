from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple


def validate_report_parameters(sales_data: Any, report_type: str, output_format: str, date_range: Optional[Dict[str, str]]) -> None:
    """Validates the input arguments for sales report generation."""
    if not sales_data or not isinstance(sales_data, list):
        raise ValueError("Sales data must be a non-empty list")

    if report_type not in ['summary', 'detailed', 'forecast']:
        raise ValueError("Report type must be 'summary', 'detailed', or 'forecast'")

    if output_format not in ['pdf', 'excel', 'html', 'json']:
        raise ValueError("Output format must be 'pdf', 'excel', 'html', or 'json'")

    if date_range:
        if 'start' not in date_range or 'end' not in date_range:
            raise ValueError("Date range must include 'start' and 'end' dates")

        start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
        end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")


def filter_sales_by_date(sales_data: List[Dict[str, Any]], date_range: Optional[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Filters sales records within the provided start and end dates."""
    if not date_range:
        return sales_data

    start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
    end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')

    return [
        sale for sale in sales_data
        if start_date <= datetime.strptime(sale['date'], '%Y-%m-%d') <= end_date
    ]


def filter_sales_by_criteria(sales_data: List[Dict[str, Any]], filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Applies arbitrary key/value or list-matching filters to the sales records."""
    if not filters:
        return sales_data

    filtered = sales_data
    for key, value in filters.items():
        if isinstance(value, list):
            filtered = [sale for sale in filtered if sale.get(key) in value]
        else:
            filtered = [sale for sale in filtered if sale.get(key) == value]
    return filtered


def calculate_summary_metrics(sales_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes total, average, minimum, and maximum sale amounts."""
    total_sales = sum(sale['amount'] for sale in sales_data)
    avg_sale = total_sales / len(sales_data)
    max_sale = max(sales_data, key=lambda x: x['amount'])
    min_sale = min(sales_data, key=lambda x: x['amount'])

    return {
        'total_sales': total_sales,
        'transaction_count': len(sales_data),
        'average_sale': avg_sale,
        'max_sale': {
            'amount': max_sale['amount'],
            'date': max_sale['date'],
            'details': max_sale
        },
        'min_sale': {
            'amount': min_sale['amount'],
            'date': min_sale['date'],
            'details': min_sale
        }
    }


def aggregate_by_grouping(sales_data: List[Dict[str, Any]], grouping: str, total_sales: float) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Groups transactions by a specific field and calculates group totals, averages, and percentages."""
    raw_groups: Dict[str, Dict[str, Any]] = {}
    for sale in sales_data:
        key = sale.get(grouping, 'Unknown')
        if key not in raw_groups:
            raw_groups[key] = {'count': 0, 'total': 0.0, 'items': []}
        raw_groups[key]['count'] += 1
        raw_groups[key]['total'] += sale['amount']
        raw_groups[key]['items'].append(sale)

    formatted_groups: Dict[str, Any] = {}
    for key, data in raw_groups.items():
        average = data['total'] / data['count']
        data['average'] = average
        formatted_groups[key] = {
            'count': data['count'],
            'total': data['total'],
            'average': average,
            'percentage': (data['total'] / total_sales) * 100 if total_sales > 0 else 0
        }

    return raw_groups, {'by': grouping, 'groups': formatted_groups}


def build_detailed_transactions(sales_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enriches transaction records with calculated profit, margin, and pre-tax values."""
    detailed_transactions = []
    for sale in sales_data:
        transaction = dict(sale)
        if 'tax' in sale and 'amount' in sale:
            transaction['pre_tax'] = sale['amount'] - sale['tax']
        if 'cost' in sale and 'amount' in sale:
            transaction['profit'] = sale['amount'] - sale['cost']
            transaction['margin'] = (transaction['profit'] / sale['amount']) * 100 if sale['amount'] > 0 else 0
        detailed_transactions.append(transaction)
    return detailed_transactions


def build_forecast_analysis(sales_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates monthly sales history, growth rate trajectories, and 3-month forward projections."""
    monthly_sales: Dict[str, float] = {}
    for sale in sales_data:
        sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        month_key = f"{sale_date.year}-{sale_date.month:02d}"
        monthly_sales[month_key] = monthly_sales.get(month_key, 0.0) + sale['amount']

    sorted_months = sorted(monthly_sales.keys())
    growth_rates = []
    for i in range(1, len(sorted_months)):
        prev_amt = monthly_sales[sorted_months[i - 1]]
        curr_amt = monthly_sales[sorted_months[i]]
        if prev_amt > 0:
            growth_rates.append(((curr_amt - prev_amt) / prev_amt) * 100)

    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0.0

    forecast = {}
    if sorted_months:
        last_month = sorted_months[-1]
        last_amount = monthly_sales[last_month]
        year, month = map(int, last_month.split('-'))

        for _ in range(1, 4):
            month += 1
            if month > 12:
                month = 1
                year += 1
            forecast_month = f"{year}-{month:02d}"
            forecast_amount = last_amount * (1 + (avg_growth_rate / 100))
            forecast[forecast_month] = forecast_amount
            last_amount = forecast_amount

    return {
        'monthly_sales': monthly_sales,
        'growth_rates': {sorted_months[i]: growth_rates[i - 1] for i in range(1, len(sorted_months))},
        'average_growth_rate': avg_growth_rate,
        'projected_sales': forecast
    }


def generate_chart_visualizations(sales_data: List[Dict[str, Any]], raw_groups: Optional[Dict[str, Any]], grouping: Optional[str]) -> Dict[str, Any]:
    """Generates data series payloads for time-series and categorical charts."""
    date_sales: Dict[str, float] = {}
    for sale in sales_data:
        date_sales[sale['date']] = date_sales.get(sale['date'], 0.0) + sale['amount']

    sorted_dates = sorted(date_sales.keys())
    charts_data = {
        'sales_over_time': {
            'labels': sorted_dates,
            'data': [date_sales[d] for d in sorted_dates]
        }
    }

    if grouping and raw_groups:
        charts_data[f'sales_by_{grouping}'] = {
            'labels': list(raw_groups.keys()),
            'data': [group['total'] for group in raw_groups.values()]
        }

    return charts_data


def render_report_output(report_data: Dict[str, Any], output_format: str, include_charts: bool) -> Any:
    """Dispatches the populated report data to the specified serializer format."""
    if output_format == 'json':
        return report_data
    elif output_format == 'html':
        return _generate_html_report(report_data, include_charts)
    elif output_format == 'excel':
        return _generate_excel_report(report_data, include_charts)
    elif output_format == 'pdf':
        return _generate_pdf_report(report_data, include_charts)


def generate_sales_report(sales_data, report_type='summary', date_range=None,
                          filters=None, grouping=None, include_charts=False,
                          output_format='pdf'):
    """
    Generate a comprehensive sales report by orchestrating modular decomposition functions.
    """
    validate_report_parameters(sales_data, report_type, output_format, date_range)

    # 1. Apply Filtering Pipeline
    sales_data = filter_sales_by_date(sales_data, date_range)
    sales_data = filter_sales_by_criteria(sales_data, filters)

    if not sales_data:
        print("Warning: No data matches the specified criteria")
        if output_format == 'json':
            return {"message": "No data matches the specified criteria", "data": []}
        else:
            return _generate_empty_report(report_type, output_format)

    # 2. Compute Summary Metrics
    summary_metrics = calculate_summary_metrics(sales_data)

    # 3. Assemble Base Report Structure
    report_data = {
        'report_type': report_type,
        'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': date_range,
        'filters': filters,
        'summary': summary_metrics
    }

    # 4. Process Optional Grouping
    raw_groups = None
    if grouping:
        raw_groups, grouping_payload = aggregate_by_grouping(sales_data, grouping, summary_metrics['total_sales'])
        report_data['grouping'] = grouping_payload

    # 5. Process Type-Specific Payload
    if report_type == 'detailed':
        report_data['transactions'] = build_detailed_transactions(sales_data)
    elif report_type == 'forecast':
        report_data['forecast'] = build_forecast_analysis(sales_data)

    # 6. Generate Charts
    if include_charts:
        report_data['charts'] = generate_chart_visualizations(sales_data, raw_groups, grouping)

    # 7. Render Output
    return render_report_output(report_data, output_format, include_charts)


# Stub helper functions
def _generate_empty_report(report_type, output_format):
    pass

def _generate_html_report(report_data, include_charts):
    pass

def _generate_excel_report(report_data, include_charts):
    pass

def _generate_pdf_report(report_data, include_charts):
    pass