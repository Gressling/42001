#!/usr/bin/env python3
"""
Create Example Database for ISO 42001 AI Management System
Creates a clean database with sample data for distribution
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from iso42001.database import ISO42001Database

def create_example_database(output_path: str):
    """Create a clean example database with sample data"""
    
    # Remove existing file if it exists
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Create new database
    db = ISO42001Database(output_path)
    
    print(f"Creating example database at: {output_path}")
    
    # Add sample AI assets
    sample_assets = [
        {
            'name': 'Customer Service Chatbot',
            'type': 'Conversational AI',
            'description': 'AI-powered chatbot for handling customer inquiries and support tickets',
            'risk_level': 'Medium',
            'business_unit': 'Customer Service',
            'owner': 'Sarah Johnson',
            'status': 'Active',
            'compliance_status': 'Compliant',
            'data_sources': 'Customer support tickets, FAQ database, product documentation',
            'review_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'tags': 'customer-service,chatbot,nlp'
        },
        {
            'name': 'Fraud Detection System',
            'type': 'Machine Learning',
            'description': 'ML model for detecting fraudulent transactions in real-time',
            'risk_level': 'High',
            'business_unit': 'Financial Services',
            'owner': 'Michael Chen',
            'status': 'Active',
            'compliance_status': 'Under Review',
            'data_sources': 'Transaction data, customer profiles, historical fraud cases',
            'review_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'tags': 'fraud-detection,ml,security'
        },
        {
            'name': 'Content Recommendation Engine',
            'type': 'Recommendation System',
            'description': 'AI system for personalizing content recommendations to users',
            'risk_level': 'Low',
            'business_unit': 'Marketing',
            'owner': 'Emma Rodriguez',
            'status': 'Under Review',
            'compliance_status': 'Pending',
            'data_sources': 'User behavior data, content metadata, engagement metrics',
            'review_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
            'tags': 'recommendations,personalization,marketing'
        },
        {
            'name': 'Document Processing AI',
            'type': 'Document AI',
            'description': 'Optical Character Recognition and document classification system',
            'risk_level': 'Medium',
            'business_unit': 'Operations',
            'owner': 'David Kim',
            'status': 'Under Review',
            'compliance_status': 'Compliant',
            'data_sources': 'Scanned documents, forms, contracts, invoices',
            'review_date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
            'tags': 'ocr,document-processing,automation'
        },
        {
            'name': 'Predictive Maintenance Model',
            'type': 'Predictive Analytics',
            'description': 'AI model for predicting equipment failures and maintenance needs',
            'risk_level': 'High',
            'business_unit': 'Manufacturing',
            'owner': 'Lisa Thompson',
            'status': 'Active',
            'compliance_status': 'Compliant',
            'data_sources': 'Sensor data, maintenance logs, equipment specifications',
            'review_date': (datetime.now() + timedelta(days=120)).strftime('%Y-%m-%d'),
            'tags': 'predictive-maintenance,iot,manufacturing'
        }
    ]
    
    # Add sample assets to database
    for asset in sample_assets:
        asset_id = db.add_asset(
            name=asset['name'],
            asset_type=asset['type'],
            description=asset['description'],
            criticality=asset['risk_level'],
            owner=asset['owner'],
            status=asset['status']
        )
        print(f"Created sample asset: {asset['name']} (ID: {asset_id})")
    
    # Add sample risk assessments
    sample_risks = [
        {
            'ai_asset_id': 1,  # Customer Service Chatbot
            'risk_category': 'Data Privacy',
            'risk_description': 'Potential exposure of customer personal information',
            'probability': 'Low',
            'impact': 'High',
            'risk_score': 6,
            'mitigation_strategy': 'Implement data anonymization and access controls',
            'responsible_person': 'Sarah Johnson',
            'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'Open'
        },
        {
            'ai_asset_id': 2,  # Fraud Detection System
            'risk_category': 'Model Bias',
            'risk_description': 'Risk of algorithmic bias affecting certain customer groups',
            'probability': 'Medium',
            'impact': 'High',
            'risk_score': 8,
            'mitigation_strategy': 'Regular bias testing and model retraining with diverse datasets',
            'responsible_person': 'Michael Chen',
            'due_date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'status': 'In Progress'
        },
        {
            'ai_asset_id': 5,  # Predictive Maintenance Model
            'risk_category': 'System Reliability',
            'risk_description': 'False predictions could lead to unnecessary downtime or equipment failure',
            'probability': 'Medium',
            'impact': 'High',
            'risk_score': 8,
            'mitigation_strategy': 'Implement human oversight and gradual rollout with monitoring',
            'responsible_person': 'Lisa Thompson',
            'due_date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
            'status': 'Open'
        }
    ]
    
    # Add sample risk assessments to database
    for risk in sample_risks:
        risk_id = db.add_risk(
            asset_id=risk['ai_asset_id'],
            risk_title=f"{risk['risk_category']} Risk",
            risk_description=risk['risk_description'],
            risk_category=risk['risk_category'],
            likelihood=risk['probability'],
            impact=risk['impact'],
            risk_level=risk['impact'],  # Using impact as risk level
            mitigation_strategy=risk['mitigation_strategy'],
            owner=risk['responsible_person'],
            status=risk['status']
        )
        print(f"Created sample risk assessment for asset {risk['ai_asset_id']} (ID: {risk_id})")
    
    # Add sample audit records
    sample_audits = [
        {
            'audit_title': 'ISO 42001 System Requirements Audit',
            'audit_type': 'Internal',
            'audit_scope': 'Customer Service Chatbot system requirements compliance',
            'auditor': 'Sarah Johnson',
            'findings': 'All functional and non-functional requirements documented and approved',
            'recommendations': 'Continue regular requirements review process',
            'compliance_score': 95,
            'status': 'Complete'
        },
        {
            'audit_title': 'Operational Planning & Control Review',
            'audit_type': 'Internal',
            'audit_scope': 'Fraud Detection System operational procedures',
            'auditor': 'Michael Chen',
            'findings': 'Operational procedures need updates to include bias monitoring',
            'recommendations': 'Update procedures to include regular bias testing and monitoring',
            'compliance_score': 75,
            'status': 'Follow-up Required'
        },
        {
            'audit_title': 'Risk Management Assessment',
            'audit_type': 'Internal',
            'audit_scope': 'Document Processing AI risk assessment processes',
            'auditor': 'David Kim',
            'findings': 'Risk assessment completed with appropriate mitigation measures',
            'recommendations': 'Maintain current risk assessment schedule',
            'compliance_score': 90,
            'status': 'Complete'
        }
    ]
    
    # Add sample audit records to database
    for audit in sample_audits:
        audit_id = db.add_audit(
            audit_title=audit['audit_title'],
            audit_type=audit['audit_type'],
            audit_scope=audit['audit_scope'],
            auditor=audit['auditor'],
            findings=audit['findings'],
            recommendations=audit['recommendations'],
            compliance_score=audit['compliance_score'],
            status=audit['status']
        )
        print(f"Created sample audit record: {audit['audit_title']} (ID: {audit_id})")
    
    print(f"\nExample database created successfully at: {output_path}")
    print(f"Database contains:")
    print(f"  - {len(sample_assets)} AI assets")
    print(f"  - {len(sample_risks)} risk assessments")  
    print(f"  - {len(sample_audits)} audit records")

def main():
    """Main function"""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create example database
    example_db_path = os.path.join(data_dir, 'iso42001_example.db')
    create_example_database(example_db_path)

if __name__ == '__main__':
    main()