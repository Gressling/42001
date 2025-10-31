#!/usr/bin/env python3
"""
Sample data generator for ISO 42001 application
This script adds sample data to test all functionality
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

# Import only database module to avoid starting dash server
from iso42001.database import ISO42001Database
from datetime import datetime, date, timedelta

def create_sample_data():
    """Create sample data for SME chemical company with AI applications"""
    db = ISO42001Database()
    
    print("Creating sample data for SME Chemical Company ISO 42001 application...")
    
    # Sample AI Assets for Chemical Company
    assets = [
        # R&D AI Applications
        ("ChemSynth AI", "ML Model", "AI system for predicting optimal chemical synthesis pathways and reaction conditions", "Critical", "Dr. Sarah Chen", "Active"),
        ("MolGen Discovery Platform", "AI System", "Molecular generation and optimization platform for new compound discovery", "Critical", "Dr. Michael Rodriguez", "Active"),
        ("Distillation Predictive Maintenance", "ML Model", "Predictive maintenance system for distillation column equipment using sensor data", "High", "Mark Thompson", "Active"),
        ("Reactor Optimization AI", "AI System", "AI-driven optimization of chemical reactor conditions for maximum yield", "High", "Dr. Lisa Wang", "Active"),
        ("Quality Control Vision System", "AI Service", "Computer vision system for automated quality inspection of chemical products", "High", "James Miller", "Active"),
        
        # Standard Business Process AI
        ("Supply Chain Optimizer", "AI System", "AI system for optimizing chemical supply chain and inventory management", "Medium", "Anna Johnson", "Active"),
        ("Customer Demand Forecasting", "ML Model", "Machine learning model for predicting customer demand for chemical products", "Medium", "Robert Wilson", "Active"),
        ("Invoice Processing AI", "AI Service", "Automated invoice processing and accounts payable system", "Medium", "Finance Team", "Active"),
        ("Safety Document Analyzer", "AI System", "NLP system for analyzing safety data sheets and regulatory compliance documents", "High", "Safety Team", "Under Review"),
        ("HR Resume Screening", "ML Model", "AI system for initial screening of job applications and resumes", "Low", "HR Department", "Active"),
        
        # Data Assets
        ("Chemical Reaction Database", "Dataset", "Historical chemical reaction data used for training synthesis prediction models", "Critical", "Data Science Team", "Active"),
        ("Equipment Sensor Data", "Dataset", "IoT sensor data from distillation columns and reactors for predictive maintenance", "High", "Operations Team", "Active"),
        ("Customer Transaction History", "Dataset", "Historical sales and transaction data for demand forecasting", "Medium", "Sales Analytics", "Active"),
        ("Regulatory Documents Database", "Dataset", "Collection of safety data sheets, regulations, and compliance documents", "High", "Compliance Team", "Active"),
        ("Product Quality Measurements", "Dataset", "Historical quality control measurements and test results", "Medium", "QC Lab", "Active")
    ]
    
    asset_ids = []
    for name, asset_type, desc, criticality, owner, status in assets:
        asset_id = db.add_asset(name, asset_type, desc, criticality, owner, status)
        asset_ids.append(asset_id)
        print(f"✓ Added asset: {name}")
    
    # Sample Risks for Chemical Company
    risks = [
        (asset_ids[0], "Synthesis Prediction Errors", "AI system may recommend dangerous or inefficient chemical synthesis pathways", "Safety & Performance", "Medium", "Very High", "Critical", "Implement safety validation layers and expert review processes", "Dr. Sarah Chen", "Open"),
        (asset_ids[2], "Predictive Maintenance False Alarms", "False positive maintenance predictions could lead to unnecessary downtime and costs", "Operational Efficiency", "High", "Medium", "High", "Tune model sensitivity and implement cost-benefit analysis", "Mark Thompson", "In Progress"),
        (asset_ids[1], "Intellectual Property Exposure", "Molecular discovery AI could inadvertently expose proprietary research data", "IP Protection", "Low", "Very High", "Critical", "Implement data encryption and access controls for training data", "Dr. Michael Rodriguez", "Open"),
        (asset_ids[3], "Reactor Optimization Safety", "AI-driven reactor optimization could recommend unsafe operating conditions", "Process Safety", "Medium", "Very High", "Critical", "Implement safety constraint validation and emergency shutdown protocols", "Dr. Lisa Wang", "Mitigated"),
        (asset_ids[10], "Chemical Data Contamination", "Training data may contain incorrect or outdated chemical reaction information", "Data Quality", "High", "High", "High", "Implement data validation and chemical expert review processes", "Data Science Team", "Open"),
        (asset_ids[5], "Supply Chain AI Bias", "AI system may exhibit bias towards certain suppliers or geographical regions", "Business Ethics", "Medium", "Medium", "Medium", "Implement fairness metrics and diverse supplier representation", "Anna Johnson", "Accepted"),
        (asset_ids[8], "Regulatory Compliance Gaps", "AI document analyzer may miss critical safety or regulatory requirements", "Compliance Risk", "Medium", "Very High", "Critical", "Implement human oversight and regular regulatory update training", "Safety Team", "Open"),
        (None, "Model Interpretability", "Critical AI systems lack explainability for regulatory compliance", "Regulatory Compliance", "High", "High", "High", "Implement explainable AI frameworks for critical systems", "CTO Office", "In Progress"),
        (asset_ids[6], "Demand Forecasting Drift", "Customer demand prediction model performance degrading due to market changes", "Business Performance", "High", "Medium", "Medium", "Implement continuous model monitoring and retraining schedule", "Robert Wilson", "Closed"),
        (asset_ids[4], "Quality Control System Failure", "Vision system failure could allow defective products to reach customers", "Product Quality", "Low", "Very High", "Critical", "Implement redundant quality checks and human oversight", "James Miller", "Mitigated")
    ]
    
    for asset_id, title, desc, category, likelihood, impact, level, mitigation, owner, status in risks:
        db.add_risk(asset_id, title, desc, category, likelihood, impact, level, mitigation, owner, status)
        print(f"✓ Added risk: {title}")
    
    # Sample Controls for Chemical Company
    controls = [
        ("CHM-001", "Chemical AI Safety Review Board", "Cross-functional review board for AI systems in chemical processes", "Administrative", "Implemented", "Effective", "Chief Technology Officer"),
        ("CHM-002", "Synthesis AI Validation Protocol", "Multi-stage validation of AI synthesis recommendations by chemical experts", "Preventive", "Implemented", "Effective", "Dr. Sarah Chen"),
        ("CHM-003", "Predictive Maintenance Calibration", "Regular calibration and validation of predictive maintenance models", "Preventive", "Implemented", "Partially Effective", "Mark Thompson"),
        ("CHM-004", "Process Safety Constraints", "Hard-coded safety limits in AI reactor optimization systems", "Preventive", "Implemented", "Effective", "Safety Engineering"),
        ("CHM-005", "Chemical Data Validation", "Automated and manual validation of chemical training data quality", "Preventive", "In Progress", "Partially Effective", "Data Science Team"),
        ("CHM-006", "AI Model Performance Monitoring", "Continuous monitoring of AI model accuracy and drift detection", "Detective", "Implemented", "Effective", "ML Operations Team"),
        ("CHM-007", "Regulatory Compliance Tracking", "System to track AI compliance with chemical industry regulations", "Administrative", "In Progress", "Not Assessed", "Compliance Team"),
        ("CHM-008", "IP Protection for AI Training", "Controls to protect proprietary chemical data in AI training", "Preventive", "Implemented", "Effective", "Legal & IT Security"),
        ("CHM-009", "Human Oversight Requirements", "Mandatory human review for critical AI decisions in production", "Administrative", "Implemented", "Effective", "Operations Management"),
        ("CHM-010", "AI Incident Response Plan", "Specific procedures for AI-related incidents in chemical operations", "Corrective", "Implemented", "Partially Effective", "Crisis Management Team"),
        ("CHM-011", "Model Explainability Framework", "Implementation of explainable AI for regulatory compliance", "Preventive", "In Progress", "Not Assessed", "AI Research Team"),
        ("CHM-012", "Third-Party AI Vendor Assessment", "Due diligence process for external AI service providers", "Preventive", "Not Started", "Not Assessed", "Procurement Team")
    ]
    
    for control_id, name, desc, control_type, status, effectiveness, owner in controls:
        db.add_control(control_id, name, desc, control_type, status, effectiveness, owner)
        print(f"✓ Added control: {name}")
    
    # Sample Incidents for Chemical Company
    incidents = [
        ("Synthesis AI Unsafe Recommendation", "ChemSynth AI recommended reaction conditions that could lead to hazardous byproducts", "Critical", "ChemSynth AI", "Training data contained incomplete safety information for rare reaction types", "Immediate model shutdown, safety review, and enhanced training data validation", "Resolved", "Lab Safety Officer", "Dr. Sarah Chen"),
        ("Distillation Column False Alarm", "Predictive maintenance system triggered unnecessary emergency shutdown", "High", "Distillation Predictive Maintenance", "Sensor calibration drift causing false positive predictions", "Recalibrated sensors and adjusted model sensitivity thresholds", "Resolved", "Operations Manager", "Mark Thompson"),
        ("Quality Control System Malfunction", "Vision system failed to detect contamination in batch #2024-0847", "Critical", "Quality Control Vision System", "Lighting changes in production area affected image recognition accuracy", "Enhanced lighting controls and model retraining with varied lighting conditions", "Investigating", "QC Supervisor", "James Miller"),
        ("Customer Data Exposure in Forecasting", "Demand forecasting system inadvertently logged customer-specific pricing data", "Medium", "Customer Demand Forecasting", "Insufficient data masking in logging configuration", "Implemented enhanced data anonymization and audit log review", "Resolved", "Data Privacy Officer", "Robert Wilson"),
        ("Molecular IP Potential Breach", "External researcher gained unauthorized access to molecular discovery training data", "High", "MolGen Discovery Platform", "Weak authentication controls for research collaboration system", "Strengthened access controls and implemented additional data encryption", "Closed", "IT Security Team", "Dr. Michael Rodriguez"),
        ("Reactor Optimization Efficiency Drop", "AI reactor optimization system performance degraded by 15% over 3 months", "Medium", "Reactor Optimization AI", "Model drift due to seasonal changes in raw material properties", "Implemented seasonal model retraining and performance monitoring dashboard", "Closed", "Process Engineer", "Dr. Lisa Wang"),
        ("Invoice Processing Error Cascade", "AI invoice system misclassified 200+ chemical supplier invoices", "Medium", "Invoice Processing AI", "Training data lacked sufficient examples of specialty chemical supplier formats", "Enhanced training data and implemented human review for unusual invoice formats", "Resolved", "Accounts Payable Manager", "Finance Team")
    ]
    
    for title, desc, severity, assets, root_cause, actions, status, reported_by, assigned_to in incidents:
        db.add_incident(title, desc, severity, assets, root_cause, actions, status, reported_by, assigned_to)
        print(f"✓ Added incident: {title}")
    
    # Sample Audits for Chemical Company
    audits = [
        ("Q3 2024 Chemical AI Safety Audit", "Internal", "Comprehensive safety review of AI systems in chemical processes", "Process Safety Team", "Found adequate safety controls for most systems, identified gaps in molecular discovery oversight", "Implement enhanced oversight for R&D AI systems and emergency response procedures", 78, "Complete"),
        ("ISO 42001 Pre-Certification Assessment", "External", "Third-party pre-certification audit for ISO 42001 compliance", "ChemTech Auditors Ltd.", "Strong technical controls identified, documentation needs improvement for traceability", "Enhance AI system documentation and implement change management processes", 84, "Complete"),
        ("FDA AI Readiness Review", "External", "Regulatory review of AI systems affecting pharmaceutical-grade chemical production", "FDA Inspection Team", "AI systems meet current regulatory expectations, recommend enhanced validation documentation", "Implement enhanced validation protocols for pharmaceutical applications", 89, "Complete"),
        ("Chemical Industry AI Ethics Assessment", "Self Assessment", "Evaluation of AI ethics practices specific to chemical industry applications", "Ethics Committee", "Good practices for data protection, need better fairness evaluation for supplier selection AI", "Implement supplier fairness metrics and bias testing protocols", 72, "Follow-up Required"),
        ("Predictive Maintenance AI Audit", "Internal", "Focused audit of predictive maintenance AI systems and their impact on operations", "Operations Audit Team", "Systems performing well, recommend enhanced documentation for maintenance decisions", "Create detailed decision audit trails and improve technician training", 81, "Complete"),
        ("AI Vendor Risk Assessment", "Internal", "Review of third-party AI service providers and data sharing agreements", "Procurement & Legal", "Most vendors meet requirements, two need enhanced data protection agreements", "Renegotiate contracts with identified vendors and implement ongoing monitoring", 76, "In Progress"),
        ("Q1 2025 Comprehensive AI Review", "Internal", "Annual comprehensive review of all AI systems and ISO 42001 compliance", "Internal Audit Team", "Scheduled for January 2025", "Complete full system inventory and compliance gap analysis", 0, "Planned"),
        ("R&D AI Intellectual Property Audit", "Internal", "Review of IP protection measures for AI systems in research and development", "Legal & IP Team", "Strong protection for core systems, need better controls for collaborative research data", "Implement enhanced data classification and access controls for research partnerships", 82, "Complete")
    ]
    
    for title, audit_type, scope, auditor, findings, recommendations, score, status in audits:
        db.add_audit(title, audit_type, scope, auditor, findings, recommendations, score, status)
        print(f"✓ Added audit: {title}")
    
    print(f"\n✓ SME Chemical Company sample data creation completed successfully!")
    print(f"✓ Application populated with realistic chemical industry AI use cases")
    print(f"✓ Includes R&D AI systems: synthesis prediction, molecular discovery, predictive maintenance")
    print(f"✓ Includes business AI systems: supply chain, demand forecasting, document processing")
    
    # Display summary
    stats = db.get_dashboard_stats()
    print(f"\n=== ChemTech Industries AI Management Dashboard ===")
    print(f"📊 Total AI Assets: {stats['total_assets']} (R&D: 5, Business: 5, Data: 5)")
    print(f"⚠️  Active Risks: {stats['active_risks']} (Critical: 5, High: 3, Medium: 2)")
    print(f"🛡️  Implemented Controls: {stats['implemented_controls']} (Safety-focused)")
    print(f"🚨 Open Incidents: {stats['open_incidents']} (Process safety & data quality)")
    print(f"✅ Completed Audits: {stats['completed_audits']} (Regulatory & safety compliance)")
    print(f"\n🏭 Ready for chemical industry ISO 42001 compliance management!")

if __name__ == "__main__":
    create_sample_data()