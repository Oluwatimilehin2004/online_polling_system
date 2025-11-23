# Voteasy - Secure Online Voting System

![Voteasy Logo](https://via.placeholder.com/150x150/4A90E2/FFFFFF?text=VE) 
*A modern, secure, and accessible digital voting platform*

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Admin Panel](#admin-panel)
- [Security Features](#security-features)
- [Troubleshooting](#troubleshooting)
- [Development Notes](#development-notes)
- [License](#license)

## Overview

Voteasy is a comprehensive online voting solution designed to provide secure, transparent, and accessible democratic participation. The system ensures election integrity through multi-factor authentication, real-time monitoring, and robust security protocols.

### Key Benefits
- ✅ **Secure Authentication** - OTP-based verification system
- ✅ **Real-time Results** - Live election monitoring
- ✅ **Admin Control** - Complete election management
- ✅ **Voter Privacy** - Anonymous voting with audit trails
- ✅ **Accessibility** - User-friendly command-line interface

## Features

### Core Functionality
- **User Registration & Authentication**
  - Phone number verification
  - OTP-based login system
  - Secure user profile management

- **Voting System**
  - Candidate listing and selection
  - One-vote-per-user enforcement
  - Real-time vote counting
  - Election period controls

- **Admin Management**
  - Poll creation and management
  - Candidate management
  - Voting period configuration
  - Results monitoring

### Security Features
- **OTP Verification** - Time-based one-time passwords
- **Vote Integrity** - Immutable vote records
- **Session Management** - Secure user sessions
- **Database Security** - Protected data storage

## System Architecture

Voteasy System Architecture
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │◄──►│  Application │◄──►│  Database   │
│  Interface  │    │    Layer     │    │   MySQL     │
└─────────────┘    └─────────────┘    └─────────────┘
                            │
                    ┌─────────────┐
                    │   OTP       │
                    │  Service    │
                    └─────────────┘
```

### Database Schema
```sql
-- Core Tables Structure
Users (usr_id, phone_number, national_id, has_voted, ...)
Candidates (cand_id, cand_name, political_party, vote_count, ...)
Polls (poll_id, title, start_time, end_time, ...)
Vote_records (vote_id, usr_id, cand_id, timestamp, ...)
```

## Installation Guide

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7+
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/Oluwatimilehin2004/online_polling_system.git
cd online_polling_system
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
```text
mysql-connector-python==8.0.0
twilio==8.0.0
```

### Step 4: Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE online_polling_system;

# Import schema (if provided)
mysql -u root -p online_polling_system < schema.sql
```

### Step 5: Configuration
Update `config.py` with your database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'online_polling_system'
}
```

## Configuration

### OTP Settings
- **OTP Expiry Time**: 5 minutes
- **OTP Length**: 6 digits
- **Max Attempts**: 3 attempts per session

### Voting Period
- **Default Duration**: Configurable by admin
- **Time Format**: YYYY-MM-DD HH:MM:SS
- **Timezone**: System local time

### File Structure
```
voteasy/
├── main.py              # Main application entry point
├── user.py              # User management module
├── admin.py             # Admin management module
├── voter.py             # Voting logic module
├── candidate.py         # Candidate management
├── database.py          # Database connection handler
├── utils.py             # Utility functions (OTP, etc.)
└── otp_logs/           # OTP log directory (auto-created)
    ├── user_7972_otp.log
    └── user_1234_otp.log
```

## Usage Guide

### For Voters

#### 1. Registration Process
```bash
# Start the application
python main.py
```

**Registration Flow:**
1. Enter phone number
2. Provide personal details (National ID, Date of Birth, Hobbies)
3. Receive OTP via console (development mode)
4. Verify OTP to complete registration

#### 2. Voting Process
1. Login with registered phone number
2. Receive and enter OTP
3. View available candidates
4. Select preferred candidate
5. Confirm vote selection

#### 3. Profile Management
- View personal information
- Update region and age
- Check voting status

### OTP Behavior Scenarios

| Scenario | System Response |
|----------|-----------------|
| **New OTP Request** | Generates 6-digit code, valid for 5 minutes |
| **OTP Not Expired** | Uses existing OTP, no new code sent |
| **OTP Expired** | Automatically generates and sends new OTP |
| **Max Attempts Exceeded** | Locks authentication for 15 minutes |

## Admin Panel

### Default Admin Credentials
```yaml
Username: admin
Password: admin123
```

*⚠️ Important: We will change these credentials in production environment*

### Admin Functions

#### 1. Poll Management
```bash
# Create new poll
Admin Panel 
→ Create New Poll
→ Enter poll details
→ Set start and end times
```

#### 2. Candidate Management
- Add new candidates to polls
- Edit candidate information (name, party, region)
- **Restriction**: Cannot modify vote counts

#### 3. Voting Period Control
- Set election start and end times
- Extend voting periods if needed
- Real-time status monitoring

#### 4. Results Monitoring
- Live vote counting
- Candidate ranking by votes
- Poll-specific or overall results

### Admin Commands Examples
```python
# Create poll
admin.create_poll("General Election 2024", "National elections", "2024-01-01 00:00:00", "2024-01-07 23:59:59")

# Add candidate
admin.add_candidate("John Doe", "Democratic Party", "North Region", 1)

# Extend voting
admin.extend_voting_period(1, "2024-01-14 23:59:59")
```

## Security Features

### Authentication Security
- **Two-Factor Authentication**: Phone + OTP verification
- **Session Management**: Automatic timeout
- **Brute Force Protection**: 3-attempt limit with cool-down

### Data Protection
- **Vote Secrecy**: No direct link between voter and candidate choice
- **Data Integrity**: Immutable vote records
- **Audit Trail**: Complete voting history

### OTP Security
```python
# OTP Generation and Storage
- Individual log files per user (last 4 digits of phone)
- Secure timestamp tracking
- Automatic cleanup of expired OTPs
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Test database connection
python -c "from database import Database; print('Connected successfully' if Database().test_connection() else 'Failed')"
```

#### 2. OTP Not Received
- Check `otp_logs/` directory for generated OTPs
- Verify phone number format
- Check system time synchronization

#### 3. Voting Period Errors
```sql
-- Check poll status
SELECT poll_id, title, start_time, end_time, NOW() as current_time 
FROM Polls WHERE is_active = TRUE;
```

#### 4. Permission Issues
```bash
# Fix file permissions
chmod 755 *.py
chmod -R 755 otp_logs/
```

### Error Messages and Solutions

| Error Message | Solution |
|---------------|----------|
| `Authentication plugin 'caching_sha2_password'` | Update MySQL connector or alter user authentication |
| `Unknown column 'id' in 'field list'` | Check database schema alignment |
| `Module 'datetime' has no attribute 'now'` | Verify Python imports in user.py |
| `Voting period has ended` | Admin must extend voting period |

## Development Notes

### Twilio SMS Restriction (Rwanda)
**Issue**: Rwanda has regulatory restrictions on automated SMS sending from software applications, including Twilio services.

**Solution Implemented**:
```python
def send_otp(phone_number, otp):
    """
    Development-mode OTP simulation
    In production, replace with actual SMS service
    compliant with local regulations
    """
    print(f"OTP for {phone_number}: {otp}")
    # Log to secure user-specific files
    log_otp_to_file(phone_number, otp)
```

**Production Recommendation**:
- Partner with local telecom providers
- Implement USSD-based verification
- Use approved SMS gateways for Rwanda

### Database Migration Notes
```sql
-- Required schema modifications
ALTER TABLE Candidates ADD COLUMN poll_id INT NOT NULL DEFAULT 1;
ALTER TABLE Polls ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
```

### Performance Considerations
- Indexed database queries for large voter bases
- Batch processing for result calculations
- Connection pooling for high concurrency

## Support

### Technical Support
- **Documentation**: [docs.voteasy.com](https://docs.voteasy.com)
- **Issues**: [GitHub Issues](https://github.com/Oluwatimilehin2004/online_polling_system.git/issues)
- **Email**: support@voteasy.com

### Emergency Contacts
- **System Admin**: admin@voteasy.com
- **Security Team**: security@voteasy.com

## Monitoring and Analytics

### Log Files Location
```
otp_logs/           # OTP verification logs
database_logs/      # Database operation logs
system_logs/        # Application operation logs
```

### Key Metrics to Monitor
- Voter registration rate
- Voting completion percentage
- System uptime and performance
- Security incident reports

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2024-01-01 | Initial release with core voting features |
| v1.1.0 | 2024-01-15 | Added admin panel and poll management |
| v1.2.0 | 2024-02-01 | Enhanced security and OTP system |

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

<div align="center">

**Voteasy** - *Empowering Democratic Participation Through Technology*

*Built with ❤️ for transparent and accessible elections*

[Report Bug](https://github.com/Oluwatimilehin2004/online_polling_system.git/issues) • [Request Feature](https://github.com/Oluwatimilehin2004/online_polling_system.git/issues)

</div>
```

