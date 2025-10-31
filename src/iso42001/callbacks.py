from dash import callback, Input, Output, State, html, ctx
import dash_bootstrap_components as dbc
from datetime import datetime
import base64
import io
import pandas as pd

from .database import ISO42001Database

# Initialize database connection
db = ISO42001Database()

def create_data_table(df, table_id):
    """Create a standard data table with Carbon styling"""
    from .app import create_data_table as app_create_data_table
    return app_create_data_table(df, table_id)

# Asset callbacks
@callback(
    Output("asset-modal", "is_open", allow_duplicate=True),
    [Input("add-asset-btn", "n_clicks"), 
     Input("submit-asset", "n_clicks"), 
     Input("cancel-asset", "n_clicks")],
    [State("asset-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_asset_modal(add_clicks, submit_clicks, cancel_clicks, is_open):
    """Toggle asset modal visibility"""
    if ctx.triggered_id in ["add-asset-btn", "submit-asset", "cancel-asset"]:
        return not is_open
    return False

@callback(
    [Output("assets-table-container", "children", allow_duplicate=True),
     Output("asset-name", "value", allow_duplicate=True),
     Output("asset-type", "value", allow_duplicate=True),
     Output("asset-description", "value", allow_duplicate=True),
     Output("asset-criticality", "value", allow_duplicate=True),
     Output("asset-owner", "value", allow_duplicate=True),
     Output("asset-status", "value", allow_duplicate=True),
     Output("asset-modal", "is_open", allow_duplicate=True)],
    [Input("submit-asset", "n_clicks")],
    [State("asset-name", "value"),
     State("asset-type", "value"),
     State("asset-description", "value"),
     State("asset-criticality", "value"),
     State("asset-owner", "value"),
     State("asset-status", "value")],
    prevent_initial_call=True
)
def add_asset(n_clicks, name, asset_type, description, criticality, owner, status):
    """Add new asset and refresh table"""
    if n_clicks and name and asset_type:
        try:
            db.add_asset(name, asset_type, description or "", criticality or "Medium", 
                        owner or "", status or "Active")
            
            # Refresh table
            assets_df = db.get_assets()
            table = create_data_table(assets_df, "assets-table")
            
            # Clear form and close modal
            return table, "", "", "", "Medium", "", "Active", False
        except Exception as e:
            print(f"Error adding asset: {e}")
    
    # Return current state without changes
    try:
        assets_df = db.get_assets()
        table = create_data_table(assets_df, "assets-table")
        return table, "", "", "", "Medium", "", "Active", False
    except:
        return html.Div("Error loading assets"), "", "", "", "Medium", "", "Active", False

# Risk callbacks
@callback(
    Output("risk-modal", "is_open", allow_duplicate=True),
    [Input("add-risk-btn", "n_clicks"), 
     Input("submit-risk", "n_clicks"), 
     Input("cancel-risk", "n_clicks")],
    [State("risk-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_risk_modal(add_clicks, submit_clicks, cancel_clicks, is_open):
    """Toggle risk modal visibility"""
    if ctx.triggered_id in ["add-risk-btn", "submit-risk", "cancel-risk"]:
        return not is_open
    return False

@callback(
    [Output("risks-table-container", "children", allow_duplicate=True),
     Output("risk-asset", "value", allow_duplicate=True),
     Output("risk-title", "value", allow_duplicate=True),
     Output("risk-description", "value", allow_duplicate=True),
     Output("risk-category", "value", allow_duplicate=True),
     Output("risk-likelihood", "value", allow_duplicate=True),
     Output("risk-impact", "value", allow_duplicate=True),
     Output("risk-level", "value", allow_duplicate=True),
     Output("risk-mitigation", "value", allow_duplicate=True),
     Output("risk-owner", "value", allow_duplicate=True),
     Output("risk-status", "value", allow_duplicate=True),
     Output("risk-modal", "is_open", allow_duplicate=True)],
    [Input("submit-risk", "n_clicks")],
    [State("risk-asset", "value"),
     State("risk-title", "value"),
     State("risk-description", "value"),
     State("risk-category", "value"),
     State("risk-likelihood", "value"),
     State("risk-impact", "value"),
     State("risk-level", "value"),
     State("risk-mitigation", "value"),
     State("risk-owner", "value"),
     State("risk-status", "value")],
    prevent_initial_call=True
)
def add_risk(n_clicks, asset, title, description, category, likelihood, impact, 
            risk_level, mitigation, owner, status):
    """Add new risk and refresh table"""
    if n_clicks and title:
        try:
            # Extract asset ID from dropdown value (format: "1 - Asset Name")
            asset_id = None
            if asset:
                asset_id = int(asset.split(" - ")[0])
            
            db.add_risk(asset_id, title, description or "", category or "", 
                       likelihood or "Medium", impact or "Medium", risk_level or "Medium",
                       mitigation or "", owner or "", status or "Open")
            
            # Refresh table
            risks_df = db.get_risks()
            table = create_data_table(risks_df, "risks-table")
            
            # Clear form and close modal
            return table, "", "", "", "", "Medium", "Medium", "Medium", "", "", "Open", False
        except Exception as e:
            print(f"Error adding risk: {e}")
    
    # Return current state
    try:
        risks_df = db.get_risks()
        table = create_data_table(risks_df, "risks-table")
        return table, "", "", "", "", "Medium", "Medium", "Medium", "", "", "Open", False
    except:
        return html.Div("Error loading risks"), "", "", "", "", "Medium", "Medium", "Medium", "", "", "Open", False

# Control callbacks
@callback(
    Output("control-modal", "is_open", allow_duplicate=True),
    [Input("add-control-btn", "n_clicks"), 
     Input("submit-control", "n_clicks"), 
     Input("cancel-control", "n_clicks")],
    [State("control-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_control_modal(add_clicks, submit_clicks, cancel_clicks, is_open):
    """Toggle control modal visibility"""
    if ctx.triggered_id in ["add-control-btn", "submit-control", "cancel-control"]:
        return not is_open
    return False

@callback(
    [Output("controls-table-container", "children", allow_duplicate=True),
     Output("control-id", "value", allow_duplicate=True),
     Output("control-name", "value", allow_duplicate=True),
     Output("control-description", "value", allow_duplicate=True),
     Output("control-type", "value", allow_duplicate=True),
     Output("control-implementation", "value", allow_duplicate=True),
     Output("control-effectiveness", "value", allow_duplicate=True),
     Output("control-owner", "value", allow_duplicate=True),
     Output("control-modal", "is_open", allow_duplicate=True)],
    [Input("submit-control", "n_clicks")],
    [State("control-id", "value"),
     State("control-name", "value"),
     State("control-description", "value"),
     State("control-type", "value"),
     State("control-implementation", "value"),
     State("control-effectiveness", "value"),
     State("control-owner", "value")],
    prevent_initial_call=True
)
def add_control(n_clicks, control_id, name, description, control_type, 
               implementation, effectiveness, owner):
    """Add new control and refresh table"""
    if n_clicks and control_id and name:
        try:
            db.add_control(control_id, name, description or "", control_type or "Preventive",
                          implementation or "Not Started", effectiveness or "Not Assessed", 
                          owner or "")
            
            # Refresh table
            controls_df = db.get_controls()
            table = create_data_table(controls_df, "controls-table")
            
            # Clear form and close modal
            return table, "", "", "", "Preventive", "Not Started", "Not Assessed", "", False
        except Exception as e:
            print(f"Error adding control: {e}")
    
    # Return current state
    try:
        controls_df = db.get_controls()
        table = create_data_table(controls_df, "controls-table")
        return table, "", "", "", "Preventive", "Not Started", "Not Assessed", "", False
    except:
        return html.Div("Error loading controls"), "", "", "", "Preventive", "Not Started", "Not Assessed", "", False

# Incident callbacks
@callback(
    Output("incident-modal", "is_open", allow_duplicate=True),
    [Input("add-incident-btn", "n_clicks"), 
     Input("submit-incident", "n_clicks"), 
     Input("cancel-incident", "n_clicks")],
    [State("incident-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_incident_modal(add_clicks, submit_clicks, cancel_clicks, is_open):
    """Toggle incident modal visibility"""
    if ctx.triggered_id in ["add-incident-btn", "submit-incident", "cancel-incident"]:
        return not is_open
    return False

@callback(
    [Output("incidents-table-container", "children", allow_duplicate=True),
     Output("incident-title", "value", allow_duplicate=True),
     Output("incident-description", "value", allow_duplicate=True),
     Output("incident-severity", "value", allow_duplicate=True),
     Output("incident-assets", "value", allow_duplicate=True),
     Output("incident-root-cause", "value", allow_duplicate=True),
     Output("incident-actions", "value", allow_duplicate=True),
     Output("incident-status", "value", allow_duplicate=True),
     Output("incident-reported-by", "value", allow_duplicate=True),
     Output("incident-assigned-to", "value", allow_duplicate=True),
     Output("incident-modal", "is_open", allow_duplicate=True)],
    [Input("submit-incident", "n_clicks")],
    [State("incident-title", "value"),
     State("incident-description", "value"),
     State("incident-severity", "value"),
     State("incident-assets", "value"),
     State("incident-root-cause", "value"),
     State("incident-actions", "value"),
     State("incident-status", "value"),
     State("incident-reported-by", "value"),
     State("incident-assigned-to", "value")],
    prevent_initial_call=True
)
def add_incident(n_clicks, title, description, severity, assets, root_cause, 
                actions, status, reported_by, assigned_to):
    """Add new incident and refresh table"""
    if n_clicks and title:
        try:
            db.add_incident(title, description or "", severity or "Medium", assets or "",
                           root_cause or "", actions or "", status or "Open", 
                           reported_by or "", assigned_to or "")
            
            # Refresh table
            incidents_df = db.get_incidents()
            table = create_data_table(incidents_df, "incidents-table")
            
            # Clear form and close modal
            return table, "", "", "Medium", "", "", "", "Open", "", "", False
        except Exception as e:
            print(f"Error adding incident: {e}")
    
    # Return current state
    try:
        incidents_df = db.get_incidents()
        table = create_data_table(incidents_df, "incidents-table")
        return table, "", "", "Medium", "", "", "", "Open", "", "", False
    except:
        return html.Div("Error loading incidents"), "", "", "Medium", "", "", "", "Open", "", "", False

# Audit callbacks
@callback(
    Output("audit-modal", "is_open", allow_duplicate=True),
    [Input("add-audit-btn", "n_clicks"), 
     Input("submit-audit", "n_clicks"), 
     Input("cancel-audit", "n_clicks")],
    [State("audit-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_audit_modal(add_clicks, submit_clicks, cancel_clicks, is_open):
    """Toggle audit modal visibility"""
    if ctx.triggered_id in ["add-audit-btn", "submit-audit", "cancel-audit"]:
        return not is_open
    return False

@callback(
    [Output("audits-table-container", "children", allow_duplicate=True),
     Output("audit-title", "value", allow_duplicate=True),
     Output("audit-type", "value", allow_duplicate=True),
     Output("audit-scope", "value", allow_duplicate=True),
     Output("audit-auditor", "value", allow_duplicate=True),
     Output("audit-findings", "value", allow_duplicate=True),
     Output("audit-recommendations", "value", allow_duplicate=True),
     Output("audit-score", "value", allow_duplicate=True),
     Output("audit-status", "value", allow_duplicate=True),
     Output("audit-modal", "is_open", allow_duplicate=True)],
    [Input("submit-audit", "n_clicks")],
    [State("audit-title", "value"),
     State("audit-type", "value"),
     State("audit-scope", "value"),
     State("audit-auditor", "value"),
     State("audit-findings", "value"),
     State("audit-recommendations", "value"),
     State("audit-score", "value"),
     State("audit-status", "value")],
    prevent_initial_call=True
)
def add_audit(n_clicks, title, audit_type, scope, auditor, findings, 
             recommendations, score, status):
    """Add new audit and refresh table"""
    if n_clicks and title:
        try:
            db.add_audit(title, audit_type or "Internal", scope or "", auditor or "",
                        findings or "", recommendations or "", score or 0, status or "Planned")
            
            # Refresh table
            audits_df = db.get_audits()
            table = create_data_table(audits_df, "audits-table")
            
            # Clear form and close modal
            return table, "", "Internal", "", "", "", "", 0, "Planned", False
        except Exception as e:
            print(f"Error adding audit: {e}")
    
    # Return current state
    try:
        audits_df = db.get_audits()
        table = create_data_table(audits_df, "audits-table")
        return table, "", "Internal", "", "", "", "", 0, "Planned", False
    except:
        return html.Div("Error loading audits"), "", "Internal", "", "", "", "", 0, "Planned", False

# Admin callbacks
@callback(
    Output("export-status", "children", allow_duplicate=True),
    [Input("export-btn", "n_clicks")],
    prevent_initial_call=True
)
def export_database(n_clicks):
    """Export database to Excel"""
    if n_clicks:
        try:
            export_path = f"iso42001_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            if db.export_database(export_path):
                return dbc.Alert(f"Database exported successfully to {export_path}", 
                               color="success", dismissable=True)
            else:
                return dbc.Alert("Export failed. Please try again.", 
                               color="danger", dismissable=True)
        except Exception as e:
            return dbc.Alert(f"Export error: {str(e)}", 
                           color="danger", dismissable=True)
    return ""

@callback(
    Output("import-status", "children", allow_duplicate=True),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
    prevent_initial_call=True
)
def import_database(contents, filename):
    """Import database from Excel"""
    if contents is not None:
        try:
            # Decode file contents
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Save temporary file
            temp_path = f"temp_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(temp_path, 'wb') as f:
                f.write(decoded)
            
            # Import data
            if db.import_database(temp_path):
                # Clean up temp file
                import os
                os.remove(temp_path)
                return dbc.Alert(f"Database imported successfully from {filename}", 
                               color="success", dismissable=True)
            else:
                return dbc.Alert("Import failed. Please check file format.", 
                               color="danger", dismissable=True)
        except Exception as e:
            return dbc.Alert(f"Import error: {str(e)}", 
                           color="danger", dismissable=True)
    return ""