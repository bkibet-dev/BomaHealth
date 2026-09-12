from models.referral import Referral


def create_referral_flow(referral_id, chp_id, household_id, reason=None):
    Referral.load_from_file()
    referral = Referral.create_referral(
        referral_id=referral_id, chp_id=chp_id, household_id=household_id, reason=reason
    )
    Referral.save_to_file()
    print(f"Referral {referral.referral_id} created (status: {referral.status})")


def list_referrals_flow(chp_id):
    Referral.load_from_file()
    referrals = Referral.get_referrals_for_chp(chp_id)
    if not referrals:
        print("No referrals found for this CHP.")
        return
    referrals = sorted(referrals, key=lambda r: r.created_at, reverse=True)
    for r in referrals:
        print(f"[{r.status.upper()}] {r.referral_id} — {r.household_id} ({r.created_at})")