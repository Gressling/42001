import sqlite3
import pandas as pd
from datetime import datetime
import json
from typing import List, Dict, Optional, Any, Union

class ISO42001Database:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = self._get_default_db_path()
        self.db_path = db_path
        self.init_database()
    
    def _get_default_db_path(self) -> str:
        """Get the default database path, handling PyInstaller bundles"""
        import os
        import sys
        
        # Check if running in PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle - use current working directory
            app_dir = os.getcwd()
            db_path = os.path.join(app_dir, "iso42001.db")
        else:
            # Running normally - use data directory relative to package root
            package_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            data_dir = os.path.join(package_root, "data")
            
            # Create data directory if it doesn't exist
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "iso42001.db")
        
        return db_path
    
    def get_connection(self):
        """Get database connection with foreign key support"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init_database(self):
        """Initialize the database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # AI Assets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                criticality TEXT CHECK(criticality IN ('Low', 'Medium', 'High', 'Critical')),
                owner TEXT,
                status TEXT CHECK(status IN ('Active', 'Inactive', 'Under Review', 'Deprecated')),
                last_reviewed DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Risk Management table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER,
                risk_title TEXT NOT NULL,
                risk_description TEXT,
                risk_category TEXT,
                likelihood TEXT CHECK(likelihood IN ('Very Low', 'Low', 'Medium', 'High', 'Very High')),
                impact TEXT CHECK(impact IN ('Very Low', 'Low', 'Medium', 'High', 'Very High')),
                risk_level TEXT CHECK(risk_level IN ('Low', 'Medium', 'High', 'Critical')),
                mitigation_strategy TEXT,
                owner TEXT,
                status TEXT CHECK(status IN ('Open', 'In Progress', 'Mitigated', 'Accepted', 'Closed')),
                review_date DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES ai_assets (id)
            )
        ''')
        
        # Controls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS controls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_id TEXT UNIQUE NOT NULL,
                control_name TEXT NOT NULL,
                control_description TEXT,
                control_type TEXT CHECK(control_type IN ('Preventive', 'Detective', 'Corrective', 'Administrative')),
                implementation_status TEXT CHECK(implementation_status IN ('Not Started', 'In Progress', 'Implemented', 'Needs Review')),
                effectiveness TEXT CHECK(effectiveness IN ('Not Assessed', 'Ineffective', 'Partially Effective', 'Effective')),
                owner TEXT,
                last_tested DATE,
                next_review DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Risk-Control mapping table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_controls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                risk_id INTEGER,
                control_id INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (risk_id) REFERENCES risks (id),
                FOREIGN KEY (control_id) REFERENCES controls (id)
            )
        ''')
        
        # Incidents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_title TEXT NOT NULL,
                incident_description TEXT,
                severity TEXT CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')),
                affected_assets TEXT,
                root_cause TEXT,
                corrective_actions TEXT,
                status TEXT CHECK(status IN ('Open', 'Investigating', 'Resolved', 'Closed')),
                reported_by TEXT,
                assigned_to TEXT,
                incident_date DATE,
                resolution_date DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Compliance Audits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_title TEXT NOT NULL,
                audit_type TEXT CHECK(audit_type IN ('Internal', 'External', 'Self Assessment')),
                audit_scope TEXT,
                auditor TEXT,
                audit_date DATE,
                findings TEXT,
                recommendations TEXT,
                compliance_score INTEGER CHECK(compliance_score BETWEEN 0 AND 100),
                status TEXT CHECK(status IN ('Planned', 'In Progress', 'Complete', 'Follow-up Required')),
                next_audit_date DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Assets CRUD operations
    def add_asset(self, name: str, asset_type: str, description: str = "", 
                  criticality: str = "Medium", owner: str = "", status: str = "Active") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ai_assets (name, type, description, criticality, owner, status, last_reviewed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, asset_type, description, criticality, owner, status, datetime.now().date()))
        asset_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return asset_id
    
    def get_assets(self) -> pd.DataFrame:
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM ai_assets ORDER BY created_date DESC", conn)
        conn.close()
        return df
    
    def update_asset(self, asset_id: int, **kwargs) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'type', 'description', 'criticality', 'owner', 'status']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_date = ?")
            values.append(datetime.now())
            values.append(asset_id)
            
            query = f"UPDATE ai_assets SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_asset(self, asset_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ai_assets WHERE id = ?", (asset_id,))
        conn.commit()
        conn.close()
        return True
    
    # Risk CRUD operations
    def add_risk(self, asset_id: Optional[int], risk_title: str, risk_description: str = "",
                 risk_category: str = "", likelihood: str = "Medium", impact: str = "Medium",
                 risk_level: str = "Medium", mitigation_strategy: str = "", owner: str = "", 
                 status: str = "Open") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO risks (asset_id, risk_title, risk_description, risk_category, 
                             likelihood, impact, risk_level, mitigation_strategy, owner, status, review_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (asset_id, risk_title, risk_description, risk_category, likelihood, impact, 
              risk_level, mitigation_strategy, owner, status, datetime.now().date()))
        risk_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return risk_id
    
    def get_risks(self) -> pd.DataFrame:
        conn = self.get_connection()
        query = '''
            SELECT r.*, a.name as asset_name 
            FROM risks r 
            LEFT JOIN ai_assets a ON r.asset_id = a.id 
            ORDER BY r.created_date DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def update_risk(self, risk_id: int, **kwargs) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['asset_id', 'risk_title', 'risk_description', 'risk_category', 
                      'likelihood', 'impact', 'risk_level', 'mitigation_strategy', 'owner', 'status']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_date = ?")
            values.append(datetime.now())
            values.append(risk_id)
            
            query = f"UPDATE risks SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_risk(self, risk_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM risks WHERE id = ?", (risk_id,))
        conn.commit()
        conn.close()
        return True
    
    # Control CRUD operations
    def add_control(self, control_id: str, control_name: str, control_description: str = "",
                   control_type: str = "Preventive", implementation_status: str = "Not Started",
                   effectiveness: str = "Not Assessed", owner: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO controls (control_id, control_name, control_description, control_type,
                                implementation_status, effectiveness, owner, next_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (control_id, control_name, control_description, control_type, 
              implementation_status, effectiveness, owner, datetime.now().date()))
        db_control_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return db_control_id
    
    def get_controls(self) -> pd.DataFrame:
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM controls ORDER BY created_date DESC", conn)
        conn.close()
        return df
    
    def update_control(self, control_db_id: int, **kwargs) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['control_id', 'control_name', 'control_description', 'control_type', 
                      'implementation_status', 'effectiveness', 'owner']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_date = ?")
            values.append(datetime.now())
            values.append(control_db_id)
            
            query = f"UPDATE controls SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_control(self, control_db_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM controls WHERE id = ?", (control_db_id,))
        conn.commit()
        conn.close()
        return True
    
    # Incident CRUD operations
    def add_incident(self, incident_title: str, incident_description: str = "", 
                    severity: str = "Medium", affected_assets: str = "", root_cause: str = "",
                    corrective_actions: str = "", status: str = "Open", reported_by: str = "",
                    assigned_to: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO incidents (incident_title, incident_description, severity, 
                                 affected_assets, root_cause, corrective_actions, status,
                                 reported_by, assigned_to, incident_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (incident_title, incident_description, severity, affected_assets, root_cause,
              corrective_actions, status, reported_by, assigned_to, datetime.now().date()))
        incident_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return incident_id
    
    def get_incidents(self) -> pd.DataFrame:
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM incidents ORDER BY created_date DESC", conn)
        conn.close()
        return df
    
    def update_incident(self, incident_id: int, **kwargs) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['incident_title', 'incident_description', 'severity', 'affected_assets', 
                      'root_cause', 'corrective_actions', 'status', 'reported_by', 'assigned_to']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_date = ?")
            values.append(datetime.now())
            values.append(incident_id)
            
            query = f"UPDATE incidents SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_incident(self, incident_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        conn.commit()
        conn.close()
        return True
    
    # Audit CRUD operations
    def add_audit(self, audit_title: str, audit_type: str = "Internal", audit_scope: str = "",
                 auditor: str = "", findings: str = "", recommendations: str = "",
                 compliance_score: int = 0, status: str = "Planned") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audits (audit_title, audit_type, audit_scope, auditor, 
                              findings, recommendations, compliance_score, status, audit_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (audit_title, audit_type, audit_scope, auditor, findings, recommendations,
              compliance_score, status, datetime.now().date()))
        audit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return audit_id
    
    def get_audits(self) -> pd.DataFrame:
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM audits ORDER BY created_date DESC", conn)
        conn.close()
        return df
    
    def update_audit(self, audit_id: int, **kwargs) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['audit_title', 'audit_type', 'audit_scope', 'auditor', 
                      'findings', 'recommendations', 'compliance_score', 'status']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_date = ?")
            values.append(datetime.now())
            values.append(audit_id)
            
            query = f"UPDATE audits SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_audit(self, audit_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM audits WHERE id = ?", (audit_id,))
        conn.commit()
        conn.close()
        return True
    
    # Database export/import functions
    def export_database(self, export_path: str) -> bool:
        """Export all database tables to Excel file"""
        try:
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                # Export each table to a separate sheet
                self.get_assets().to_excel(writer, sheet_name='Assets', index=False)
                self.get_risks().to_excel(writer, sheet_name='Risks', index=False)
                self.get_controls().to_excel(writer, sheet_name='Controls', index=False)
                self.get_incidents().to_excel(writer, sheet_name='Incidents', index=False)
                self.get_audits().to_excel(writer, sheet_name='Audits', index=False)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def import_database(self, import_path: str) -> bool:
        """Import data from Excel file - WARNING: This will replace existing data"""
        try:
            conn = self.get_connection()
            
            # Clear existing data
            cursor = conn.cursor()
            tables = ['ai_assets', 'risks', 'controls', 'incidents', 'audits']
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
            
            # Import data from Excel
            excel_file = pd.ExcelFile(import_path)
            
            if 'Assets' in excel_file.sheet_names:
                assets_df = pd.read_excel(import_path, sheet_name='Assets')
                assets_df.to_sql('ai_assets', conn, if_exists='append', index=False)
            
            if 'Risks' in excel_file.sheet_names:
                risks_df = pd.read_excel(import_path, sheet_name='Risks')
                # Remove asset_name column if it exists (it's a joined column)
                if 'asset_name' in risks_df.columns:
                    risks_df = risks_df.drop('asset_name', axis=1)
                risks_df.to_sql('risks', conn, if_exists='append', index=False)
            
            if 'Controls' in excel_file.sheet_names:
                controls_df = pd.read_excel(import_path, sheet_name='Controls')
                controls_df.to_sql('controls', conn, if_exists='append', index=False)
            
            if 'Incidents' in excel_file.sheet_names:
                incidents_df = pd.read_excel(import_path, sheet_name='Incidents')
                incidents_df.to_sql('incidents', conn, if_exists='append', index=False)
            
            if 'Audits' in excel_file.sheet_names:
                audits_df = pd.read_excel(import_path, sheet_name='Audits')
                audits_df.to_sql('audits', conn, if_exists='append', index=False)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get summary statistics for dashboard"""
        conn = self.get_connection()
        
        stats = {}
        stats['total_assets'] = pd.read_sql_query("SELECT COUNT(*) as count FROM ai_assets", conn).iloc[0]['count']
        stats['active_risks'] = pd.read_sql_query("SELECT COUNT(*) as count FROM risks WHERE status != 'Closed'", conn).iloc[0]['count']
        stats['implemented_controls'] = pd.read_sql_query("SELECT COUNT(*) as count FROM controls WHERE implementation_status = 'Implemented'", conn).iloc[0]['count']
        stats['open_incidents'] = pd.read_sql_query("SELECT COUNT(*) as count FROM incidents WHERE status IN ('Open', 'Investigating')", conn).iloc[0]['count']
        stats['completed_audits'] = pd.read_sql_query("SELECT COUNT(*) as count FROM audits WHERE status = 'Complete'", conn).iloc[0]['count']
        
        conn.close()
        return stats