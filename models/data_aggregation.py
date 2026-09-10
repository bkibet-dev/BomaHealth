def aggregate_household_data(households):
    if not households:
        return {'total_households': 0, 'total_members': 0}
    total = len(households)
    members = sum(h.get('members', 0) for h in households)
    return {'total_households': total, 'total_members': members}

def aggregate_referral_stats(referrals):
    if not referrals:
        return {}
    stats = {}
    for ref in referrals:
        status = ref.get('status')
        stats[status] = stats.get(status, 0) + 1
    return stats

def aggregate_chp_performance(chp_records):
    if not chp_records:
        return []
    return sorted(chp_records, key=lambda x: x.get('resolved', 0), reverse=True)

def aggregate_by_date_range(data, start_date, end_date):
    if not data:
        return []
    return [d for d in data if start_date <= d.get('date') <= end_date]