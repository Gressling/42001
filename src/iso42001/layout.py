"""
Layout components and UI elements for the ISO 42001 Bookkeeping System
"""

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from datetime import date

from .database import ISO42001Database
from . import __version__

# Initialize the database
db = ISO42001Database()

# Version utilities
def get_version_major_minor():
    """Extract major.minor version from __version__"""
    parts = __version__.split('.')
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else __version__

# IBM Carbon-inspired color scheme
CARBON_COLORS = {
    'primary': '#0f62fe',
    'secondary': '#393939',
    'background': '#f4f4f4',
    'surface': '#ffffff',
    'text': '#161616',
    'text_secondary': '#525252',
    'success': '#198038',
    'warning': '#f1c21b',
    'danger': '#da1e28',
    'border': '#e0e0e0'
}

# Custom CSS styles
CARBON_STYLE = {
    'fontFamily': '"IBM Plex Sans", Arial, sans-serif',
    'backgroundColor': CARBON_COLORS['background'],
    'color': CARBON_COLORS['text']
}

TAB_STYLE = {
    'borderBottom': '1px solid #d0d0d0',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': CARBON_COLORS['surface']
}

TAB_SELECTED_STYLE = {
    'borderTop': '3px solid #0f62fe',
    'borderBottom': '1px solid #d0d0d0',
    'backgroundColor': CARBON_COLORS['surface'],
    'color': CARBON_COLORS['primary'],
    'padding': '6px',
    'fontWeight': 'bold'
}

def create_header():
    """Create application header"""
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("ISO 42001 Bookkeeping System", className="mb-0", 
                               style={'color': 'white', 'fontWeight': '300'}),
                        html.Small("AI Management System Compliance  ", 
                                 style={'color': '#c6c6c6'}),
                        html.Small(f"Version {get_version_major_minor()}", 
                                style={'color': '#c6c6c6', 'fontSize': '0.9em'})
                    ])
                ], width=12)
            ], align="center")
        ], fluid=True),
        color=CARBON_COLORS['secondary'],
        dark=True,
        className="mb-4"
    )

def create_stats_cards():
    """Create dashboard statistics cards"""
    stats = db.get_dashboard_stats()
    
    cards = [
        dbc.Card([
            dbc.CardBody([
                html.H4(stats['total_assets'], className="card-title", style={'color': CARBON_COLORS['primary']}),
                html.P("Total AI Assets", className="card-text")
            ])
        ], color="light", outline=True),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(stats['active_risks'], className="card-title", style={'color': CARBON_COLORS['warning']}),
                html.P("Active Risks", className="card-text")
            ])
        ], color="light", outline=True),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(stats['implemented_controls'], className="card-title", style={'color': CARBON_COLORS['success']}),
                html.P("Controls", className="card-text")
            ])
        ], color="light", outline=True),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(stats['open_incidents'], className="card-title", style={'color': CARBON_COLORS['danger']}),
                html.P("Open Incidents", className="card-text")
            ])
        ], color="light", outline=True),
        
        dbc.Card([
            dbc.CardBody([
                html.H4(stats['completed_audits'], className="card-title", style={'color': CARBON_COLORS['secondary']}),
                html.P("Completed Audits", className="card-text")
            ])
        ], color="light", outline=True)
    ]
    
    return dbc.Row([
        dbc.Col(card, width=12, md=6, lg=2, className="mb-3") for card in cards
    ])

def create_data_table(df, table_id):
    """Create a standard data table with Carbon styling"""
    if df.empty:
        return html.Div("No data available", className="text-center text-muted p-4")
    
    # Add edit column for editable tables
    columns = []
    if table_id in ["assets-table", "risks-table", "controls-table", "incidents-table", "audits-table"] and not df.empty:
        # Add edit buttons to data
        df_copy = df.copy()
        df_copy['edit'] = "Edit"  # Simple text for now, will be handled by callback
        df = df_copy
        
        # Add Edit button column at the end
        columns = [{"name": col, "id": col} for col in df.columns if col != 'edit']
        columns.append({
            "name": "Action", 
            "id": "edit"
        })
    else:
        # Add regular columns for non-editable tables
        columns = [{"name": col, "id": col} for col in df.columns]
    
    return dash_table.DataTable(
        id=table_id,
        data=df.to_dict('records'),
        columns=columns,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': CARBON_STYLE['fontFamily'],
            'border': f'1px solid {CARBON_COLORS["border"]}'
        },
        style_header={
            'backgroundColor': CARBON_COLORS['secondary'],
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'backgroundColor': CARBON_COLORS['surface'],
            'color': CARBON_COLORS['text']
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': CARBON_COLORS['background']
            }
        ],
        page_size=10,
        sort_action="native",
        filter_action="native"
    )

def create_form_input(label, input_id, input_type="text", options=None, value=""):
    """Create standardized form input"""
    if input_type == "dropdown":
        input_component = dcc.Dropdown(
            id=input_id,
            options=[{'label': opt, 'value': opt} for opt in options] if options else [],
            value=value,
            style={'marginBottom': '10px'}
        )
    elif input_type == "textarea":
        input_component = dcc.Textarea(
            id=input_id,
            value=value,
            style={'width': '100%', 'height': '100px', 'marginBottom': '10px'}
        )
    elif input_type == "date":
        input_component = dcc.DatePickerSingle(
            id=input_id,
            date=value if value else date.today(),
            style={'marginBottom': '10px'}
        )
    else:
        input_component = dbc.Input(
            id=input_id,
            type=input_type,
            value=value,
            style={'marginBottom': '10px'}
        )
    
    return dbc.Row([
        dbc.Col([
            dbc.Label(label, style={'fontWeight': 'bold', 'color': CARBON_COLORS['text']}),
            input_component
        ], width=12)
    ], className="mb-2")

def render_assets_tab():
    """Render AI Assets tab"""
    assets_df = db.get_assets()
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("AI Assets Management", style={'color': CARBON_COLORS['primary']}),
                html.P("Manage and track AI assets in your organization")
            ], width=8),
            dbc.Col([
                dbc.Button("Add New Asset", id="add-asset-btn", color="primary", className="float-end")
            ], width=4)
        ], className="mb-4"),
        
        # Add/Edit asset modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="asset-modal-title")),
            dbc.ModalBody([
                # Hidden field to store asset ID for editing
                dcc.Store(id="edit-asset-id", data=None),
                create_form_input("Asset Name", "asset-name"),
                create_form_input("Asset Type", "asset-type", "dropdown", 
                                ["ML Model", "AI System", "Dataset", "Algorithm", "AI Service"]),
                create_form_input("Description", "asset-description", "textarea"),
                create_form_input("Criticality", "asset-criticality", "dropdown",
                                ["Low", "Medium", "High", "Critical"]),
                create_form_input("Owner", "asset-owner"),
                create_form_input("Status", "asset-status", "dropdown",
                                ["Active", "Inactive", "Under Review", "Deprecated"])
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-asset", className="ms-auto", n_clicks=0),
                dbc.Button("Save Asset", id="submit-asset", color="primary", className="ms-2", n_clicks=0)
            ])
        ], id="asset-modal", is_open=False),
        
        # Assets table
        html.Div(id="assets-table-container", children=[
            create_data_table(assets_df, "assets-table")
        ])
    ])

def render_risks_tab():
    """Render Risk Management tab"""
    risks_df = db.get_risks()
    assets_df = db.get_assets()
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Risk Management", style={'color': CARBON_COLORS['primary']}),
                html.P("Identify, assess, and manage AI-related risks")
            ], width=8),
            dbc.Col([
                dbc.Button("Add New Risk", id="add-risk-btn", color="primary", className="float-end")
            ], width=4)
        ], className="mb-4"),
        
        # Add/Edit risk modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="risk-modal-title")),
            dbc.ModalBody([
                # Hidden field to store risk ID for editing
                dcc.Store(id="edit-risk-id", data=None),
                create_form_input("Associated Asset", "risk-asset", "dropdown",
                                [f"{row['id']} - {row['name']}" for _, row in assets_df.iterrows()] if not assets_df.empty else []),
                create_form_input("Risk Title", "risk-title"),
                create_form_input("Risk Description", "risk-description", "textarea"),
                create_form_input("Risk Category", "risk-category"),
                create_form_input("Likelihood", "risk-likelihood", "dropdown",
                                ["Very Low", "Low", "Medium", "High", "Very High"]),
                create_form_input("Impact", "risk-impact", "dropdown",
                                ["Very Low", "Low", "Medium", "High", "Very High"]),
                create_form_input("Risk Level", "risk-level", "dropdown",
                                ["Low", "Medium", "High", "Critical"]),
                create_form_input("Mitigation Strategy", "risk-mitigation", "textarea"),
                create_form_input("Owner", "risk-owner"),
                create_form_input("Status", "risk-status", "dropdown",
                                ["Open", "In Progress", "Mitigated", "Accepted", "Closed"])
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-risk", className="ms-auto", n_clicks=0),
                dbc.Button("Save Risk", id="submit-risk", color="primary", className="ms-2", n_clicks=0)
            ])
        ], id="risk-modal", is_open=False),
        
        # Risks table
        html.Div(id="risks-table-container", children=[
            create_data_table(risks_df, "risks-table")
        ])
    ])

def render_controls_tab():
    """Render Controls tab"""
    controls_df = db.get_controls()
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Controls Management", style={'color': CARBON_COLORS['primary']}),
                html.P("Manage implemented controls and safeguards")
            ], width=8),
            dbc.Col([
                dbc.Button("Add New Control", id="add-control-btn", color="primary", className="float-end")
            ], width=4)
        ], className="mb-4"),
        
        # Add/Edit control modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="control-modal-title")),
            dbc.ModalBody([
                # Hidden field to store control ID for editing
                dcc.Store(id="edit-control-id", data=None),
                create_form_input("Control ID", "control-id"),
                create_form_input("Control Name", "control-name"),
                create_form_input("Control Description", "control-description", "textarea"),
                create_form_input("Control Type", "control-type", "dropdown",
                                ["Preventive", "Detective", "Corrective", "Administrative"]),
                create_form_input("Implementation Status", "control-implementation", "dropdown",
                                ["Not Started", "In Progress", "Implemented", "Needs Review"]),
                create_form_input("Effectiveness", "control-effectiveness", "dropdown",
                                ["Not Assessed", "Ineffective", "Partially Effective", "Effective"]),
                create_form_input("Owner", "control-owner")
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-control", className="ms-auto", n_clicks=0),
                dbc.Button("Save Control", id="submit-control", color="primary", className="ms-2", n_clicks=0)
            ])
        ], id="control-modal", is_open=False),
        
        # Controls table
        html.Div(id="controls-table-container", children=[
            create_data_table(controls_df, "controls-table")
        ])
    ])

def render_incidents_tab():
    """Render Incidents tab"""
    incidents_df = db.get_incidents()
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Incident Management", style={'color': CARBON_COLORS['primary']}),
                html.P("Track and manage AI-related incidents")
            ], width=8),
            dbc.Col([
                dbc.Button("Add New Incident", id="add-incident-btn", color="primary", className="float-end")
            ], width=4)
        ], className="mb-4"),
        
        # Add/Edit incident modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="incident-modal-title")),
            dbc.ModalBody([
                # Hidden field to store incident ID for editing
                dcc.Store(id="edit-incident-id", data=None),
                create_form_input("Incident Title", "incident-title"),
                create_form_input("Incident Description", "incident-description", "textarea"),
                create_form_input("Severity", "incident-severity", "dropdown",
                                ["Low", "Medium", "High", "Critical"]),
                create_form_input("Affected Assets", "incident-assets"),
                create_form_input("Root Cause", "incident-root-cause", "textarea"),
                create_form_input("Corrective Actions", "incident-actions", "textarea"),
                create_form_input("Status", "incident-status", "dropdown",
                                ["Open", "Investigating", "Resolved", "Closed"]),
                create_form_input("Reported By", "incident-reported-by"),
                create_form_input("Assigned To", "incident-assigned-to")
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-incident", className="ms-auto", n_clicks=0),
                dbc.Button("Save Incident", id="submit-incident", color="primary", className="ms-2", n_clicks=0)
            ])
        ], id="incident-modal", is_open=False),
        
        # Incidents table
        html.Div(id="incidents-table-container", children=[
            create_data_table(incidents_df, "incidents-table")
        ])
    ])

def render_compliance_tab():
    """Render Compliance/Audits tab"""
    audits_df = db.get_audits()
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Compliance & Audits", style={'color': CARBON_COLORS['primary']}),
                html.P("Track compliance assessments and audit activities")
            ], width=8),
            dbc.Col([
                dbc.Button("Add New Audit", id="add-audit-btn", color="primary", className="float-end")
            ], width=4)
        ], className="mb-4"),
        
        # Add/Edit audit modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="audit-modal-title")),
            dbc.ModalBody([
                # Hidden field to store audit ID for editing
                dcc.Store(id="edit-audit-id", data=None),
                create_form_input("Audit Title", "audit-title"),
                create_form_input("Audit Type", "audit-type", "dropdown",
                                ["Internal", "External", "Self Assessment"]),
                create_form_input("Audit Scope", "audit-scope", "textarea"),
                create_form_input("Auditor", "audit-auditor"),
                create_form_input("Findings", "audit-findings", "textarea"),
                create_form_input("Recommendations", "audit-recommendations", "textarea"),
                create_form_input("Compliance Score (0-100)", "audit-score", "number"),
                create_form_input("Status", "audit-status", "dropdown",
                                ["Planned", "In Progress", "Complete", "Follow-up Required"])
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-audit", className="ms-auto", n_clicks=0),
                dbc.Button("Save Audit", id="submit-audit", color="primary", className="ms-2", n_clicks=0)
            ])
        ], id="audit-modal", is_open=False),
        
        # Audits table
        html.Div(id="audits-table-container", children=[
            create_data_table(audits_df, "audits-table")
        ])
    ])

def render_admin_tab():
    """Render Administration tab"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4("Administration", style={'color': CARBON_COLORS['primary']}),
                html.P("Database management and system administration")
            ])
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Database Export"),
                    dbc.CardBody([
                        html.P("Export all data to Excel file for backup or analysis"),
                        dbc.Button("Export Database", id="export-btn", color="success", className="me-2"),
                        html.Div(id="export-status", className="mt-2")
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Database Import"),
                    dbc.CardBody([
                        html.P("Import data from Excel file (WARNING: This will replace existing data)"),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=False
                        ),
                        html.Div(id="import-status", className="mt-2")
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Copyright and License Information
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("About & Legal Information"),
                    dbc.CardBody([
                        html.H6(f"ISO 42001 Bookkeeping System v{get_version_major_minor()}", className="mb-3", style={'fontWeight': 'bold'}),
                        
                        html.P([
                            "Copyright © 2025 ",
                            html.Strong("Gressling Consulting GmbH"), " (E.U.) & ",
                            html.Strong("Paramus Transform LLC"), " (U.S.)"
                        ], className="mb-2"),
                        
                        html.P([
                            "Licensed under ",
                            html.A("Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)", 
                                  href="https://creativecommons.org/licenses/by-nc-sa/4.0/", 
                                  target="_blank", 
                                  style={'color': CARBON_COLORS['primary']}),
                            html.Br(),
                            html.Img(src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png", 
                                    alt="CC BY-NC-SA 4.0", 
                                    style={'marginTop': '8px'})
                        ], className="mb-3"),
                        
                        html.Hr(),
                        
                        html.P([
                            html.Strong("Support & Contact:"), html.Br(),
                            "For technical support and inquiries: ",
                            html.A("support@paramus.ai", 
                                  href="mailto:support@paramus.ai", 
                                  style={'color': CARBON_COLORS['primary']})
                        ], className="mb-2"),
                        
                        html.P([
                            html.Strong("Version:"), " 1.0.0", html.Br(),
                            html.Strong("Last Updated:"), " 2025-10-31 10:31"
                        ], className="mb-0", style={'fontSize': '0.9em', 'color': CARBON_COLORS['text_secondary']})
                    ])
                ])
            ], width=12)
        ])
    ])

def create_app_layout():
    """Create the main application layout"""
    return dbc.Container([
        create_header(),
        
        # Statistics cards
        create_stats_cards(),
        
        # Main tabs
        dcc.Tabs(id="main-tabs", value="assets", children=[
            dcc.Tab(label="Assets", value="assets", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Risk Management", value="risks", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Controls", value="controls", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Incidents", value="incidents", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Compliance", value="compliance", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Administration", value="admin", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        ]),
        
        # Tab content
        html.Div(id="tab-content", className="mt-4"),
        
        # Hidden placeholder components for callback compatibility
        # These prevent "ID not found in layout" errors when callbacks are registered
        html.Div([
            # Asset placeholders
            html.Div(id="assets-table-container", style={'display': 'none'}),
            dbc.Input(id="asset-name", style={'display': 'none'}),
            dbc.Input(id="asset-type", style={'display': 'none'}),
            dbc.Input(id="asset-description", style={'display': 'none'}),
            dbc.Input(id="asset-criticality", style={'display': 'none'}),
            dbc.Input(id="asset-owner", style={'display': 'none'}),
            dbc.Input(id="asset-status", style={'display': 'none'}),
            dbc.Modal(id="asset-modal", is_open=False, style={'display': 'none'}),
            dbc.Button(id="add-asset-btn", style={'display': 'none'}),
            dbc.Button(id="submit-asset", style={'display': 'none'}),
            dbc.Button(id="cancel-asset", style={'display': 'none'}),
            dcc.Store(id="edit-asset-id"),
            html.H4(id="asset-modal-title", style={'display': 'none'}),
            
            # Risk placeholders
            html.Div(id="risks-table-container", style={'display': 'none'}),
            dbc.Input(id="risk-asset", style={'display': 'none'}),
            dbc.Input(id="risk-title", style={'display': 'none'}),
            dbc.Input(id="risk-description", style={'display': 'none'}),
            dbc.Input(id="risk-category", style={'display': 'none'}),
            dbc.Input(id="risk-likelihood", style={'display': 'none'}),
            dbc.Input(id="risk-impact", style={'display': 'none'}),
            dbc.Input(id="risk-level", style={'display': 'none'}),
            dbc.Input(id="risk-mitigation", style={'display': 'none'}),
            dbc.Input(id="risk-owner", style={'display': 'none'}),
            dbc.Input(id="risk-status", style={'display': 'none'}),
            dbc.Modal(id="risk-modal", is_open=False, style={'display': 'none'}),
            dbc.Button(id="add-risk-btn", style={'display': 'none'}),
            dbc.Button(id="submit-risk", style={'display': 'none'}),
            dbc.Button(id="cancel-risk", style={'display': 'none'}),
            dcc.Store(id="edit-risk-id"),
            html.H4(id="risk-modal-title", style={'display': 'none'}),
            
            # Control placeholders
            html.Div(id="controls-table-container", style={'display': 'none'}),
            dbc.Input(id="control-id", style={'display': 'none'}),
            dbc.Input(id="control-name", style={'display': 'none'}),
            dbc.Input(id="control-description", style={'display': 'none'}),
            dbc.Input(id="control-type", style={'display': 'none'}),
            dbc.Input(id="control-implementation", style={'display': 'none'}),
            dbc.Input(id="control-effectiveness", style={'display': 'none'}),
            dbc.Input(id="control-owner", style={'display': 'none'}),
            dbc.Modal(id="control-modal", is_open=False, style={'display': 'none'}),
            dbc.Button(id="add-control-btn", style={'display': 'none'}),
            dbc.Button(id="submit-control", style={'display': 'none'}),
            dbc.Button(id="cancel-control", style={'display': 'none'}),
            dcc.Store(id="edit-control-id"),
            html.H4(id="control-modal-title", style={'display': 'none'}),
            
            # Incident placeholders
            html.Div(id="incidents-table-container", style={'display': 'none'}),
            dbc.Input(id="incident-title", style={'display': 'none'}),
            dbc.Input(id="incident-description", style={'display': 'none'}),
            dbc.Input(id="incident-severity", style={'display': 'none'}),
            dbc.Input(id="incident-assets", style={'display': 'none'}),
            dbc.Input(id="incident-root-cause", style={'display': 'none'}),
            dbc.Input(id="incident-actions", style={'display': 'none'}),
            dbc.Input(id="incident-status", style={'display': 'none'}),
            dbc.Input(id="incident-reported-by", style={'display': 'none'}),
            dbc.Input(id="incident-assigned-to", style={'display': 'none'}),
            dbc.Modal(id="incident-modal", is_open=False, style={'display': 'none'}),
            dbc.Button(id="add-incident-btn", style={'display': 'none'}),
            dbc.Button(id="submit-incident", style={'display': 'none'}),
            dbc.Button(id="cancel-incident", style={'display': 'none'}),
            dcc.Store(id="edit-incident-id"),
            html.H4(id="incident-modal-title", style={'display': 'none'}),
            
            # Audit placeholders
            html.Div(id="audits-table-container", style={'display': 'none'}),
            dbc.Input(id="audit-title", style={'display': 'none'}),
            dbc.Input(id="audit-type", style={'display': 'none'}),
            dbc.Input(id="audit-scope", style={'display': 'none'}),
            dbc.Input(id="audit-auditor", style={'display': 'none'}),
            dbc.Input(id="audit-findings", style={'display': 'none'}),
            dbc.Input(id="audit-recommendations", style={'display': 'none'}),
            dbc.Input(id="audit-score", style={'display': 'none'}),
            dbc.Input(id="audit-status", style={'display': 'none'}),
            dbc.Modal(id="audit-modal", is_open=False, style={'display': 'none'}),
            dbc.Button(id="add-audit-btn", style={'display': 'none'}),
            dbc.Button(id="submit-audit", style={'display': 'none'}),
            dbc.Button(id="cancel-audit", style={'display': 'none'}),
            dcc.Store(id="edit-audit-id"),
            html.H4(id="audit-modal-title", style={'display': 'none'}),
            
            # Admin placeholders
            html.Div(id="export-status", style={'display': 'none'}),
            html.Div(id="import-status", style={'display': 'none'}),
            dbc.Button(id="export-btn", style={'display': 'none'}),
            dcc.Upload(id="upload-data", style={'display': 'none'})
        ], style={'display': 'none'}),
        
        # Interval component for auto-refresh
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        )
    ], fluid=True, style=CARBON_STYLE)