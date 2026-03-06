"""Configuration and constants."""


def get_deduction_rate(country: str) -> float:
    """
    Get TDS deduction rate by country.

    Args:
        country: Country name

    Returns:
        TDS rate as a decimal (e.g., 0.10 for 10%)
    """
    country_normalized = country.strip().lower()

    if country_normalized == "india":
        return 0.10
    elif country_normalized in ("united states", "usa", "us"):
        return 0.12
    else:
        return 0.0
