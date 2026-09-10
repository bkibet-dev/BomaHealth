import pytest
def aggregate_household_data(households):
    pass

def aggregate_referral_stats(referrals):
    pass

def aggregate_chp_performance(chp_records):
    pass

def aggregate_by_date_range(data, start_date, end_date):
    pass

def test_aggregate_household_data_valid():
    data = [
        {'id': 'HH001', 'members': 5},
        {'id': 'HH002', 'members': 3}
    ]
    result = aggregate_household_data(data)
    assert result == {'total_households': 2, 'total_members': 8}

def test_aggregate_referral_stats_valid():
    referrals = [
        {'status': 'pending', 'chp_id': 'CHP001'},
        {'status': 'resolved', 'chp_id': 'CHP001'},
        {'status': 'pending', 'chp_id': 'CHP002'}
    ]
    result = aggregate_referral_stats(referrals)
    assert result['pending'] == 2
    assert result['resolved'] == 1

def test_aggregate_chp_performance_valid():
    records = [
        {'chp_id': 'CHP001', 'resolved': 10, 'pending': 2},
        {'chp_id': 'CHP002', 'resolved': 8, 'pending': 1}
    ]
    result = aggregate_chp_performance(records)
    assert len(result) == 2
    assert result[0]['chp_id'] == 'CHP001'

def test_aggregate_by_date_range_valid():
    data = [
        {'date': '2024-01-15', 'value': 10},
        {'date': '2024-02-20', 'value': 20}
    ]
    result = aggregate_by_date_range(data, '2024-01-01', '2024-02-28')
    assert len(result) == 2
    assert result[0]['value'] == 10