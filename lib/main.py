import typer
import json
from typing import List, Optional
from branding import validate_brand_name, validate_brand_color, validate_brand_logo_url
from validation import validate_chp_id, validate_household_id, validate_referral_status
from data_aggregation import aggregate_household_data, aggregate_referral_stats

app = typer.Typer(help="BomaHealth Management and Branding CLI")
@app.command(name="check-brand")
def check_brand(
    name: str = typer.Option(..., help="Brand name to validate"),
    color: str = typer.Option(..., help="Hex code or standard color name"),
    url: Optional[str] = typer.Option(None, help="Optional logo URL link")
):
    """Validate project branding parameters."""
    if not validate_brand_name(name):
        typer.secho(f"Invalid Brand Name: '{name}' (Must be 2-50 characters)", fg="red")
        raise typer.Exit(1)
        
    if not validate_brand_color(color):
        typer.secho(f"Invalid Color Format: '{color}' (Use standard names or hex strings)", fg="red")
        raise typer.Exit(1)
        
    if url and not validate_brand_logo_url(url):
        typer.secho(f"Invalid Logo URL structure: '{url}'", fg="red")
        raise typer.Exit(1)

    typer.secho(f"Branding looks great! Name: {name} | Color: {color}", fg="green")
@app.command(name="verify-id")
def verify_id(
    chp: Optional[str] = typer.Option(None, help="Verify a Community Health Promoter ID (e.g. CHP001)"),
    hh: Optional[str] = typer.Option(None, help="Verify a Household ID (e.g. HH012)")
):
    """Verify health infrastructure identification codes."""
    if chp:
        if validate_chp_id(chp):
            typer.secho(f"'{chp}' is a valid CHP Identification code.", fg="green")
        else:
            typer.secho(f"'{chp}' is an invalid CHP code. Format must match 'CHP###'", fg="red")
    if hh:
        if validate_household_id(hh):
            typer.secho(f"'{hh}' is a valid Household ID.", fg="green")
        else:
            typer.secho(f"'{hh}' is an invalid Household ID. Format must match 'HH###'", fg="red")
@app.command(name="stats")
def summary_stats(
    json_file: str = typer.Argument(..., help="Path to a JSON file containing household records array")
):
    """Aggregate survey records from a raw data file."""
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        
        results = aggregate_household_data(data)
        typer.echo(f"--- BomaHealth Aggregated Metrics ---")
        typer.echo(f"Total Logged Households : {results['total_households']}")
        typer.echo(f"Total Registered Members: {results['total_members']}")
        
    except FileNotFoundError:
        typer.secho(f"Target data file not found at: '{json_file}'", fg="red")
    except json.JSONDecodeError:
        typer.secho("Parsing Error: Provided target is not valid JSON format.", fg="red")

if __name__ == "__main__":
    app()