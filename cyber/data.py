import pandas as pd
from datetime import datetime, timedelta

VULNERABILITIES = [
    {
        "ID": "VUL-001",
        "Name": "SQL Injection in Login Form",
        "Category": "Application",
        "Severity": "Critical",
        "CVSS Score": 9.8,
        "Status": "Open",
        "Discovered": "2026-03-20",
        "Description": "Login form is vulnerable to SQL injection due to unsanitized user input.",
        "Recommendation": "Use parameterized queries / prepared statements. Implement input validation and WAF."
    },
    {
        "ID": "VUL-002",
        "Name": "Unencrypted Data Transfer",
        "Category": "Network",
        "Severity": "Critical",
        "CVSS Score": 9.1,
        "Status": "In Progress",
        "Discovered": "2026-03-18",
        "Description": "Sensitive data transmitted over HTTP instead of HTTPS on internal API endpoints.",
        "Recommendation": "Enforce TLS 1.2+ for all communications. Redirect all HTTP traffic to HTTPS."
    },
    {
        "ID": "VUL-003",
        "Name": "Weak Password Policy",
        "Category": "Authentication",
        "Severity": "High",
        "CVSS Score": 7.5,
        "Status": "Open",
        "Discovered": "2026-03-15",
        "Description": "Intern accounts lack minimum password length and complexity requirements.",
        "Recommendation": "Enforce min 12 characters, uppercase, lowercase, number, and special character."
    },
    {
        "ID": "VUL-004",
        "Name": "Missing Multi-Factor Authentication",
        "Category": "Authentication",
        "Severity": "High",
        "CVSS Score": 8.0,
        "Status": "In Progress",
        "Discovered": "2026-03-28",
        "Description": "MFA not enforced for VPN and cloud console access by intern accounts.",
        "Recommendation": "Enforce MFA using TOTP or hardware keys for all remote access points."
    },
    {
        "ID": "VUL-005",
        "Name": "Excessive User Privileges",
        "Category": "Access Control",
        "Severity": "High",
        "CVSS Score": 7.2,
        "Status": "Open",
        "Discovered": "2026-03-25",
        "Description": "Interns have admin-level access to development databases and cloud consoles.",
        "Recommendation": "Implement least-privilege principle. Assign role-based access control (RBAC)."
    },
    {
        "ID": "VUL-006",
        "Name": "Insecure File Upload",
        "Category": "Application",
        "Severity": "Medium",
        "CVSS Score": 6.5,
        "Status": "Open",
        "Discovered": "2026-04-01",
        "Description": "File upload does not validate file types or scan for malware.",
        "Recommendation": "Validate MIME types, restrict extensions, scan uploads with antivirus before storage."
    },
    {
        "ID": "VUL-007",
        "Name": "Outdated Software Dependencies",
        "Category": "Application",
        "Severity": "Medium",
        "CVSS Score": 5.4,
        "Status": "Resolved",
        "Discovered": "2026-03-22",
        "Description": "Several packages are outdated with known CVEs.",
        "Recommendation": "Run audit tools (npm audit / pip-audit). Establish regular dependency update schedule."
    },
    {
        "ID": "VUL-008",
        "Name": "No Security Awareness Training",
        "Category": "Human",
        "Severity": "Medium",
        "CVSS Score": 5.0,
        "Status": "Resolved",
        "Discovered": "2026-04-03",
        "Description": "Interns receive no formal cybersecurity orientation when joining the program.",
        "Recommendation": "Mandatory onboarding security training covering phishing, data handling, and incident reporting."
    },
]

TRAINING_MODULES = [
    {
        "id": 1,
        "title": "Introduction to Cybersecurity",
        "level": "Beginner",
        "duration": "30 min",
        "description": "Fundamentals of cybersecurity: CIA triad, threat landscape, and basic terminology.",
        "topics": ["CIA Triad", "Types of Threats", "Cybersecurity Careers", "Basic Terminology"],
        "completed": True,
        "score": 92
    },
    {
        "id": 2,
        "title": "Phishing & Social Engineering",
        "level": "Beginner",
        "duration": "45 min",
        "description": "Recognize and respond to phishing attacks and social engineering tactics.",
        "topics": ["Types of Phishing", "Red Flags in Emails", "Reporting Suspicious Activity", "Real-world Examples"],
        "completed": True,
        "score": 88
    },
    {
        "id": 3,
        "title": "Password Security & Authentication",
        "level": "Intermediate",
        "duration": "35 min",
        "description": "Best practices for strong passwords, MFA, and credential management.",
        "topics": ["Password Strength", "Password Managers", "Multi-Factor Authentication", "Credential Stuffing"],
        "completed": False,
        "score": None
    },
    {
        "id": 4,
        "title": "Network Security Basics",
        "level": "Intermediate",
        "duration": "60 min",
        "description": "Understand firewalls, VPNs, secure Wi-Fi, and network threats.",
        "topics": ["Firewalls & IDS", "VPN Usage", "Wi-Fi Security", "Man-in-the-Middle Attacks"],
        "completed": False,
        "score": None
    },
    {
        "id": 5,
        "title": "Secure Coding Practices",
        "level": "Advanced",
        "duration": "90 min",
        "description": "Write secure code: input validation, OWASP Top 10, and security testing.",
        "topics": ["OWASP Top 10", "Input Validation", "SQL Injection Prevention", "XSS Prevention"],
        "completed": False,
        "score": None
    },
    {
        "id": 6,
        "title": "Data Protection & Privacy",
        "level": "Intermediate",
        "duration": "40 min",
        "description": "GDPR basics, data classification, encryption, and secure data handling.",
        "topics": ["Data Classification", "Encryption Basics", "GDPR Overview", "Secure Data Disposal"],
        "completed": False,
        "score": None
    },
]

QUIZ_QUESTIONS = {
    1: {
        "title": "Cybersecurity Fundamentals Quiz",
        "questions": [
            {
                "q": "What does CIA stand for in cybersecurity?",
                "options": ["Central Intelligence Agency", "Confidentiality, Integrity, Availability", "Cyber Incident Awareness", "Control, Identify, Analyze"],
                "answer": 1
            },
            {
                "q": "Which of the following is NOT a type of malware?",
                "options": ["Ransomware", "Trojan", "Firewall", "Spyware"],
                "answer": 2
            },
            {
                "q": "What is the primary goal of a phishing attack?",
                "options": ["To crash a system", "To steal sensitive information", "To improve network speed", "To install updates"],
                "answer": 1
            },
            {
                "q": "Which principle means giving users only the access they need?",
                "options": ["Defense in Depth", "Least Privilege", "Zero Trust", "Need to Know"],
                "answer": 1
            },
            {
                "q": "What does a VPN primarily provide?",
                "options": ["Faster internet", "Encrypted connection", "Free Wi-Fi", "Virus protection"],
                "answer": 1
            },
        ]
    },
    2: {
        "title": "Phishing Awareness Quiz",
        "questions": [
            {
                "q": "Which is a common sign of a phishing email?",
                "options": ["Clear sender identity", "Urgent language and suspicious links", "Proper grammar throughout", "Known company branding only"],
                "answer": 1
            },
            {
                "q": "Spear phishing targets:",
                "options": ["Random individuals", "Specific individuals or organizations", "Only executives", "Only IT staff"],
                "answer": 1
            },
            {
                "q": "What should you do if you receive a suspicious email?",
                "options": ["Click the link to verify", "Reply asking for more info", "Report it to IT/security team", "Delete and ignore it"],
                "answer": 2
            },
            {
                "q": "Vishing is phishing via:",
                "options": ["Email", "Text message", "Voice/phone call", "Social media"],
                "answer": 2
            },
            {
                "q": "A legitimate organization will NEVER ask for your password via:",
                "options": ["Their secure website portal", "Email", "In-person with ID verification", "Phone with known callback number"],
                "answer": 1
            },
        ]
    }
}

REPORTS = [
    {
        "id": 1,
        "title": "Initial Security Assessment Report",
        "date": "2026-03-30",
        "type": "Assessment",
        "status": "Final",
        "author": "Nishchay Kumar",
        "summary": "Comprehensive assessment of the cybersecurity posture of the Tech Intern Program at Tinymart Global Private Limited, Noida.",
        "critical": 2, "high": 3, "medium": 2, "low": 1,
        "recommendations": [
            "Immediately patch SQL injection vulnerability in login module",
            "Enforce HTTPS across all services and endpoints",
            "Implement MFA for all intern accounts",
            "Conduct mandatory security awareness training for all interns",
        ]
    },
    {
        "id": 2,
        "title": "Monthly Security Progress Report – April 2026",
        "date": "2026-04-30",
        "type": "Progress",
        "status": "Final",
        "author": "Nishchay Kumar",
        "summary": "Monthly tracking of vulnerability remediation progress and training completion rates across the intern program.",
        "critical": 1, "high": 2, "medium": 2, "low": 0,
        "recommendations": [
            "Accelerate MFA rollout – currently 40% complete",
            "Address remaining critical vulnerability: SQL injection",
            "Increase training completion rate from 67% to 90%",
        ]
    },
]

ACTIVITY_FEED = [
    {"Time": "2 hours ago",  "Event": "SQL Injection risk identified in login module",        "Type": "🔴 Vulnerability"},
    {"Time": "4 hours ago",  "Event": "Intern batch 3 completed Phishing Awareness module",    "Type": "🟢 Training"},
    {"Time": "1 day ago",    "Event": "Weak password policy patched on dev servers",           "Type": "🟡 Mitigation"},
    {"Time": "1 day ago",    "Event": "New quiz assigned: Network Security Basics",            "Type": "🔵 Training"},
    {"Time": "2 days ago",   "Event": "Unencrypted data transfer detected on API endpoint",    "Type": "🔴 Vulnerability"},
    {"Time": "3 days ago",   "Event": "Security Assessment scan completed",                    "Type": "🟡 Assessment"},
]


def get_vuln_df():
    return pd.DataFrame(VULNERABILITIES)